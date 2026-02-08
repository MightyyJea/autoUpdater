import subprocess
import requests
import os
import json

configpath = "config.json"

path = "feriumconf.json"


def initFeriumConf():
    feriumconf = {
        "active_profile": 1,
        "profiles": [
            {
                "name": "main",
                "output_dir": f"{os.getcwd()}/mods",
                "game_version": "1.21.1",
                "mod_loader": "Fabric",
                "mods": [],
            }
        ],
    }
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(feriumconf, f, indent=4)
    ferium("profile", "switch")


def getremote():
    if not os.path.exists(configpath):
        with open(configpath, "w", encoding="utf-8") as f:
            json.dump({"remote": "127.0.0.1:5000", "patchversion": 0}, f, indent=4)

            return "127.0.0.1:5000", 0
    else:
        with open(configpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["remote"], data["patchversion"]


def ferium(command, args):
    subprocess.run(["./ferium", "--config-file", path, command, args])


def fetchNewPatch():
    remote, patch = getremote()
    serverPatch = requests.get(f"http://{remote}/getpatch").json
    if patch == serverPatch:
        print("tout est a jour !")
        return
    print("Mise a jour detecter")
    with open(configpath, "w", encoding=4) as f:
        data = json.load(f)
        data["patchversion"] = serverPatch
        json.dump(data, f, indent=4)

    initFeriumConf()
    modlist = requests.get(f"http://{remote}/getmodlist").json()

    for i in modlist:
        ferium("add", i["modid"])


fetchNewPatch()
