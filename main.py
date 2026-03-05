# Imports
import os

# Main
print("MinecraftTogether | V3.0.0-dev\nType \"help\" to get started.")

while True:
    command = input("\n> ").split(" ")
    
    match command[0]:
        case "help":
            print("\nHelp!")
            print("Commands are argument-based, <insert> means its required and (insert) means its optional")
            print("help | Brings up this menu.")
            print("clear | Clears the text output.")
            print("exit | Closes the program.")
        case "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        case "exit":
            break
    