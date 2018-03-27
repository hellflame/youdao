# coding=utf8
import spider
import customizer
import sqlsaver
from gevent.monkey import patch_all
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore
from gevent.timeout import Timeout

patch_all()
__author__ = "hellflame"


class Race(object):
    def __init__(self, phrase=''):
        self.phrase = phrase.lower()
        self.pool = Pool()
        self.sem = BoundedSemaphore(3)
        self.result = None
        self.sql_saver = sqlsaver.SQLSaver()

    def race(self, runner):
        with self.sem:
            try:
                runner()
            except Timeout:
                # 继承自 BaseException，不能通过 Exception 截获异常
                return

    def local_sql_fetch(self):
        with Timeout(1, False):
            result = self.sql_saver.query(self.phrase)
            if result:
                self.racer_weapon(result, gun='sql')

    def custom_server_fetch(self):
        with Timeout(5, False):
            result = customizer.Customize(self.phrase).server_fetch()
            if result:
                self.racer_weapon(result, gun='custom')

    def official_server_fetch(self):
        timeout = 7
        with Timeout(timeout, False):
            _, result = spider.Spider(timeout=timeout).deploy(self.phrase)
            if result:
                self.racer_weapon(result, gun='official')

    def racer_weapon(self, bullet, gun):
        self.result = bullet
        # print gun
        if not gun == 'sql' and 'possibles' not in bullet:
            self.sql_saver.upset(self.phrase, bullet)
        self.pool.kill()

    def launch_race(self):
        self.pool.map(self.race, [self.custom_server_fetch, self.official_server_fetch, self.local_sql_fetch])


if __name__ == '__main__':
    race = Race('what')
    race.launch_race()
    print race.result


