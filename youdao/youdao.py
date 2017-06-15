# coding=utf8
import os
import sys
import json
import sqlite3
import random
__author__ = "hellflame"

if sys.version_info.major == 2:
    from urllib2 import urlopen, URLError
    from urllib import quote, unquote
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    from urllib.request import urlopen, URLError, quote, unquote

default_keys = (('1971137497', 'privateDict'),
                ('1189092886', 'hellflame'),
                ('623990957', 'hellflamedns'))


def db_ok(func):
    def func_wrapper(self, *args, **kwargs):
        if self.db and self.cursor:
            return func(self, *args, **kwargs)
    return func_wrapper


def cache(func):
    def func_wrapper(self):
        if len(self.phrase) > self.status.MAX_QUERY_LENGTH:
            # print "TOO LONG"
            return func(self)
        data = self.status.query(self.phrase)
        if data:
            # print "CACHE FOUND"
            self.result = json.loads(data)
            self.valid_check()
            return self.result
        else:
            # print "CACHING ..."
            data = func(self)
            error_code = data['errorCode']
            if error_code == 0:
                self.status.up_set(self.phrase, json.dumps(data))
                return data
            else:
                if error_code == 30:
                    print("Translate UnSuccessful!")
                elif error_code == 40:
                    print("Unsupported Language Type !")
                elif error_code == 50:
                    print ("Invalid key pair found !!!\n\nkey: {}\nfrom: {}\n".format(self.key, self.key_from))
                return ''
    return func_wrapper


class Youdao:
    def __init__(self, phrase='', db_path=''):
        self.data_url = "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&type=data&doctype=json&version=1.1&q={}"
        self.phrase = phrase.lower()
        self.result = {}
        self.valid = True
        self.raw = ''
        if not db_path:
            self.db_path = os.path.join(os.path.expanduser('~'), '.youdao.sqlite3.db')
        else:
            self.db_path = db_path
        self.status = Status(self.db_path)
        key = self.status.get_API_key()
        self.key = key[0]
        self.key_from = key[1]

    def set_phrase(self, phrase):
        self.phrase = phrase.lower()

    def valid_check(self):
        if 'translation' not in self.result or \
                (len(self.result['translation']) == 1 and self.result['translation'][0] == self.result['query']):
            self.valid = False
            return False
        return True

    @cache
    def executor(self):
        return self.executor_without_cache()

    def executor_without_cache(self):
        """
        if there is no need to use a cache, use this method directly
        :return:
        """
        try:
            data_url = self.data_url.format(self.key_from, self.key, quote(self.phrase))
            self.raw = urlopen(data_url, timeout=3).read().decode('utf8').encode('utf8')
            self.result = json.loads(self.raw)
            self.valid_check()
            return self.result
        except URLError:
            print("whoops~~~What did you say again?")
            exit(1)
        except ValueError:
            print("Meow~~~Server responded hair bulb!")
            exit(2)
        except Exception as e:
            print self.phrase.encode()
            print(e)
            print "up is error"
            exit(3)

    def update(self):
        data = self.status.query_list()
        for i in data:
            self.phrase = i[0].encode()
            print "updating @ {}\t".format(self.phrase),
            fetch = self.executor_without_cache()
            if fetch['errorCode'] == 0:
                self.status.up_set(self.phrase, json.dumps(fetch))
                print "ok"
            else:
                print "failed"

    def check_raw(self):
        return json.dumps(self.result, indent=2)

    def web(self):
        temp = ""
        if "web" not in self.result:
            return temp
        temp += "网络释义 \033[01;34m>>>\033[00m\n"
        for i in self.result['web']:
            temp += '\t' + i['key'] + '\n\t'
            for j in i['value']:
                temp += '  ' + j + ','
            temp += '\n'
        return temp

    def trans(self):
        temp = ""
        if not self.valid_check():
            return temp
        temp += '翻译     \033[01;33m>>>\033[00m\n'
        for i in self.result['translation']:
            temp += '\t' + i + '\n'
        return temp

    def basic(self):
        temp = ""
        data = self.result.get('basic', '')
        if not data:
            return temp
        temp += "基本释义 \033[01;32m>>>\033[00m\n"
        phonetic = data.get('phonetic', '')
        us_phonetic = data.get('us-phonetic', '')
        uk_phonetic = data.get('uk-phonetic', '')
        base = data.get('explains', '')
        if phonetic:
            temp += "\t[{}]\n".format(phonetic)
        if us_phonetic:
            temp += "\tus. [{}]\n".format(us_phonetic)
        if uk_phonetic:
            temp += "\tuk. [{}]\n".format(uk_phonetic)
        if base:
            for i in base:
                temp += '\t' + i + "\n"
        return temp

    def shred_auto_complete(self, shred):
        shreds = self.status.shred_query(shred)
        temp = " ".join((x[0] for x in shreds if len(shreds) > 1 and not x[0] == shred or x[0].startswith(shred)))
        return temp

    @staticmethod
    def complete_code():
        return """###-begin-youdao-completion-###
# simple youdaoDict word auto completion script
# Installation: youdao -cp >> ~/.bashrc  (or ~/.zshrc)
# or youdao -cp >> ~/.bash_profile (.etc)
#
_youdao_parser_options()
{
  local curr_arg;
  curr_arg=${COMP_WORDS[COMP_CWORD]}
  COMPREPLY=( $(compgen -W "$(youdao --shard $curr_arg)" $curr_arg ) );
}
complete -F _youdao_parser_options youdao
###-end-youdao-completion-###"""


