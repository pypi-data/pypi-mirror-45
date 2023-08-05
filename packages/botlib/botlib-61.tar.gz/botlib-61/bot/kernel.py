# bot/kernel.py

__doc__ = """ boot code, initialisation and main loop. """

import bot
import logging
import obj
import os
import sys
import threading
import time

from obj.shell import start

from bot import __version__
from bot.fleet import Fleet

defaults = obj.Dotted()
defaults.background = ""
defaults.exclude = ""
defaults.logdir = ""
defaults.modules = ""
defaults.name = "bot"
defaults.options = ""
defaults.shell = False
defaults.usage = ""
defaults.version = __version__
defaults.wait = True
defaults.workdir = ""

class Cfg(obj.Dotted):

    _default = ""

class Kernel(obj.handler.Handler, bot.fleet.Fleet, obj.store.Store):

    def __init__(self):
        super().__init__()
        self._in = sys.stdin    
        self._out = sys.stdout
        self._err = sys.stderr
        self._type = obj.get_type(self)
        self.cfg = obj.Cfg(defaults)
        self.mods = []
        self.loaded = []

    def dispatch(self, event):
        logging.warn("dispatch %s" % event.txt)
        event._func = self.get_cmd(event)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def start(self, name, version=__version__, wd=""):
        super().start()
        shell = start(name, version, wd)
        self.add(shell)
        return shell
