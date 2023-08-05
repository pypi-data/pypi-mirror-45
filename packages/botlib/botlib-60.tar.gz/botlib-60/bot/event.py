""" event handler. """

import bot
import logging
import obj
import obj.command
import threading

class Event(obj.command.Command):

    def __init__(self, txt=""):
        super().__init__(txt)
        self._func = None
        self._ready = threading.Event()
        self._result = []
        self._results = []
        self._target = None
        self._thrs = []
        self._trace = ""
        self.batched = True
        self.channel = ""

    def display(self):
        for txt in self._result:
            bot.run.kernel.announce(txt)

    def ok(self, txt=""):
        self.reply("ok %s" % txt or self.cmd.cmd)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self._result.append(txt)

    def show(self, b=None):
        if not b:
            b = bot.run.kernel.get_bot(self.orig)
        if not b:
            logging.error("missing register from %s" % self.orig)
            return
        for txt in self._result:
            b.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        result = []
        thrs = []
        for thr in self._thrs:
            try:
                ret = thr.join()
            except RuntimeError:
                continue
            thrs.append(thr)
            self._results.append(ret)
        for thr in thrs:
            self._thrs.remove(thr)
        return self
