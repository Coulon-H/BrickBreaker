from tkinter import *


class Brick(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item


class Tableau(Canvas):

    def __init__(self, hw, th):
        x, y, n = 5, 10, 0
        Canvas.__init__(self, bg="lightyellow", width=hw, height=th)
        self.bar = self.create_rectangle(x1, y1, x1 + 70, y1 + 10, fill='lightgreen')
        self.ball = self.create_oval(x2, y2, x2 + 20, y2 + 20, fill='red')
        self.container = {}
        for j in range(0, 3):
            for i in range(0, 5):
                rect = Brick(Tableau, self.create_rectangle(x, y, x + 137, y + 10, fill='orange'))
                x += 138
                self.container[rect.item] = rect
                n += 1
            n += 1
            x = 5
            y += 10
        self.ckeck = []
        self.left = self.bind_all('<Left>', self.deplg)
        self.right = self.bind_all('<Right>', self.depld)
        self.start = self.bind_all('<Return>', self.start)
        self.stop = self.bind_all('<space>', self.stop)
        self.pack()

    def avance(self, horiz, vertic):  # fonction de déplacement
        global x1, y1, windows
        x1, y1 = x1 + horiz, y1 + vertic
        self.coords(self.bar, x1, y1, x1 + 70, y1 + 10)

    def deplg(self, event):   # gauche
        self.avance(-10, 0)

    def depld(self, event):   # droite
        self.avance(10, 0)

    def deplball(self):       # mouvement de la balle
        global h, t, x2, y2, dx, dy, l
        coords = self.coords(self.bar)
        if x2 <= 0:
            dx *= -1
        if (x2 + 20) >= h:
            dx *= -1
        if y2 == 0:
            dy *= -1
        x2, y2 = x2 + dx, y2 + dy
        self.coords(self.ball, x2, y2, x2 + 20, y2 + 20)
        #print(x2, dx, self.container)

        self.check_collisions()
        if len(self.find_overlapping(coords[0], coords[1], coords[2], coords[3])) > 1:  # collision avec la barre
            dy *= -1

        if l > 0:
            self.after(100, self.deplball)
        if y2 > y1 + 10:
            l = 0

    def check_collisions(self):
        ball_coords = self.coords(self.ball)
        items = self.find_overlapping(*ball_coords)
        objects = [self.container[x] for x in items if x in self.container]
        self.collide(objects)

    def collide(self, k):
        global dx, dy
        print(k)
        c = self.coords(self.ball)
        x = (c[0] + c[2]) * 0.5
        if len(k) > 1:
            dy *= -1
        elif len(k) == 1:
            game_object = k[0]
            print(game_object)
            coords = self.coords(game_object.item)
            print(coords)
            if x > coords[2]:
                dx *= 1
            elif x < coords[0]:
                dx *= -1
            else:
                dy *= -1
            self.delete(game_object.item)

    def start(self, event):
        global l
        l += 1
        if l == 1:
            self.deplball()

    def stop(self, event):
        global l
        l = 0


class Windows(Tk):
    def __init__(self, hw, th):
        Tk.__init__(self)
        self.title("BrickBreaker")

        self.configure(bg="blue")
        self.Can = Tableau(hw, th)
        self.mainloop()


l = 0
h = 700
t = 500
x1, y1 = h - 370, t - 50     # coordonnées du rectangle
x2, y2 = x1 + 20, y1 - 20   # coordonnées du cercle
dx, dy = -10, -10            # déplacement horizontale, déplacement verticale
windows = Windows(h, t)

