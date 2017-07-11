import os
import json
import sqlite3
from contextlib import contextmanager
from urllib import quote, unquote
__author__ = "hellflame"


class SQLSaver(object):
    def __init__(self, db_path=''):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.expanduser('~/.youdao.sqlite3.db')
        self.TABLE = 'query'

    @contextmanager
    def connection(self):
        try:
            db = sqlite3.connect(self.db_path)
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "query varchar(50) NOT NULL UNIQUE,"
                           "raw_json TEXT NOT NULL DEFAULT '')".format(
                            self.TABLE))
            yield cursor
            db.commit()
            db.close()
        except Exception as e:
            raise e

    def query(self, query):
        with self.connection() as cursor:
            cursor.execute("select raw_json from {} WHERE query = '{}' ".format(self.TABLE, query))
            result = cursor.fetchone()
            if result:
                return json.loads(unquote(result[0]))
            return None

    def shred_query(self, shred):
        with self.connection() as cursor:
            if shred:
                cursor.execute("""select query from {} WHERE query like "{}%" limit 10""".format(
                    self.TABLE, shred
                ))
            else:
                cursor.execute("select query from {} limit 10".format(self.TABLE))

            result = cursor.fetchall()
            return result

    def upset(self, query, raw_dict):
        with self.connection() as cursor:
            cursor.execute("select id from {} WHERE query = '{}' ".format(self.TABLE, query))
            result = cursor.fetchone()
            raw_json = quote(json.dumps(raw_dict))
            if result:
                cursor.execute("update {} set raw_json = '{}' WHERE id = {}".format(self.TABLE,
                                                                                    raw_json,
                                                                                    result[0]))
            else:
                cursor.execute("insert into {} (query ,raw_json) VALUES ('{}', '{}')".format(self.TABLE,
                                                                                             query,
                                                                                             raw_json))





