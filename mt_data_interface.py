# mt_data_interface.py
# Handles setting and getting information from a generated json file called mt_data.json, for data like server info, preferred tunneler locations, and other persistent data.

# Imports
import json

# Functions
def set_json(data):
    with open("mt_data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_json():
    with open("mt_data.json", "r") as file:
        return json.load(file)

def init_json():
    set_json({
        "servers": [],
        "tunneler": None
    })
    
def set_value(key: str, value):
    new = get_json()
    new[key] = value
    set_json(new)

def get_value(key: str):
    return get_json()[key]

def add_server(name: str, path: str): # path is the path to the start file, not the folder
    serverList = get_value("servers")
    
    for sv in serverList: # same name check, no repeated server names
        if sv["name"] == name:
            return

    new = get_value("servers")
    new.append({
        "name": name,
        "path": path
    })
    set_value("servers", new)

def get_server(name: str):
    for sv in get_value("servers"):
        if sv["name"] == name:
            return sv

def remove_server(name: str, all: bool = False):
    if all:
        set_value("servers", [])
    else:
        serverList = get_value("servers")
        for sv in serverList:
            if sv["name"] == name:
                serverList.remove(sv)
        set_value("servers", serverList)

# Testing Code (ran when running json_handler.py separately)
print(get_json())