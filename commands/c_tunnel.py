# c_tunnel.py
# Allows the user to select a tunneling binary or a start script to run, optionally disabling or enabling running it on server start

# Imports
from tkinter import filedialog
from commands.deps import data_interface

# Functions
def add():
    file = filedialog.askopenfilename(title="Select the file that starts your tunneler.")
    data_interface.set_value("tunneler", {
        "path": file,
        "disabled": False
    })
    print("\n[SUCCESS] Tunneler set and enabled.")

def remove():
    if data_interface.get_value("tunneler")["path"] == None:
        print("[ERROR] No tunneler to remove.")
        return

    data_interface.set_value("tunneler", {
        "path": None,
        "disabled": True
    })
    print("[SUCCESS] Tunneler removed.")

def toggle():
    path = data_interface.get_value("tunneler")["path"]
    disabled = data_interface.get_value("tunneler")["disabled"]
    if path != None:
        data_interface.set_value("tunneler", {
            "path": path,
            "disabled": not disabled
        })
        print(f"[SUCCESS] Set tunneler to {"DISABLED" if not disabled else "ENABLED"}.") # disabled variable is still old value, hence the not
    else:
        print(f"[ERROR] Tunneler not found, maybe one hasn't been added yet?")

def list():
    tunneler = data_interface.get_value("tunneler")
    print("\n[Tunnel Information]")
    print(f"Path: ({"None, tunneler not found." if tunneler["path"] == None else tunneler["path"]})")
    print(f"Disabled: {"True" if tunneler["disabled"] else "False"}")