import Tkinter
main = Tk()

def leftKey(event):
    print ("Left key pressed")

def rightKey(event):
    print ("Right key pressed")

def upKey(event):
    print ("Up key pressed")

def downKey(event):
    print ("Down key pressed")

frame = Frame(main, width=640, height=480)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
main.bind('<Up>', upKey)
main.bind('<Down>', downKey)
frame.pack()
main.mainloop()
