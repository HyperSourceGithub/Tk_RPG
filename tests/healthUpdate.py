# file to test updating
from tkinter import *

health = 100
def hit():
    global health
    if health <= 10:
        print("Dead!")
        quit()
    else:
        health -= 10
    label.config(text=f"Health: {health}")
    label.pack()


root = Tk()
root.geometry("300x200")

label = Label(root, text=f"Health: {health}", font=("Helvetica", 14))
label.pack()

button = Button(root, text="-10 HP", command=hit)
button.pack()

root.mainloop()
