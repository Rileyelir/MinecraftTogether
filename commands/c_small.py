# c_small.py
# Command module dedicated for smaller snippets of code that don't warrant their own file. Maybeee help should have its own file, but oh well.

# Imports
from os import system, name

def help(command: str): # yes i know it shouldn't be 5 million print statements but it works fine and i like it :)
    match command:
        case "manager":
            print("\n[Help: manager]")
            print("Accepted subcommands:")
            print("----------------------------")
            print("manager list | Lists all usable servers.")
            print("manager start <server-name> | Starts the server specified in the argument.")
            print("manager add | Adds a new server to the list.")
            print("manager remove <server-name> | Removes a server from the list.")
        case "tunnel":
            print("\n[Help: tunnel]")
            print("Accepted subcommands:")
            print("----------------------------")
            print("tunnel add | Add a tunneling executable or start script and enable it for server startup.")
            print("tunnel remove | Remove currently set tunnel if one is found.")
            print("tunnel toggle | Activates/deactivates the tunnel.")
            print("tunnel list | Gives information about the tunnel.")
        case _:
            print("\n[Help]")
            print("Commands are argument-based, <insert> means its required and (insert) means its optional.")
            print("----------------------------")
            print("manager <subcommand> | Accesses a function of the server manager.")
            print("create | Begins the server creation process.")
            print("tunnel <subcommand> | Add and manage the status of your tunneling solution.")
            print("help (command) | Brings up this menu or extra help about a specific command.")
            print("clear | Clears the text output.")
            print("exit | Closes the program.")

def clear():
    system('cls' if name == 'nt' else 'clear')