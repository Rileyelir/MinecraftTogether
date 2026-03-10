# c_small.py
# Command module dedicated for smaller snippets of code that don't warrant their own file.

# Imports
import os

def help(command: str):
    match command:
        case "manager":
            print("\nAccepted subcommands:")
            print("manager list")
        case _:
            print("\nCommands are argument-based, <insert> means its required and (insert) means its optional")
            print("manager <subcommand> (server-name) | Accesses a function of the server manager.")
            print("create | Begins the server creation process.")
            print("help (command) | Brings up this menu or extra help about a specific command.")
            print("clear | Clears the text output.")
            print("exit | Closes the program.")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')