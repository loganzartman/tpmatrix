from termpixels import App, Color
from random import uniform, randint 
import sys
import argparse

def randchar():
    return chr(randint(0xFF00, 0xFFEF))

SPEED_MIN = 0.5
SPEED_MAX = 2
LENGTH_MIN = 3
LENGTH_MAX = 8
HUE = 0.3*360

class Particle:
    def __init__(self):
        self.pos = 0
        self.speed = uniform(SPEED_MIN, SPEED_MAX)
        self.length = uniform(LENGTH_MIN, LENGTH_MAX)

class MatrixApp(App):
    def on_start(self):
        self.on_resize()
    
    def on_resize(self):
        self.cols = [Particle() for x in range(self.screen.w // 2)]

    def on_frame(self):
        for x, p in enumerate(self.cols):
            px = x * 2
            for i in range(int(p.length) + 1):
                col = Color.hsl(HUE/360,1,1 - i/p.length)
                self.screen.at(px, int(p.pos - i), clip=True).fg = col
            for i in range(int(p.speed) + 1):
                pos = p.pos + i
                self.screen.print(" ", px, int(pos - p.length))
                self.screen.print(randchar(), px, int(pos), fg=col)
            p.pos += p.speed
            if p.pos - p.length >= self.screen.h:
                self.cols[x] = Particle()
        self.screen.update()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The best Matrix text rain for terminals")
    parser.add_argument("--speed-min", "-s", type=float, nargs="?", default=SPEED_MIN, help="Minimum rain speed")
    parser.add_argument("--speed-max", "-S", type=float, nargs="?", default=SPEED_MAX, help="Maximum rain speed")
    parser.add_argument("--length-min", "-l", type=float, nargs="?", default=LENGTH_MIN, help="Minimum raindrop length")
    parser.add_argument("--length-max", "-L", type=float, nargs="?", default=LENGTH_MAX, help="Maximum raindrop length")
    parser.add_argument("--hue", "-H", type=float, nargs="?", default=HUE, help="Color hue (0 to 360)")
    ns = parser.parse_args(sys.argv[1:])
    SPEED_MIN = ns.speed_min
    SPEED_MAX = ns.speed_max
    LENGTH_MIN = ns.length_min
    LENGTH_MAX = ns.length_max
    HUE = ns.hue
    MatrixApp().start()

