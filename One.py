import math
import tkinter as tk

top = tk.Tk()


canvas = tk.Canvas(top, bg='black', height=600, width=600)
canvas.pack()


DELAY = 100
CIRCULAR_PATH_INCR = 10

sin = lambda degs: math.sin(math.radians(degs))
cos = lambda degs: math.cos(math.radians(degs))


class Celestial(object):
    COS_0, COS_180 = cos(0), cos(180)
    SIN_90, SIN_270 = sin(90), sin(270)

    def __init__(self, x, y, radius):
        self.x, self.y = x, y
        self.radius = radius

    def bounds(self):
        return (self.x + self.radius*self.COS_0,   self.y + self.radius*self.SIN_270,
                self.x + self.radius*self.COS_180, self.y + self.radius*self.SIN_90)


def circular_path(x, y, radius, delta_ang, start_ang=0):
    ang = start_ang % 360
    while True:
        yield x + radius*cos(ang), y + radius*sin(ang)
        ang = (ang+delta_ang) % 360


def update_position(canvas, id, celestial_obj, path_iter):
    celestial_obj.x, celestial_obj.y = next(path_iter)
    x0, y0, x1, y1 = canvas.coords(id)
    oldx, oldy = (x0+x1) // 2, (y0+y1) // 2
    dx, dy = celestial_obj.x - oldx, celestial_obj.y - oldy
    canvas.move(id, dx, dy)
    canvas.after(DELAY, update_position, canvas, id, celestial_obj, path_iter)


sol_obj = Celestial(300, 300, 25)
planet_obj1 = Celestial(250+100, 250, 15)
sol = canvas.create_oval(sol_obj.bounds(), fill='white', width=0)
planet1 = canvas.create_oval(planet_obj1.bounds(), fill='blue', width=0)

orbital_radius = math.hypot(sol_obj.x - planet_obj1.x, sol_obj.y - planet_obj1.y)
path_iter = circular_path(sol_obj.x, sol_obj.y, orbital_radius, CIRCULAR_PATH_INCR)
next(path_iter)

top.after(DELAY, update_position, canvas, planet1, planet_obj1, path_iter)
top.mainloop()