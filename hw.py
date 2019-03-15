from graphics import *
def main():

    win = GraphWin("Mario", 640, 480)
    c = Image(Point(0,240),("E:\Users\David\Documents\python\Mario.gif")
    c.draw(win)


    
    for x in range (1, 640):
        c.move(1,0)
        time.sleep(.05)
    
main()
