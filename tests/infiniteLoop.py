from tkinter import *

count = 0

def update_count():
    global count
    count += 1
    label.config(text=f"Count: {count}")
    root.after(1000, update_count)  # Schedule this function to be called again after 1000 milliseconds (1 second)

root = Tk()
root.geometry("300x200")

label = Label(root, text=f"Count: {count}", font=("Helvetica", 14))
label.pack()

# Start the update loop
root.after(1000, update_count)  # Call update_count after 1000 milliseconds (1 second)

root.mainloop()
