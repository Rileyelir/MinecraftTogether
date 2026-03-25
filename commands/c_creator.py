# c_creator.py
# Handles the creation of new servers by downloading the chosen server file, auto-generating a start script, and automatically adding it to mt_data.json.

# Imports
import requests
from os import mkdir
from shutil import rmtree
from pathlib import Path
from commands.deps import data_interface

# Functions

# Gets user input on different things about the server they want to make, and puts it all together by calling download functions and setting data
def create_server():
    print("\n-- Server Creator --")
    name = input("Server Name: ")
    mkdir(name)

    while True:
        print("\nServer Types:\n1. Vanilla\n2. Paper\n3. Forge (unimplemented)")
        stype = input("? ")
        if stype == "1" or stype == "2": # Add 3 when forge is implemented
            break
        else:
            print("[ERROR] Answer not valid, please try again.")

    version = input("\nServer Version (1.12.2, etc): ")
    try:
        match stype:
            case "1":
                download_vanilla_jar(version, name)
            case "2":
                download_paper_jar(version, name)
    except Exception as e:
        print("\n[ERROR] Connection with one of the providers' API has failed. Either the provider is down or you are not connected to the internet.")
        print(e)
        rmtree(name)
        return

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
                return
            case _:
                print("[ERROR] Invalid answer, try again.")

    data_interface.add_server(name, str(Path(name).resolve())+"/server.jar", maxRam)
    print(f"\nServer creation completed, {name} added to server list.")

# Fetches the official version manifest and sifts through it to find the selected version and downloads it
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

# Uses the PaperMC v2 api and builds on top of a url after finding the version and the build number and downloads the server file.
def download_paper_jar(version, path):
    url = "https://api.papermc.io/v2/projects/paper"
    for v in requests.get(url).json()["versions"]:
        if v == version:
            download_url = url + f"/versions/{v}/builds"
            print("\n[SUCCESS] Version found, downloading...")

            build = requests.get(url + f"/versions/{v}/builds").json()["builds"][-1]["build"] # most recent build
            serverJar = requests.get(url + f"/versions/{v}/builds/{build}/downloads/paper-{v}-{build}.jar", stream=True)
            with open(f"{path}/server.jar", "wb") as file:
                for chunk in serverJar.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("[SUCCESS] Server file downloaded successfully.")
            return
    print("[ERROR] Version not found or other error occurred.")