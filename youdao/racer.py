import asyncio

from youdao.spider import Spider
from youdao.customizer import Customize
from youdao.storage import Storage


class Race(object):
    async def run(self, phrase, serve_mode=False):
        storage = Storage()
        sources = [Spider(), storage]
        if not serve_mode:
            sources.insert(1, Customize())
        parse_map = {
            type(s).__name__: s.parse for s in sources
        }
        tasks = []
        for s in sources:
            tasks.append(asyncio.create_task(self.with_cancel_task(s.fetch(phrase),
                                                                   [t for t in tasks]),
                                             name=type(s).__name__))
        done, pending = await asyncio.wait(tasks, timeout=5)
        for p in pending:
            p.cancel()

        for d in done:
            t_name = d.get_name()
            r = d.result()
            if r:
                parsed = parse_map[t_name](r)
                if parsed and t_name != "Storage" and 'possibles' not in parsed:
                    await storage.upset(phrase, parsed)
                return parsed

    @staticmethod
    async def with_cancel_task(t, cancels):
        r = None
        try:
            r = await t
        except asyncio.exceptions.CancelledError:
            pass
        if cancels and r:
            for c in cancels:
                c.cancel()
        return r
