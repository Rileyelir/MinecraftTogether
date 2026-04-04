# c_creator.py
# Handles the creation of new servers by downloading the chosen server file, auto-generating a start script, and automatically adding it to mt_data.json.

# Imports
import requests
from os import mkdir, listdir, remove
from os import name as osName
from shutil import rmtree
from pathlib import Path
from commands.deps import data_interface
from time import sleep
import subprocess
from tkinter import filedialog

# Variables
defaultCMD = [
    "java", 
    "", # Placeholder/template for something like -Xmx4G
    "", 
    "-jar",
    "", # Start file path
    "--nogui"
]

# Functions

# Gets user input on different things about the server they want to make, and puts it all together by calling download functions and setting data
def create_server():
    print("\n-- Server Creator --")
    name = input("Server Name: ")
    mkdir(name)
    serverInfo = []

    while True:
        print("\nServer Types:\n1. Vanilla\n2. Paper\n3. Forge")
        stype = input("? ")
        if stype == "1" or stype == "2" or stype == "3":
            break
        else:
            print("[ERROR] Answer not valid, please try again.")
    
    maxRam = int(input("\nServer Ram Limit (gb): "))
    version = input("\nServer Version (1.12.2, etc): ")
    try:
        match stype:
            case "1":
                serverInfo = download_vanilla_jar(version, name)
            case "2":
                serverInfo = download_paper_jar(version, name)
            case "3":
                serverInfo = download_forge_jar(version, name, maxRam)
    except Exception as e:
        print("\n[ERROR] Connection with one of the providers' API has failed. Either the provider is down or you are not connected to the internet.")
        #print(e)
        rmtree(name)
        return
    
    if serverInfo == []: # If something went wrong in one of the download functions, cancel server creation
        rmtree(name)
        return

    # Specify Java version check
    print("\nDo you want to specify a version of Java to use? (y/N)")
    print("This is only required for servers that don't specifically work with the Java version found in your PATH. Select no if this doesn't apply to you.")
    print("If you are running a modern Forge server (1.17+), you will have to add the path to the jvm arguments in the server files manually for now.")
    javaChoice = input("? ")
    if javaChoice.lower() == "y":
        serverInfo[1][0] = filedialog.askopenfilename(title="Select the executable for the specified Java version.")
        print("[SUCCESS] Java version set for this server.")

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

    if serverInfo[1] == defaultCMD: # if not a modern forge server, set proper thingamajigs
        serverInfo[1][1] = f"-Xmx{maxRam}G"
        serverInfo[1][2] = f"-Xms{maxRam}G"
        serverInfo[1][4] = serverInfo[0]

    data_interface.add_server(name, serverInfo[0], maxRam, serverInfo[1])
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
            return [str(Path(path).resolve())+"/server.jar", defaultCMD]
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
            return [str(Path(path).resolve())+"/server.jar", defaultCMD]
    print("[ERROR] Version not found or other error occurred.")

# Find forge version and download a server installer, install the server, cleanup installation files.
def download_forge_jar(version, path, maxRam):
    try:
        try:
            forgeVersion = requests.get("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json").json()["promos"][version+"-recommended"]
        except:
            forgeVersion = requests.get("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json").json()["promos"][version+"-latest"]
        print("\n[SUCCESS] Version found, downloading installer...")
        isLegacy = True if int(version.split(".")[1]) < 17 else False

        fullVersion = version+"-"+forgeVersion
        serverJar = requests.get(f"https://maven.minecraftforge.net/net/minecraftforge/forge/{fullVersion}/forge-{fullVersion}-installer.jar", stream=True)
        with open(f"{path}/server-installer.jar", "wb") as file:
            for chunk in serverJar.iter_content(chunk_size=8192):
                file.write(chunk)
        print("[SUCCESS] Forge installer downloaded, installing server... (this may take a minute)")

        cmd = [
            "java",
            "-jar",
            "server-installer.jar",
            "--installServer"
        ]
        process = subprocess.Popen(
            cmd,
            cwd=Path(path).absolute(),
            #stdout=subprocess.DEVNULL,
            text=True
        )
        process.wait()

        print("\n[SUCCESS] Server installer finished, finding start file and cleaning up...")
        startFile: Path
        selectedCMD = defaultCMD
        if isLegacy:
            for f in listdir(path):
                if f.endswith(".jar") and f[0:5] == "forge":
                    startFile = str(Path(f"{path}/{f}").absolute())
                if f[0:16] == "server-installer":
                    remove(f"{path}/{f}")
        else:
            for f in listdir(path):
                if ((osName == "nt" and f.endswith(".bat")) or (osName != "nt" and f.endswith(".sh"))) and f[0:3] == "run":
                    startFile = str(Path(f"{path}/{f}").absolute())
                    selectedCMD = [startFile]
                if f[0:16] == "server-installer":
                    remove(f"{path}/{f}")
        return [startFile, selectedCMD]

    except Exception as e:
        print("[ERROR] Version not found or other error occurred.")
        print(e)