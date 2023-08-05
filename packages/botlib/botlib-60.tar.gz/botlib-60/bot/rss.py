""" feed fetcher. """

import bot
import obj
import re

from obj.utils import file_time, get_feed, strip_html, to_time, unescape

from .run import kernel, launch

def init():
    fetcher = bot.rss.Fetcher()
    return fetcher.start()

class Cfg(obj.Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_list = ["title", "link"]
        self.summary = []

class Seen(obj.Dotted):

    def __init__(self):
        super().__init__()
        self.urls = []

class Feed(obj.Dotted):

    pass

class Fetcher(obj.Dotted):

    seen = Seen()

    def __init__(self):
        super().__init__()
        self._thrs = []
        self.cfg = Cfg()

    def display(self, obj):
        result = ""
        if "display_list" in obj:
            dl = obj.display_list
        else:
            dl = self.cfg.display_list
        for key in dl:
            if key == "summary":
                skip = False
                for txt in self.cfg.summary:
                    if txt not in obj.link:
                        skip = True
                if skip:
                    continue
            data = obj.get(key, None)
            if data:
                data = str(data)
                data = data.replace("\n", " ")
                data = strip_html(data.rstrip())
                data = re.sub(r"\s+", " ", data)
                data = unescape(data)
                result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        counter = 0
        objs = []
        for obj in get_feed(rssobj.rss):
            if not obj:
                continue
            feed = Feed(dict(obj))
            if feed.link in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(feed.link)
            counter += 1
            feed.update(rssobj)
            objs.append(feed)
            if "updated" in feed:
                date = file_time(to_time(feed.updated))
                feed.save(stime=date)
                continue
            elif "published" in feed:
                date = file_time(to_time(feed.published))
                feed.save(stime=date)
                continue
            feed.save()
        Fetcher.seen.save()
        for obj in objs:
            txt = self.display(obj)
            kernel.announce(txt)
        return counter

    def join(self):
        for thr in self._thrs:
            thr.join()

    def run(self):
        for obj in kernel.all("bot.rss.Rss"):
            self._thrs.append(launch(self.fetch, obj))
        return self._thrs

    def start(self, repeat=True):
        last = kernel.last(get_type(self))
        if last:
            self.cfg.upgrade(last)
            self.cfg.save()
        last_seen = kernel.last("bot.rss.Seen")
        if last_seen:
            Fetcher.seen.update(last_seen)
        if repeat:
            repeater = Repeater(600, self.run)
            repeater.start()
            return repeater

    def stop(self):
        Fetcher.seen.save()

class Rss(obj.Dotted):

    def __init__(self):
        super().__init__()
        self.rss = ""

def fetch(event):
    fetcher = Fetcher()
    fetcher.start(repeat=False)
    thrs = fetcher.run()
    res = []
    for thr in thrs:
        res.append(thr.join())
    event.reply("fetched %s" % ",".join([str(x or "0") for x in res]))

def rss(event):
    if not event.rest or "http" not in event.rest:
        event.reply("rss <url>")
        return
    o = Rss()
    o.rss = event.rest
    o.save()
    event.reply("ok 1")
