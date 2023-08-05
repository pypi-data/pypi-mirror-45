FGA + Arcade
============

A very simple game engine based on the excellent
[Arcade](https://github.com/pvcraven/arcade/) library. This is an educational
game engine designed to support only very limited kind of games. The current
implementation only support platformers (e.g, Mario Bros.), but maybe it will
support other kinds games in the future.


## How does it work?

First pip install it (you will need Python 3.6+):

```shell
$ pip install fgarcade
```

The a game.py file and optionally a folder called assets. The "Platformer" class
from ``fgarcade`` implements most of the logic necessary to build a platform.
You still have to define the scenery, configure some options, and maybe add custom
logic and renderizations:

```python
# game.py

import fgarcade as ge


@ge.create_platformer('Simple game', width=800, height=600)
def game(self):
    """
    Create game and initialize the variables.
    """
    self.create_tower(10, 2, coords=(0, 1))
    self.create_ground(3, coords=(2, 3))
    self.create_ground(3, coords=(6, 1))
    self.create_platform(3, coords=(4, 5))
    self.create_platform(3, coords=(12, 4))
    self.create_ground(35, coords=(0, 0), smooth_ends=False)
    self.create_ramp('up', 6, coords=(15, 1))
    self.create_ground(5, coords=(21, 6), smooth_ends=False, height=6)
    self.create_ramp('down', 6, coords=(26, 7))
    self.create_tower(10, coords=(34, 1))


if __name__ == "__main__":
    game.run()
```