import os
import json
import aiosqlite

from urllib.parse import quote, unquote

DB_PATH = os.getenv("YD_STORAGE", "~/.youdao.sqlite3.db")


class Storage(object):
    TABLE = "query"

    def __init__(self, db_path=''):
        self.db_path = db_path or os.path.expanduser(DB_PATH)

    async def check_db(self):
        if os.path.exists(self.db_path):
            return
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                             "query varchar(50) NOT NULL UNIQUE,"
                             "raw_json TEXT NOT NULL DEFAULT '')".format(self.TABLE))
            await db.commit()

    async def fetch(self, target):
        await self.check_db()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("select raw_json from {} WHERE query = ? ".format(self.TABLE),
                                      (target,))
            result = await cursor.fetchone()
            if result:
                return result[0]
            return None

    @staticmethod
    def parse(raw_content):
        return json.loads(unquote(raw_content))

    async def remove_query(self, query):
        """remove one saved query"""
        await self.check_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("delete from {} where query = ?".format(self.TABLE),
                             (query,))
            await db.commit()

    async def shred_query(self, shred):
        """query for auto complete"""
        await self.check_db()
        async with aiosqlite.connect(self.db_path) as db:
            if shred:
                cursor = await db.execute("""select query from {} WHERE query like ? limit 10""".format(self.TABLE),
                               (shred + "%",))
            else:
                cursor = await db.execute("select query from {} order by id desc limit 10".format(self.TABLE))

            return await cursor.fetchall()

    async def upset(self, query, raw_dict):
        """update or insert one query result"""
        await self.check_db()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("select id from {} WHERE query = ? ".format(self.TABLE),
                           (query,))
            result = await cursor.fetchone()
            raw_json = quote(json.dumps(raw_dict))
            if result:
                await db.execute("update {} set raw_json = ? WHERE id = ?".format(self.TABLE),
                                 (raw_json, result[0]))
            else:
                await db.execute("insert into {} (query ,raw_json) VALUES (?, ?)".format(self.TABLE),
                                 (query, raw_json))
            await db.commit()

