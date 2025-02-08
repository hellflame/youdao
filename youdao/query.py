import json
import asyncio
import traceback
from functools import wraps

from youdao.racer import Race
from youdao.storage import Storage


def void_return(fun):
    """check void return"""
    @wraps(fun)
    def check(self):
        if not self.result or not self.valid:
            return ''
        else:
            return fun(self)
    return check


class Query(object):
    def __init__(self, phrase=''):
        self.phrase = phrase.lower()
        self.result = {}
        self.valid = True
        self.raw = ''
        self.is_new = False

    @staticmethod
    def run_async(t):
        loop = asyncio.get_event_loop()
        try:
            return loop.run_until_complete(t)
        except:
            traceback.print_exc()
        finally:
            loop.close()

    def set_phrase(self, phrase):
        self.phrase = phrase.lower()

    def valid_check(self):
        if not self.result:
            self.is_new = True
            self.valid = False
            return False

        if 'errorCode' not in self.result:
            self.is_new = True

        if not self.is_new:
            if 'translation' not in self.result or \
                    (len(self.result['translation']) == 1 and self.result['translation'][0] == self.result['query']):
                self.valid = False

    def executor(self):
        race = Race()
        self.result = self.run_async(race.run(self.phrase))
        self.valid_check()
        return self.result

    def check_raw(self):
        return json.dumps(self.result, indent=2, ensure_ascii=False)

    @void_return
    def web(self):
        temp = ""
        if not self.is_new:
            if "web" not in self.result:
                return temp
            temp += "网络释义 \033[01;34m>>>\033[00m\n"
            for i in self.result['web']:
                temp += '\t{}\n\t'.format(i['key'])
                for j in i['value']:
                    temp += '  ' + j + ','
                temp += '\n'
        else:
            if 'web_translate' in self.result and self.result['web_translate']:
                temp += "网络释义 \033[01;34m>>>\033[00m\n"
                for i in self.result['web_translate']:
                    temp += '\t{}\n'.format(i)

        return temp.strip()

    @void_return
    def trans(self):
        temp = ""
        if not self.is_new:
            temp += '翻译     \033[01;33m>>>\033[00m\n'
            for i in self.result['translation']:
                temp += '\t{}\n'.format(i)
        else:
            possibles = self.result.get("possibles", [])

            if possibles:
                temp += "相关词语     \033[01;33m>>>\033[00m\n"
                for i in possibles:
                    temp += "\t{}\n\t{}\n\n".format(i['possible'], i['explain'])
            else:
                temp = ""

        return temp

    @void_return
    def basic(self):
        temp = ""
        if not self.is_new:
            data = self.result.get('basic', {})
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
                    temp += "\t{}\n".format(i)
        else:
            trans = self.result.get('translate', [])
            if trans:
                temp += "基本释义 \033[01;32m>>>\033[00m\n"
                pronounce = self.result.get("pronounces", [])
                for i in pronounce:
                    temp += "\t{}\n".format(i)
                for i in trans:
                    temp += "\t{}\n".format(i)
            else:
                temp = ""

        return temp

    def shred_auto_complete(self, shred):
        shreds = self.run_async(Storage().shred_query(shred))
        return " ".join((x[0] for x in shreds if len(shreds) > 1 and not x[0] == shred or x[0].startswith(shred)))


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(asctime)s|%(module)s|%(message)s")
    print(Query("linux").executor())
