# -*- coding: utf-8 -*-

import json
import os
from core.hero import *
from core.tree import *
from core.star import *
from core.enemy import *

LEVELS_DIR = os.path.join(os.path.dirname(__file__), "..", "levels")

# LevelGenerator - builds the game environment for a level from its
# universal data source (levels/level{num}.json). No per-level branches:
# every level is described by the same schema of start / roads / trees /
# stars / enemies, so adding a level is just adding a JSON file.
class LevelGenerator():
    def __init__(self, num, world):
        self.num, self.screen = num, world.screen
        self.data = self._load(num)

    @staticmethod
    def _path(num):
        return os.path.join(LEVELS_DIR, "level{}.json".format(num))

    @classmethod
    def _load(cls, num):
        with open(cls._path(num)) as f:
            return json.load(f)

    @classmethod
    def level_exists(cls, num):
        return os.path.isfile(cls._path(num))

    def start_point(self):
        return tuple(self.data["start"])

    # Walkable corridors, each as [x_min, y_min, x_max, y_max] of the hero's
    # allowed top-left position. Movement logic checks membership against these.
    @property
    def roads(self):
        return self.data["roads"]

    def generate_trees(self):
        return [Tree(self.screen, x, y) for x, y in self.data["trees"]]

    def generate_stars(self):
        return [Star(self.screen, x, y) for x, y in self.data["stars"]]

    def generate_enemies(self):
        return [
            Enemy(self.screen, e["x"], e["y"], e["face"], e.get("patrol", 68))
            for e in self.data["enemies"]
        ]
