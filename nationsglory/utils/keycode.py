import os

key_control_py = {"-100": "Button 1",
            "-99": "Button 2",
            "44": "w",
            "16" : "a",
            "31": "s",
            "32": "d",
            "57": "space",
            "42": "shiftleft",
            "30": "q",
            "18": "e",
            "20": "t",
            "15": "tab",
            "-98": "Button 3",
            "-96": "Button 5",
            "53": "/",
            "38": "l",
            "184": "rmenu",
            "36": "j",
            "37": "k",
            "50": "m",
            "64": "f6",
            "46": "c",
            "29": "ctrlleft",
            "22": "u",
            "25": "p",
            "-97": "Button 4",
            "11": "0",
            "67": "f9",
            "65": "f7",
            "35": "h",
            "48": "b",
            "60": "f2",
            "61": "f3",
            "59": "f1",
            "63": "f5",
            "66": "f8",
            "87": "f11",
            "17": "w",
            "28": "return",
            "2": "1",
            "3": "2",
            "4": "3",
            "5": "4",
            "6": "5",
            "7": "6",
            "8": "7",
            "9": "8",
            "10": "9",
            "33": "f",
            "19": "r",
            "47": "v",
            "34": "g",
            "210": "insert",
            "49": "n",
            "26": "{",
            "13": "=",
            "39": ";"}


class KeycodeManager:
    """
    Manages key code mappings between Minecraft and Python.
    """
    def __init__(self, ng_dir=None):
        self.ng_dir = ng_dir
        
    def get_key_control(self):
        """
        Reads key controls from the game's options.txt file.
        
        Returns:
            dict: A dictionary mapping key codes to key names
        
        Raises:
            ValueError: If ng_dir is not set
        """
        if self.ng_dir is None:
            raise ValueError("Le chemin du dossier ng n'est pas enregistré")

        else:
            key_control_minecraft = {}
            path = os.path.join(self.ng_dir, "versions/stable/options.txt")
            with open(path, "r") as f:
                txt = f.readlines()

            for line in txt:
                if line[:3] == "key":
                    line = line[:-1]
                    key_control_minecraft[line.split(":")[1]] = line.split(":")[0]
                else:
                    continue
        return key_control_minecraft

    def link_key_control(self):
        """
        Links Minecraft key controls to Python key controls.
        
        Returns:
            dict: A dictionary mapping Minecraft key names to Python key names
        """
        linked_key_control = {}
        key_control_minecraft = self.get_key_control()
        for key, value in key_control_minecraft.items():
            if key in key_control_py.keys():
                linked_key_control[value] = key_control_py[key]
        return linked_key_control