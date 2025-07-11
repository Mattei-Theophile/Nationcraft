import discord
from discord.ext import commands
from nationsglory.config import settings
import time
from nationsglory.player import Player
from typing import List, Optional


class ChatMessageProcessor:
    """Handles processing and formatting of chat messages."""

    def __init__(self):
        self.last_sentence = settings.PathGestion().get_log_file()[-1]

    def _remove_color_codes(self, text: List[str]) -> str:
        """Removes color codes (§ followed by a character) from text."""
        i = 0
        while i < len(text):
            if text[i] == "§":
                text.pop(i + 1)
                text.pop(i)
                i -= 1
            i += 1
        return "".join(text)

    def convert_chat_message(self, sentence: str) -> Optional[str]:
        """Converts a raw chat message to a formatted string."""
        words = sentence.split(" ")
        if len(words) < 4 or words[4] != "[CHAT]":
            return None

        # Remove newline character from the last word
        words[-1] = words[-1].rstrip('\n')
        timestamp = words[0]
        log_level = words[1]

        # Regular chat message
        if "banner" not in words[5]:
            text = self._remove_color_codes(list(" ".join(words[5:])))
            return f"[{timestamp}] [{log_level}] {text}"

        # Player with rank message
        elif "rank" in words[7]:
            grade = words[6][4:-1]
            country = words[10][6:-1]
            player_name = words[15][6:].split("§")[0]
            message = self._remove_color_codes(list(" ".join(words[17:])))
            return f"[{timestamp}] [{log_level}] [{grade}] [{player_name}] [{country}] » {message}"

        # Player disconnection message
        elif "minus" in words[6]:
            player = words[7]
            connected_status = words[8]
            return f"[{timestamp}] [{log_level}] » Le joueur {player} s'est déconnecté {connected_status}"

        # Player connection message
        elif "plus" in words[6]:
            player = words[7]
            connected_status = words[8]
            return f"[{timestamp}] [{log_level}] » Le joueur {player} s'est connecté {connected_status}"

        # System messages (assault, announce)
        elif any(keyword in words[6] for keyword in ["assault", "announce"]):
            message = self._remove_color_codes(list(" ".join(words[7:])))
            return f"[{timestamp}] [{log_level}] » {message}"

        # Default fallback
        else:
            message = " ".join(words)
            return f"[{timestamp}] [{log_level}] » {message}"

    def get_new_messages(self) -> List[str]:
        """Gets new messages from the log file."""
        path = settings.PathGestion()
        file = path.get_log_file()
        messages = []

        # Find where we left off last time
        offset = 0
        while self.last_sentence != file[-offset-1]:
            offset += 1
            if offset >= len(file):
                break

        # Process new messages
        for i in range(offset, 0, -1):
            formatted_message = self.convert_chat_message(file[-i])
            if formatted_message:
                messages.append(formatted_message)

        # Update last seen message
        if file:
            self.last_sentence = file[-1]

        return messages


class DiscordBot(commands.Bot):
    """Discord bot for in-game chat integration."""

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)
        self.chat_processor = ChatMessageProcessor()

        # Register commands
        self.add_command(self.message)
        self.add_command(self.activate_chat)
        self.add_command(self.deactivate_chat)

    @commands.command(name="message")
    async def message(self, ctx: commands.Context, *args):
        """Sends a message from Discord to the game chat."""
        await ctx.message.delete()

        if settings.id_author_discord != ctx.author.id:
            await ctx.send("Vous n'avez pas lié votre tchat")
            return

        discord_message = ' '.join(args)
        try:
            player = Player(settings.PathGestion().link_key_control())
            time.sleep(3)
            player.open_chat()
            player.write(discord_message)
            await ctx.send(f"[Discord] [{ctx.author.name}] » {discord_message}")
        except Exception as e:
            await ctx.send(f"Problème avec l'envoi du message: {str(e)}")

    @commands.command(name="deactivate_tchat")
    async def deactivate_chat(self, ctx: commands.Context):
        """Unlinks the in-game chat from Discord."""
        await ctx.message.delete()
        settings.id_author_discord = 0
        await ctx.send(f"le tchat est délié de {ctx.author.name}")

    @commands.command(name="activate_tchat")
    async def activate_chat(self, ctx: commands.Context):
        """Links the in-game chat to Discord."""
        await ctx.message.delete()
        settings.id_author_discord = ctx.author.id
        await ctx.send(f"le tchat est lié avec {ctx.author.name}")

    async def on_ready(self):
        """Called when the bot is ready and connected."""
        print(f'We have logged in as {self.user}')

    async def write_chat_to_discord(self, ctx: commands.Context):
        """Continuously monitors for new chat messages and sends them to Discord."""
        while True:
            messages = self.chat_processor.get_new_messages()
            for msg in messages:
                await ctx.send(msg)


def main():
    """Main entry point for the bot."""
    bot = DiscordBot()
    bot.run(settings.token_bot)
