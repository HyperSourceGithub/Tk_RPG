# tkinter imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# secrets!
import pickle
import hmac
import secrets

# misc misc
import random
import os

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
settings_window = None
status = None

# ===============================================================================
# funkshins and calsses (put into an if true to collapse in vscode)
if True:
    
    # ---------------------------------------------------------------
    # CASH OPS
    def cashplus():
        global money
        money += 10
        money_label.config(text=f"Money: ${money}")
        
    def updatecash():
        global money
        money_label.config(text=f"Money: ${money}")
        root.update()

    # ---------------------------------------------------------------
    # INVENTORY
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
    
    # INVENTORY SCRAP
    def scrap_item(index):
        global money
        item = inventory.pop(index)
        money += 50
        money_label.config(text=f"Money: ${money}")
        show_inventory()  # Refresh inventory window
    
    # ---------------------------------------------------------------
    # EXIT
    def exit_game():
        cancel = messagebox.showinfo(title="Quitting...", message="Quitting game...", type="okcancel")
        if cancel == "ok":
            root.destroy()
            exit()
        else:
            pass   
    
    # ---------------------------------------------------------------
    # SETTINGS
    def show_settings():
        global settings_window

        if settings_window is None or not settings_window.winfo_exists():
            settings_window = Toplevel(root)
            settings_window.title("Settings")
            settings_window.geometry("400x300")
            settings_window.transient(root)  # Make the new window a transient of the root window
            settings_window.grab_set()  # Grab all events for the new window

        lbl = Label(settings_window, text="⚙️ Settings:")
        lbl.grid(row=0, column=0, columnspan=6, pady=10)
        
        save_button = ttk.Button(settings_window, text="Save Game", command=save)
        save_button.grid(column=0, row=1, pady=5, columnspan=6)

        load_button = ttk.Button(settings_window, text="Load Game", command=load)
        load_button.grid(column=0, row=2, pady=5, columnspan=6)

        quit_button = ttk.Button(settings_window, text="Quit", command=exit_game)
        quit_button.grid(column=0, row=3, pady=5, columnspan=6)
        
        update_grid(settings_window)

    # ---------------------------------------------------------------
    # SAVES
    def save_game(data, filename, key):
        # Serialize the data
        serialized_data = pickle.dumps(data)

        # Create an HMAC for the data
        hmac_obj = hmac.new(key, serialized_data, digestmod='sha256')
        digest = hmac_obj.digest()

        # Store the serialized data and the HMAC together
        with open(filename, 'wb') as file:
            file.write(digest)  # Write the HMAC first
            file.write(serialized_data)  # Then the actual data
        messagebox.showinfo(title="Saved!", message="Saved game.", type='ok')
      
    def save():
        save_data = {
            'money': 500,
            'health': 100,
            'inventory': ["sword", "apple", "heal juice", "glock 19"]
        }
        global key
        key = secrets.token_bytes(32)  # Generate a strong random key
        save_game(save_data, 'saves.p', key)          

    # ---------------------------------------------------------------
    # LOADS
    
    def load_game(filename, key):
        with open(filename, 'rb') as file:
            # Read the HMAC and serialized data
            stored_hmac = file.read(32)  # Assuming the HMAC is 32 bytes long (sha256)
            serialized_data = file.read()

            # Verify the HMAC
            hmac_obj = hmac.new(key, serialized_data, digestmod='sha256')
            if not hmac.compare_digest(stored_hmac, hmac_obj.digest()):
                raise ValueError("Data has been tampered with or the key is incorrect!")
            else:
                messagebox.showinfo(title="Success!", message="Loaded sucessfully.", type='ok')

            # Deserialize the data
            return pickle.loads(serialized_data)
    
    def load():
        try:
            loaded_data = load_game('saves.p', key)
            print(loaded_data)
        except ValueError as e:
            messagebox.showinfo(title="Error!", message=f"An error occured: {e}", type='ok')
    
    # ---------------------------------------------------------------
    # FILE CHECKS
    def check_file(filename):
        result = None
        # Check if the file exists
        if not os.path.exists(filename):
            result = "NF"
            return result
        
        # Check if the file is empty
        if os.stat(filename).st_size == 0:
            result = "E"
            return result
        
        result = "NE"
        return result
    
    # ---------------------------------------------------------------
    # SCREEN UPDATES    
    def update_grid(frame):
        for col in range(6):
            frame.columnconfigure(col, weight=1)
        for row in range(10):
            frame.rowconfigure(row, weight=1)
            
    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------------
    # TOOLTIPS
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
    
    # ---------------------------------------------------------------
    # INIT         
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
begin_label = ttk.Label(frm, text="initializing...")
begin_label.grid(column=0, row=4, columnspan=10)

update_grid(frm)
root.update()

root.after(800) # add a delay

# init
clear_screen()
root.update()
init_frame()

# ===============================================================================
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
money_label.grid(column=0, row=0, sticky=(W, N))
Tooltip(money_label, "Amount of moolah you currently have. Spend it wisely.")

health_label = ttk.Label(frm, text=f"Health: {health} HP")
health_label.grid(column=6, row=0, sticky=(E, N))#, padx=(0,10))
Tooltip(health_label, "Amount of HP you currently have. Reaching 0 means death.")

# add_button = ttk.Button(frm, text="Add Money ($10)", command=cashplus)
# add_button.grid(column=1, row=2, pady=5)

inventory_button = ttk.Button(frm, text="Show Inventory", command=show_inventory)
inventory_button.grid(column=6, row=9, sticky=(E, S))

# ===============================================================================
# save/load/quit buutooons
settings_button = ttk.Button(frm, text="⚙️", command=show_settings, width=2)
settings_button.grid(column=0, row=9, sticky=(W, S))

# ===============================================================================

# frame grid make biggaer also!
update_grid(frm)

check = check_file('saves.p')
print(check)
if check == "NE":
    # Load game data if available
    loadchoice = messagebox.showinfo(icon="question", title="Load game?", message="Would you like to load your save data? (Cancel to quit)", type='yesnocancel')
    if loadchoice == "yes":
        load()
    elif loadchoice == "no":
        messagebox.showinfo(title="Info", message="Did not load game.", type="ok")
    elif loadchoice == "cancel":
        exit_game()
elif check != "NE":
    messagebox.showinfo(title="Save")

root.mainloop()