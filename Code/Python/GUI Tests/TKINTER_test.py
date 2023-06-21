import tkinter as tk

#print(tkinter.TkVersion)
#print(tkinter.TclVersion)
#tkinter._test()

root = tk.Tk()
root.title("Generator")
root.geometry('640x480+8+50')
#label = tk.Label(root, text="TEST", bg="gold", fg="blue", font="Arial 24").pack()
label = tk.Label(root, text="Hello World")
label.pack(side='top')

leftFrame = tk.Frame(root)
leftFrame.pack(side='left', anchor='n', fill=tk.Y, expand=False)

canvas = tk.Canvas(root, relief='raised', borderwidth=1)
canvas.pack(side='left', anchor='n')

rightFrame=tk.Frame(root)
rightFrame.pack(side='right', anchor='n', expand=True)

button1 = tk.Button(rightFrame, text="Button1")
button2 = tk.Button(rightFrame, text="Button2")
button3 = tk.Button(rightFrame, text="Button3")
button1.pack(side='top')
button2.pack(side='top')
button3.pack(side='top')

root.mainloop()