class Status:
    def __init__(self, db_path):
        """
        Databases to save Youdao queries
        :param db_path: SQLite3 file db path

        # TODO: data compress
        """
        self.db_path = db_path
        self.db = None
        self.cursor = None
        self.QUERY = 'query'
        self.BASIC = 'basic'
        self.TRANSLATION = 'translation'
        self.WEB = 'web'
        self.API = 'API_keys'
        self.MAX_QUERY_LENGTH = 50
        self.init_db()

    def __del__(self):
        if self.db:
            self.db.commit()
            self.db.close()

    def init_db(self):
        try:
            self.db = sqlite3.connect(self.db_path)
            self.cursor = self.db.cursor()
            # TODO: save more specific data rather than big json string
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                "query varchar({}) NOT NULL UNIQUE,"
                                "{} TEXT NOT NULL DEFAULT '',"
                                "{} TEXT NOT NULL DEFAULT '',"
                                "{} TEXT NOT NULL DEFAULT '',"
                                "raw_json TEXT NOT NULL DEFAULT '')".format(
                                    self.QUERY,
                                    self.MAX_QUERY_LENGTH,
                                    self.BASIC,
                                    self.WEB,
                                    self.TRANSLATION))

            # customize API keys
            self.cursor.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                                "key VARCHAR(20) NOT NULL PRIMARY KEY,"
                                "value VARCHAR(30) NOT NULL )".format(self.API))
        except Exception as e:
            print(e)

    @db_ok
    def set_API_key(self, key, value):
        self.cursor.execute("select * from `{}` WHERE key = '{}' and value = '{}'".format(self.API, key, value))
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute("insert into `{}` VALUES ('{}', '{}')".format(self.API, key, value))
            return False
        return True

    @db_ok
    def remove_API_key(self, key):
        try:
            self.cursor.execute("delete from `{}` WHERE key = '{}'".format(self.API, key))
        except Exception as e:
            print(e)

    @db_ok
    def get_API_key(self, key=''):
        if key:
            self.cursor.execute("select value from {} WHERE key = '{}'".format(self.API, key))
            result = self.cursor.fetchone()
            if result:
                return [key, result[0]]
        self.cursor.execute("select key, value from {}".format(self.API))
        result = self.cursor.fetchall()
        if not result:
            return random.choice(default_keys)
        else:
            return random.choice(result)

    @db_ok
    def API_list(self):
        self.cursor.execute("select key, value from {}".format(self.API))
        result = self.cursor.fetchall()
        return result

    @db_ok
    def query_list(self):
        self.cursor.execute("select query from {}".format(self.QUERY))
        result = self.cursor.fetchall()
        return result

    @db_ok
    def query(self, query):
        self.cursor.execute("select raw_json from {} "
                            "WHERE query = '{}' ".format(self.QUERY, query))
        result = self.cursor.fetchone()
        if result:
            # don't forget to decode the SQL safe string
            return unquote(result[0])
        return None

    def shred_query(self, shred):
        if shred:
            self.cursor.execute("""select query from {} WHERE query like "{}%" limit 10""".format(
                self.QUERY, shred
            ))
        else:
            self.cursor.execute("select query from {} limit 10".format(self.QUERY))

        result = self.cursor.fetchall()
        return result

    @db_ok
    def up_set(self, query, raw_json):
        # TODO: `update` or `insert` without status check for laziness
        self.cursor.execute("select id from {} WHERE query = '{}' ".format(self.QUERY, query))
        result = self.cursor.fetchone()
        # don't forgot to decode
        data = json.loads(unquote(raw_json))
        # in order to avoid some SQL syntax error, encode them into some safer string
        fetch = (quote(json.dumps(data.get(self.BASIC, ''))),
                 quote(json.dumps(data.get(self.WEB, ''))),
                 quote(json.dumps(data.get(self.TRANSLATION), '')))
        if result:
            self.cursor.execute("update {} set "
                                "raw_json='{}', "
                                "{} = '{}',"
                                "{} = '{}',"
                                "{} = '{}' WHERE id = {}".format(self.QUERY,
                                                                 quote(raw_json),
                                                                 self.BASIC, fetch[0],
                                                                 self.WEB, fetch[1],
                                                                 self.TRANSLATION, fetch[2],
                                                                 result[0]))
        else:
            self.cursor.execute("""insert into {} (query, raw_json, {}, {}, {}) VALUES
                               ('{}', '{}', '{}', '{}', '{}')""".format(
                                    self.QUERY,
                                    self.BASIC,
                                    self.WEB,
                                    self.TRANSLATION,
                                    query,
                                    quote(raw_json),
                                    fetch[0],
                                    fetch[1],
                                    fetch[2]
                                ))

if __name__ == '__main__':
    youdao = Youdao('fox')
    print (youdao.shred_auto_complete('f'))


