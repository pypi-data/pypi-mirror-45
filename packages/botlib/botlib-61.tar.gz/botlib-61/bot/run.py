""" place to stash runtime objects. """

import bot
import obj
import sys

from bot.kernel import Kernel
from bot.users import Users

cfg = obj.Cfg()
kernel = Kernel()
users = Users()

def cmd(txt):
    s = obj.shell.Shell()
    s.prompt = False
    s.verbose = False
    e = s.cmd(txt)
    e.wait()
    return e

def launch(func, *args, **kwargs):
    t = obj.tasks.Task()
    t.start()
    t.put(func, args, kwargs)
    return t
    
def get(name):
    return getattr(sys.modules[__name__], name, None)

def set(name, o):
    return setattr(sys.modules[__name__], name, o)
