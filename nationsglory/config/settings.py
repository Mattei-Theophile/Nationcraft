import sys
import os
import subprocess


class PathGestion:
    def __init__(self):
        self.os_sys = sys.platform
        self.ng_dir = self.get_ng_dir()


    def get_ng_dir(self):
        ng_path = None
        match self.os_sys:
            case "window":
                ng_path = os.getenv("APPDATA")
                ng_path = os.path.join(ng_path, ".NationsGlory")
            case "linux":
                subprocess.run(["xhost +"], shell=True)
                ng_path = f"/home/{os.getlogin()}/.config/.NationsGlory"


        return ng_path

    def get_log_file(self):
        if self.ng_dir is None:
            raise ValueError("Le chemin du dossier ng n'est pas enregistré")

        else:

            path = os.path.join(self.ng_dir, "versions/stable/")
            with open(f"{path}/output-client.log", "r") as file:
                file = file.readlines()


        return file

    def get_mod_loaders(self):
        if self.ng_dir is None:
            raise ValueError("Le chemin du dossier ng n'est pas enregistré")

        else:

            path = os.path.join(self.ng_dir, "versions/stable/")
            with open(f"{path}/ForgeModLoader-client-0.log", "r") as file:
                file = file.readlines()


        return file