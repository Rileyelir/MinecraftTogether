# main.py
# Links everything together by receiving and parsing user input

# Imports
from commands import *

# Main
print("MinecraftTogether | V3.0.0\nType \"help\" to get started.")

c_manager.clear_missing_servers()

while True:
    command = input("\n> ").split(" ")
    lastArg = " ".join(command[2:])

    try:
        match command[0]:
            case "manager":
                match command[1]:
                    case "list":
                        c_manager.list()
                    case "start":
                        c_manager.serverInstance.start(lastArg)
                    case "add":
                        c_manager.add()
                    case "remove":
                        c_manager.remove(lastArg)
            case "tunnel":
                match command[1]:
                    case "add":
                        c_tunnel.add()
                    case "remove":
                        c_tunnel.remove()
                    case "toggle":
                        c_tunnel.toggle()
                    case "list":
                        c_tunnel.list()
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