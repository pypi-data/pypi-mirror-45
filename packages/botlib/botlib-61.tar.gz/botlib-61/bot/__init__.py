""" bot package. """

__version__ = 61

import logging
import obj
import sys

from obj import cdir, cfg
from obj.tasks import launch
from obj.utils import get_name, hd

from .event import Event
from .run import kernel

class Bot(obj.handler.Handler):

    def __init__(self):
        super().__init__()
        self.cache = obj.OutputCache()
        self.channels = []
        self.prompt = False
        self.state = obj.Dotted()
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
             self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        if not cfg.workdir:
            cfg.workdir = hd(".bot")
            cdir(cfg.workdir)
        self.start()
        txt = self.get_aliased(txt)
        e = bot.event.Event(txt)
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def dispatch(self, event):
        kernel.dispatch(event)

    def fileno(self):
        return sys.stdin

    def join(self):
        pass

    def raw(self, txt):
        print(txt)

    def resume(self):
        pass

    def say(self, botid, channel, txt):
        if self.verbose:
            self.cache.add(channel, txt)
            self.raw(txt)

    def show_prompt(self):
        pass

    def start(self):
        super().start()
        kernel.add(self)

    def work(self):
        while not self._stopped:
            event = self._queue.get()
            if not event:
                break
            self.dispatch(event)
        self.ready()

import bot.cmds
import bot.entry
import bot.event
import bot.fleet
import bot.irc
import bot.kernel
import bot.rss
import bot.run
import bot.users
