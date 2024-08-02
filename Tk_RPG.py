from tkinter import *
from tkinter import ttk

# vareeabulls
money = 0
inventory = ["sword", "apple", "flask of some random juice I found in the science lab", "glock 19"]
inventory_window = None

# funkshins
def cashplus():
    global money
    money += 10
    money_label.config(text=f"Money: ${money}")

def show_inventory():
    global inventory_window

    if inventory_window is None or not inventory_window.winfo_exists():
        inventory_window = Toplevel(root)
        inventory_window.title("Inventory")
        inventory_window.geometry("400x300")
        inventory_window.transient(root)  # Make the new window a transient of the root window
        inventory_window.grab_set()  # Grab all events for the new window

    # Clear previous contents
    for widget in inventory_window.winfo_children():
        widget.destroy()

    lbl = Label(inventory_window, text="Inventory:")
    lbl.grid(row=0, column=0, columnspan=2, pady=10)

    for index, item in enumerate(inventory):
        item_label = Label(inventory_window, text=f"• {item}")
        item_label.grid(row=index + 1, column=0, sticky="w")
        scrap_button = Button(inventory_window, text="Scrap", command=lambda i=index: scrap_item(i))
        scrap_button.grid(row=index + 1, column=1)

def scrap_item(index):
    global money
    item = inventory.pop(index)
    money += 50
    money_label.config(text=f"Money: ${money}")
    show_inventory()  # Refresh inventory window

def save_game():
    with open("saves.txt", "w") as file:
        file.write(f"{money}\n")
        for item in inventory:
            file.write(f"{item}\n")

def load_game():
    global money, inventory
    try:
        with open("saves.txt", "r") as file:
            lines = file.readlines()
            money = int(lines[0].strip())
            inventory = [line.strip() for line in lines[1:]]
        money_label.config(text=f"Money: ${money}")
    except FileNotFoundError:
        print("Save file not found. Starting with default values.")
    except Exception:
        print("No save data found. Continuing as regular and resetting data...")

# deefien root
root = Tk()
root.geometry("450x300")

# fraem
frm = ttk.Frame(root, padding=10)
frm.grid(sticky=(N, S, E, W))

# root grid make itself BIGGER :O
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# fraem titel
frm.master.title("Tk_RPG")

# labeels buutooons and other stuffs
title_label = ttk.Label(frm, text="tk_rpg: a simple rpg")
title_label.grid(column=0, row=0, columnspan=3, pady=5)

money_label = ttk.Label(frm, text=f"Money: ${money}")
money_label.grid(column=1, row=1, pady=5)

add_button = ttk.Button(frm, text="Add Money ($10)", command=cashplus)
add_button.grid(column=1, row=2, pady=5)

inventory_button = ttk.Button(frm, text="Show Inventory", command=show_inventory)
inventory_button.grid(column=1, row=3, pady=10)

save_button = ttk.Button(frm, text="Save Game", command=save_game)
save_button.grid(column=1, row=4, pady=10)

load_button = ttk.Button(frm, text="Load Game", command=load_game)
load_button.grid(column=1, row=5, pady=10)

quit_button = ttk.Button(frm, text="Quit", command=root.destroy)
quit_button.grid(column=1, row=6, pady=5)

# frame grid make biggaer also!
frm.columnconfigure(0, weight=1)
frm.columnconfigure(1, weight=1)
frm.columnconfigure(2, weight=1)
for row in range(0, 10):
    frm.rowconfigure(row, weight=1)

# Load game data if available
load_game()

root.mainloop()
