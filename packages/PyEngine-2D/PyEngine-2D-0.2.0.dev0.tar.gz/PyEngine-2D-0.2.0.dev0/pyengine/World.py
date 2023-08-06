from pyengine.Systems import EntitySystem, MusicSystem
from pyengine.Exceptions import NoSystemError

__all__ = ["World"]


class World:
    def __init__(self):
        self.window = None
        self.systems = [EntitySystem(self), MusicSystem(self)]

    def get_system(self, classe):
        for i in self.systems:
            if type(i) == classe:
                return i
        raise NoSystemError("World have any "+str(classe)+" as system")

    def has_system(self, classe):
        for i in self.systems:
            if type(i) == classe:
                return True
        return False

    def set_window(self, window):
        self.window = window

    def update(self):
        for i in self.systems:
            try:
                i.update()
            except AttributeError:
                pass

    def keypress(self, key):
        for i in self.systems:
            try:
                i.keypress(key)
            except AttributeError:
                pass

    def keyup(self, key):
        for i in self.systems:
            try:
                i.keyup(key)
            except AttributeError:
                pass

    def mousepress(self, button, pos):
        for i in self.systems:
            try:
                i.mousepress(button, pos)
            except AttributeError:
                pass

    def event(self, evt):
        if evt.type == self.systems[1].ENDSOUND:
            self.systems[1].next_song()

    def show(self, screen):
        for i in self.systems:
            try:
                i.show(screen)
            except AttributeError:
                pass

    def show_debug(self, screen):
        for i in self.systems:
            try:
                i.show_debug(screen)
            except AttributeError:
                pass
