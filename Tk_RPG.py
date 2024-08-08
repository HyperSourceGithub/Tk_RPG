from tkinter import *
from tkinter import ttk
import random

# vareeabulls
money = 500
health = 100

inventory = ["sword", 
             "apple", 
             "heal juice", 
             "glock 19"]
title_messages = ["The RPG of the century!", 
                  "Eaten Fresh!", 
                  "Crispy!", 
                  "I smell smoke!", 
                  "oo look a TITLE!!", 
                  "{Undefined null String;}"]



inventory_window = None
status = None

# ===============================================================================
# funkshins and calsses (put into an if true to collapse in vscode)
if True:
    def cashplus():
        global money
        money += 10
        money_label.config(text=f"Money: ${money}")
        
    def updatecash():
        global money
        money_label.config(text=f"Money: ${money}")
        root.update()

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
        global money, inventory, health
        try:
            with open("saves.txt", "r") as file:
                lines = file.readlines()
                money = int(lines[0].strip())
                health = int(lines[1].strip())
                inventory = [line.strip() for line in lines[2:]]
            money_label.config(text=f"Money: ${money}")
            health_label.config(text=f"Health: {health} HP")
        except FileNotFoundError:
            print("Save file not found. Starting with default values.")
        except Exception:
            print("No save data found. Continuing as regular and resetting data...")
            
    def update_grid():
        for col in range(6):
            frm.columnconfigure(col, weight=1)
        for row in range(10):
            frm.rowconfigure(row, weight=1)
            
    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    class Tooltip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tip_window = None
            self.widget.bind("<Enter>", self.show_tip)
            self.widget.bind("<Leave>", self.hide_tip)

        def show_tip(self, event):
            x, y, _cx, _cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25

            self.tip_window = Toplevel(self.widget)
            self.tip_window.wm_overrideredirect(True)
            self.tip_window.wm_geometry(f"+{x}+{y}")

            label = Label(self.tip_window, text=self.text, relief=SOLID, borderwidth=0, padx=5, pady=5, font=("Arial", 10, "normal"))
            label.pack()

        def hide_tip(self, event):
            if self.tip_window:
                self.tip_window.destroy()
                self.tip_window = None
                
    def init_frame():
        global frm
        frm = ttk.Frame(root, padding=10)
        frm.grid(sticky=(N, S, E, W))

# ===============================================================================

# deefien root
root = Tk()
root.geometry("750x450")

# fraem
init_frame()

# root grid make itself BIGGER :O
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# fraem titel
frm.master.title(f"Tk_RPG: {random.choice(title_messages)}")

# ===============================================================================
status = 'begin'
begin_label = ttk.Label(frm, text="Hello, World!")
begin_label.grid(column=0, row=4, columnspan=10)
update_grid()
root.update()
root.after(3000)
clear_screen()
root.update()
init_frame()

status = 'run'
if status == 'run':
    pass
else:
    print("fatal error! a chunk of code has been skipped! exiting game...")
    exit()
# labeels buutooons and other stuffs
#title_label = ttk.Label(frm, text="tk_rpg: a simple rpg")
#title_label.grid(column=1, row=0, columnspan=3, pady=3)

money_label = ttk.Label(frm, text=f"Money: ${money}")
money_label.grid(column=0, row=0, pady=3, sticky=(W))
Tooltip(money_label, "Amount of moolah you currently have. Spend it wisely.")

health_label = ttk.Label(frm, text=f"Health: {health} HP")
health_label.grid(column=6, row=0, pady=3, sticky=(E))#, padx=(0,10))
Tooltip(health_label, "Amount of HP you currently have. Reaching 0 means death.")

# add_button = ttk.Button(frm, text="Add Money ($10)", command=cashplus)
# add_button.grid(column=1, row=2, pady=5)

inventory_button = ttk.Button(frm, text="Show Inventory", command=show_inventory)
inventory_button.grid(column=0, row=3, pady=10, sticky=(W))

# ===============================================================================
# save/load/quit buutooons

save_button = ttk.Button(frm, text="Save Game", command=save_game)
save_button.grid(column=0, row=8, pady=5, sticky=(W))

load_button = ttk.Button(frm, text="Load Game", command=load_game)
load_button.grid(column=6, row=8, pady=5, sticky=(E))

quit_button = ttk.Button(frm, text="Quit", command=root.destroy)
quit_button.grid(column=0, row=8, pady=5, columnspan=10)

# ===============================================================================

# frame grid make biggaer also!
update_grid()

# Load game data if available
load_game()

root.mainloop()