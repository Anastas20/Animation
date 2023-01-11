import tkinter as tk
from random import randint


class Rain:
    def __init__(self, canvas, x, y, speed, length, color='white'):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = length
        self.canvas = canvas
        self.line = canvas.create_line(self.x, self.y, self.x, self.y+length, fill=color)

    def move(self):
        self.y += self.speed
        self.canvas.move(self.line, 0, self.speed)

        if self.y > 500:
            self.canvas.move(self.line, 0, -(500+self.length))
            self.y -= 500 + self.length


def draw():
    for drop in drops:
        drop.move()

    root.after(10, draw)


root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500, bg='darkblue')
canvas.pack()

drops = [Rain(canvas, x=randint(0, 500), y=randint(0, 500), speed=randint(1, 3), length=randint(5, 20))
         for i in range(101)]

draw()

root.mainloop()