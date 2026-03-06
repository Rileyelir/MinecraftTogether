# c_small.py
# Command module dedicated for smaller snippets of code that don't warrant their own file.

# Imports
import os

def help():
    print("\nHelp!")
    print("Commands are argument-based, <insert> means its required and (insert) means its optional")
    print("help | Brings up this menu.")
    print("clear | Clears the text output.")
    print("exit | Closes the program.")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')