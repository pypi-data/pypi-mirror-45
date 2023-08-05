""" manage users. """

import bot
import logging
import obj

class EUSER(Exception):
    pass

class User(obj.Dotted):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(obj.store.Store):

    cache = obj.Dotted()
    userhosts = obj.Dotted()

    def allowed(self, origin, perm):
        perm = perm.upper()
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        logging.error("denied %s %s" % (origin, perm))
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin="", type=None):
        return self.all(type or "bot.users.User")

    def get_user(self, origin, type=None):
        if origin in Users.cache:
            return Users.cache[origin]
        s = {"user": origin}
        res = list(self.find(type or "bot.users.User", s))
        if res:
            u = res[-1]
            Users.cache[origin] = u
            return u

    def meet(self, origin, perms=[]):
        user = self.get_user(origin)
        if not user:
            user = User()
        user.user = origin
        user.perms = perms + ["USER", ]
        if perms:
            user.perms.extend(perms.upper())
        user.save(timed=True)
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if not user:
            user = User()
            user.user = origin
            user.perms = ["OPER", "USER"]
            user.save()
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise EUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user
