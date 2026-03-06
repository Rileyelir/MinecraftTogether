# main.py
# Links everything together by receiving and parsing user input

# Imports
from commands import *

# Main
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
    