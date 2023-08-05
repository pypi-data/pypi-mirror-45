""" event handler. """

import logging
import obj
import obj.command
import threading

from .run import kernel

class Event(obj.command.Command):

    def __init__(self, txt=""):
        super().__init__(txt)
        self._results = []
        self._trace = ""
        self.batched = True

    def display(self):
        for txt in self._result:
            kernel.announce(txt)

    def show(self, b=None):
        if not b:
            b = kernel.get_bot(self.orig)
        if not b:
            logging.error("missing register from %s" % self.orig)
            return
        for txt in self._result:
            b.say(self.orig, self.channel, txt)
