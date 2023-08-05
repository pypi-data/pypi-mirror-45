""" bot package. """

__version__ = 62

import obj

class Bot(obj.handler.Handler):

    def __init__(self):
        super().__init__()
        self.cache = obj.base.OutputCache()
        self.channels = []
        self.prompt = False
        self.state = obj.base.Dotted()
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
             self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        if not obj.cfg.workdir:
            obj.cfg.workdir = hd(".bot")
            obj.utils.cdir(obj.cfg.workdir)
        self.start()
        from .event import Event
        txt = self.get_aliased(txt)
        e = Event(txt)
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def dispatch(self, event):
        from .run import kernel
        kernel.dispatch(event)

    def fileno(self):
        import sys
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
        from .run import kernel
        super().start()
        kernel.add(self)
