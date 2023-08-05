""" simple data entry commands. """

import obj

class Log(obj.Dotted):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(obj.Dotted):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    obj = Log()
    obj.txt = event.rest
    obj.save(timed=True)
    event.ok(1)

def todo(event):
    obj = Todo()
    obj.txt = event.rest
    obj.save(timed=True)
    event.ok(1)
