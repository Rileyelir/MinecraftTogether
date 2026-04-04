# c_manager.py
# Allows display and management of the server list along with starting servers.

# Imports
import subprocess
import shutil
from pathlib import Path
from commands.deps import data_interface
from tkinter import filedialog
from platform import system as currentOS
import os

# Class & Functions
def list():
    print("\n[Server List]")
    for serv in data_interface.get_value("servers"):
        print(f"{serv["name"]} ({serv["path"]})")

# Function that runs automatically on startup of main.py to clean up broken server paths
def clear_missing_servers():
    for serv in data_interface.get_value("servers"):
        try:
            with open(serv["path"], "r") as file:
                pass
        except FileNotFoundError:
            data_interface.remove_server(serv["name"])

def get_java_path():
    system_java = shutil.which("java")
    if system_java:
        return system_java
    return None

# Add server to list
def add():
    jar = filedialog.askopenfilename(title="Select the server's start file.")
    name = input("Server Name: ")
    maxRam = input("Server Ram Limit (gb): ")

    # Specify Java version check
    print("\nDo you want to specify a version of Java to use? (y/N)")
    print("This is only required for servers that don't specifically work with the Java version found in your PATH. Select no if this doesn't apply to you.")
    print("If you are running a modern Forge server (1.17+), you will have to add the path to the jvm arguments in the server files manually for now.")
    javaChoice = input("? ")
    specJava = "java"
    if javaChoice.lower() == "y":
        specJava = filedialog.askopenfilename(title="Select the executable for the specified Java version.")
        print("[SUCCESS] Java version set for this server.")

    cmd = []
    if jar.endswith(".jar"):
        cmd = [
            specJava, 
            f"-Xmx{maxRam}G",
            f"-Xms{maxRam}G", 
            "-jar",
            jar,
            "--nogui"
        ]
    else:
        cmd = [jar]

    data_interface.add_server(name, jar, maxRam, cmd)
    print(f"\n[SUCCESS] Added server {name} to list.")

# Remove server from list
def remove(serverName: str):
    data_interface.remove_server(serverName)

class Server: # might want to split this into a different file at some point
    def __init__(self):
        self.process = None
        self.currentServer = None

    def start(self, name: str):
        self.currentServer = data_interface.get_server(name)

        if not self.currentServer:
            print("[ERROR] Server not found.")
            return
        
        if self.process:
            print("[ERROR] There is a a server already active.")
            return

        java_exe = get_java_path()
        if not java_exe:
            print("[ERROR] Java not found. Please install Java and link it to your global PATH.")
            return
        jar_full_path = Path(self.currentServer["path"])
        ram = self.currentServer["ram"]
        server_dir = jar_full_path.parent 

        cmd = self.currentServer["cmd"]

        self.process = subprocess.Popen(
            cmd,
            cwd=str(server_dir),
            #stdin=subprocess.PIPE,
            #stdout=subprocess.DEVNULL,
            text=True,
        )

        if not data_interface.get_value("tunneler")["disabled"]:
            system = currentOS()
            filePath = data_interface.get_value("tunneler")["path"]
            if system == "Windows":
                os.startfile(filePath)
            elif system == "Darwin": # macOS
                os.system(f"open {filePath}") # needs to be tested (but how?)
            else: # Linux
                os.system(f"xdg-open {filePath}") # needs to be tested

        print(f"[SUCCESS] Server {name} is starting!")
        self.process.wait() # Stop all code until server closes
        print("\n[NOTICE] Server closed, re-entering MinecraftTogether...")

serverInstance = Server()