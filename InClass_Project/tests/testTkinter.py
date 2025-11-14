import tkinter as tk

root = tk.Tk()

def on_button_click():
    print('explorer opened')

button = tk.Button(root, text="Upload Resume", command=on_button_click)


root.mainloop()

