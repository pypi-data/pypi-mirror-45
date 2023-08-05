""" basic bot commands. """

import obj

from obj import get_type
from obj.utils import get_exception

from .run import kernel, users

def fleet(event):
    try:
        nr = int(event.args[0])
    except (IndexError, ValueError):
        event.reply(str([get_type(b) for b in kernel.bots]))
        return
    try:
        event.reply(str(kernel.bots[nr]))
    except IndexError:
        pass

def load(event):
    if not event.args:
        loader = obj.loader.Loader()
        loader.walk("obj")
        loader.walk("bot")
        event.reply("|".join(sorted([x.split(".")[-1] for x in loader.table.keys()])))
        return
    name = event.args[0]
    try:
        mod = kernel.walk(name)
    except ModuleNotFoundError:
        event.reply("module %s not found." % name)
        return
    except:
        event.reply(get_exception())
    event.reply("%s loaded" % name)

def meet(event):
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("|".join(sorted(users.userhosts.keys())))
        return
    origin = users.userhosts.get(origin, origin)
    u = users.meet(origin, perms)
    event.reply("added %s" % u.user)

def unload(event):
    if not event.args:
        loader = obj.loader.Loader()
        loader.walk("obj.cmds")
        loader.walk("bot")
        event.reply("|".join(loader.table.keys()))
        return
    name = event.args[0]
    try:
        del kernel.table[name]
    except KeyError:
        event.reply("%s is not loaded." % name)        
        return
    event.reply("unload %s" % name)
