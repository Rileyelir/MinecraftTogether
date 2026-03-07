# c_setup.py
# Handles the creation of new servers by downloading the chosen server file, auto-generating a start script, and automatically adding it to mt_data.json.

# Imports
import requests
import json

# Functions
def download_jar(version: str):
    vanillaManifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    for v in vanillaManifest["versions"]:
        if v["id"] == version:
            print("[SUCCESS] Version found, downloading...")
            versionInfo = requests.get(v["url"]).json()
            serverJar = requests.get(versionInfo["downloads"]["server"]["url"], stream=True)
            with open("MinecraftServer_" + version + ".jar", "wb") as file:
                for chunk in serverJar.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("[SUCCESS] Server file downloaded successfully.")

# Testing Code (ran when running c_setup.py separately)
download_jar("1.17.1")