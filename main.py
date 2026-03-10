# main.py
# Links everything together by receiving and parsing user input

# Imports
from commands import *

# Main
print("MinecraftTogether | V3.0.0-dev\nType \"help\" to get started.")

while True:
    command = input("\n> ").split(" ")
    try:
        match command[0]:
            case "manager":
                match command[1]:
                    case "list":
                        c_manager.list()
                    case "start":
                        c_manager.serverInstance.start(command[2])
                    case "stop":
                        c_manager.serverInstance.stop()
            case "create":
                c_creator.create_server()
            case "help":
                c = None
                if len(command) > 1: c = command[1]
                c_small.help(c)
            case "clear":
                c_small.clear()
            case "exit":
                break
    except IndexError:
        print("Provided command has insufficient arguments.")