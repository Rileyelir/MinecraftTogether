# main.py
# Links everything together by receiving and parsing user input

# Imports
from commands import *

# Main
# we should totally be checking servers if they're there on startup and auto-delete missing server entries
print("MinecraftTogether | V3.0.0-dev\nType \"help\" to get started.")

while True:
    command = input("\n> ").split(" ")
    match command[0]:
        case "help":
            c_small.help()
        case "clear":
            c_small.clear()
        case "exit":
            break
    