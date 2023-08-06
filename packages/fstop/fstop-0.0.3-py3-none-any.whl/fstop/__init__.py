from .engine import *
from .pak import *


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 0:
        map = Map(sys.argv[1])
        screen = Screen(map.config["vsize"], [1600, 900], map.config['icon'], 'FStop', '.')
        screen.load(map)
        screen.mainloop()
    else:
        map = Map('test.map')  # sys.argv[1])
        screen = Screen(map.config["vsize"], [1600, 900], map.config['icon'], 'FStop', '.')
        screen.load(map)
        screen.mainloop()
