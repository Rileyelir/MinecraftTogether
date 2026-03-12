# c_manager.py
# Handles the management of servers, being an intermediary between user input and mt_data.json alongside controlling server states and auto-launching tunneling software.

# Imports
import subprocess
import threading
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

def add():
    jar = filedialog.askopenfilename(title="Select the server's jar file.", filetypes=(("Server Jar", "*.jar"),))
    name = input("Server Name: ")
    maxRam = input("Server Ram Limit (gb): ")
    data_interface.add_server(name, jar, maxRam)
    print(f"\n[SUCCESS] Added server {name} to list.")

def remove(serverName: str):
    data_interface.remove_server(serverName)

class Server: # might want to split this into a different file at some point in the near future
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

        def run():
            java_exe = get_java_path()
            if not java_exe:
                print("[ERROR] Java not found. Please install Java and link it to your global PATH.")
                return
            jar_full_path = Path(self.currentServer["path"])
            ram = self.currentServer["ram"]
            server_dir = jar_full_path.parent 

            cmd = [
                java_exe, 
                f"-Xmx{ram}G", 
                f"-Xms{ram}G", 
                "-jar", jar_full_path.name
            ]

            self.process = subprocess.Popen(
                cmd,
                cwd=str(server_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                text=True,
            )

        threading.Thread(target=run, daemon=True).start()

        if not data_interface.get_value("tunneler")["disabled"]:
            system = currentOS()
            filePath = data_interface.get_value("tunneler")["path"]
            if system == "Windows":
                os.startfile(filePath)
            elif system == "Darwin": # macOS
                os.system(f"open {filePath}") # needs to be tested
            else: # Linux
                os.system(f"xdg-open {filePath}") # needs to be tested
        print(f"[SUCCESS] Server {name} is starting!")

    def stop(self):
        if self.process and self.process.poll() is None:
            print("Stopping server...")
            self.process.communicate(input="stop\n")
            self.process = None
        else:
            print("No server is currently running.")

serverInstance = Server()