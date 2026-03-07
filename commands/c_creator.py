# c_creator.py
# Handles the creation of new servers by downloading the chosen server file, auto-generating a start script, and automatically adding it to mt_data.json.

# Imports
import requests
from os import mkdir

# Functions
def create_server():
    print("\n-- Server Creator --")
    name = input("Server Name: ")
    version = input("Server Version (i.e. 1.12, 1.21.11): ")

    mkdir(name)
    download_vanilla_jar(version, name)

    maxRam = input("\nServer Ram Limit (gb): ")
    with open(f"{name}/start.bat", "w") as file:
        file.write(f"java -Xmx{maxRam}G -Xms{maxRam}G -jar server.jar")

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

# Testing Code (ran when running c_setup.py separately)
create_server()