# file to test tooltips
from tkinter import *

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

        label = Label(self.tip_window, text=self.text, background="blue", relief=SOLID, borderwidth=1, font=("Arial", 15, "normal"))
        label.pack()

    def hide_tip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

root = Tk()
root.geometry("300x200")

label = Label(root, text="Hover over me!", font=("Helvetica", 14))
label.pack(pady=20)

# Add a tooltip to the label
Tooltip(label, "This is a tooltip!")

root.mainloop()
