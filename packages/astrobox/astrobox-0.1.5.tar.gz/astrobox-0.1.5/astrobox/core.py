# -*- coding: utf-8 -*-
from __future__ import print_function

import random

from robogame_engine import GameObject
from robogame_engine.constants import ROTATE_TURNING
from robogame_engine.theme import theme
from .cargo_box import CargoBox


class AstroUnit(GameObject, CargoBox):
    pass


class Dron(AstroUnit):
    rotate_mode = ROTATE_TURNING
    radius = 44
    auto_team = True
    __my_mathership = None
    _dead = False
    layer = 2

    def __init__(self, coord=None):
        super(Dron, self).__init__(coord=coord)
        CargoBox.__init__(self, initial_cargo=0, maximum_cargo=theme.MAX_DRON_ELERIUM)
        self._objects_holder = self.scene
        self.__health = theme.MAX_HEALTH

    @property
    def sprite_filename(self):
        return 'dron_{}.png'.format(self.team)

    @property
    def my_mathership(self):
        if self.__my_mathership is None:
            try:
                self.__my_mathership = self.scene.get_mathership(team=self.team)
            except IndexError:
                raise Exception("No mathership for {} "
                                "- check matherships_count!".format(self.__class__.__name__))
        return self.__my_mathership

    @property
    def meter_1(self):
        return self.fullness

    @property
    def meter_2(self):
        return float(self.__health) / theme.MAX_HEALTH

    @property
    def is_alive(self):
        return self.__health > 0

    @property
    def drones(self):
        return self.scene.drones

    @property
    def asteroids(self):
        return self.scene.asteroids

    @property
    def matherships(self):
        return self.scene.matherships

    def game_step(self):
        super(Dron, self).game_step()
        CargoBox.game_step(self)
        if self.is_alive and self.__health < theme.MAX_HEALTH:
            self.__health += theme.HEALTH_TOP_UP_SPEED

    def on_stop_at_target(self, target):
        for asteroid in self.asteroids:
            if asteroid.near(target):
                self.on_stop_at_asteroid(asteroid)
                return
        else:
            for ship in self.matherships:
                if ship.near(target):
                    self.on_stop_at_mathership(ship)
                    return
        self.on_stop_at_point(target)

    def on_stop_at_point(self, target):
        pass

    def on_stop_at_asteroid(self, asteroid):
        pass

    def on_stop_at_mathership(self, mathership):
        pass

    def move_at(self, target, speed=None):
        if not self.is_alive:
            return
        super(Dron, self).move_at(target, speed)

    def turn_to(self, target, speed=None):
        if not self.is_alive:
            return
        super(Dron, self).turn_to(target, speed)


class Asteroid(AstroUnit):
    rotate_mode = ROTATE_TURNING
    radius = 50
    selectable = False
    counter_attrs = dict(size=16, position=(0, 0), color=(255, 255, 255))

    def __init__(self, coord, max_elerium=None):
        direction = random.randint(0, 360)
        super(Asteroid, self).__init__(coord=coord, direction=direction)
        if max_elerium is None:
            max_elerium = random.randint(theme.MIN_ASTEROID_ELERIUM, theme.MAX_ASTEROID_ELERIUM)
        self._size = (max_elerium / theme.MIN_ASTEROID_ELERIUM) * .8
        CargoBox.__init__(self, initial_cargo=max_elerium, maximum_cargo=max_elerium)
        self._sprite_num = 1
        # TODO сделать разные картинки спрайтов, одинакового размера и рандомить
        # self._sprite_num = random.randint(1, 9)

    @property
    def sprite_filename(self):
        return 'asteroids/{}.png'.format(self._sprite_num)

    @property
    def zoom(self):
        return .4 + self.fullness * .6 * self._size

    @property
    def counter(self):
        return self.payload

    def on_born(self):
        self.turn_to(self.direction + 90, speed=0.27)

    def on_stop(self):
        self.turn_to(self.direction + 90, speed=0.27)


class MatherShip(AstroUnit):
    radius = 75
    selectable = False
    counter_attrs = dict(size=22, position=(75, 135), color=(255, 255, 255))

    def __init__(self, coord, max_elerium, team=1):
        super(MatherShip, self).__init__(coord=coord)
        CargoBox.__init__(self, initial_cargo=0, maximum_cargo=max_elerium)
        self.__team = team

    @property
    def sprite_filename(self):
        return 'mothership_{}.png'.format(self.__team)

    @property
    def counter(self):
        return self.payload



