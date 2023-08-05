""" boot code, initialisation and main loop. """

import bot.base
import bot.fleet
import logging
import obj
import os
import readline
import sys
import threading
import time

from obj.shell import init_mods, ld, start, touch
from obj.utils import get_type

class Cfg(obj.base.Dotted):

    _default = ""

class Kernel(obj.handler.Handler, bot.fleet.Fleet, obj.store.Store):

    def __init__(self):
        super().__init__()
        self._in = sys.stdin    
        self._out = sys.stdout
        self._err = sys.stderr
        self._type = get_type(self)
        self.cfg = Cfg()
        self.mods = []
        self.loaded = []

    def dispatch(self, event):
        event._func = self.get_cmd(event)
        if event._func:
            logging.warn("dispatch %s" % event.txt)
            event._func(event)
            event.show()
        event.ready()

    def start(self, name, version=bot.base.__version__, wd=""):
        cfg = start(name, version, wd)
        self.cfg.update(cfg)
        histfile = ld("history")
        touch(histfile)
        readline.read_history_file(histfile)
        super().start()
        init_mods(self, cfg.modules.split(","))
        return self

    def wait(self):
        if self.cfg.shell:
            super().wait()
