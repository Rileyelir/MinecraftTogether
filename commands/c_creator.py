# c_creator.py
# Handles the creation of new servers by downloading the chosen server file, auto-generating a start script, and automatically adding it to mt_data.json.

# Imports
import requests
from os import mkdir
from shutil import rmtree
from pathlib import Path
from commands.deps import data_interface

# Functions
def create_server(): # Returning 0 means failed, 1 means success (in an ideal world)
    print("\n-- Server Creator --")
    name = input("Server Name: ")
    version = input("Server Version (i.e. 1.12, 1.21.11): ")

    mkdir(name)
    download_vanilla_jar(version, name)

    maxRam = int(input("\nServer Ram Limit (gb): "))

    while True: # EULA Check
        print("\nhttps://account.mojang.com/documents/minecraft_eula")
        eula = input("Do you agree to the Minecraft EULA found above? (Y/n): ")

        match eula.lower():
            case "y"|"":
                with open(f"{name}/eula.txt", "w") as file:
                    file.write("eula=true")
                break
            case "n":
                print("EULA disagreed to, server creation shutting down.")
                rmtree(name)
                return 0
            case _:
                print("Invalid answer, try again.")

    data_interface.add_server(name, str(Path(name).resolve())+"/server.jar", maxRam)
    print(f"\nServer creation completed, {name} added to server list.")

def download_vanilla_jar(version, path):
    vanillaManifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    for v in vanillaManifest["versions"]:
        if v["id"] == version:
            print("\n[SUCCESS] Version found, downloading...")
            versionInfo = requests.get(v["url"]).json()
            serverJar = requests.get(versionInfo["downloads"]["server"]["url"], stream=True)
            with open(f"{path}/server.jar", "wb") as file:
                for chunk in serverJar.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("[SUCCESS] Server file downloaded successfully.")
            return
    print("[ERROR] Version not found or other error occurred.")