# coding=utf8
import sys
import json

if sys.version_info.major == 2:
    from urllib2 import urlopen, URLError
    from urllib import quote
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    from urllib.request import urlopen, URLError, quote


__author__ = "hellflame"


class Youdao:
    def __init__(self, phrase='', private_key_from='', private_key=''):
        self.data_url = "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&type=data&doctype=json&version=1.1&q={}"
        self.phrase = phrase
        self.key_from = private_key_from
        self.key = private_key
        self.result = {}
        self.valid = True

    def set_phrase(self, phrase):
        self.phrase = phrase

    def set_key(self, key):
        self.key = key

    def set_from(self, key_from):
        self.key_from = key_from

    def valid_check(self):
        if 'translation' not in self.result or \
                (len(self.result['translation']) == 1 and self.result['translation'][0] == self.result['query']):
            self.valid = False
            return False
        return True

    def executor(self):
        try:
            data_url = self.data_url.format(self.key_from, self.key, quote(self.phrase))
            self.result = json.loads(urlopen(data_url, timeout=3).read().decode('utf8'))
            self.valid_check()
            return self.result
        except URLError:
            print("whoops~~~What did you say again?")
            exit(1)
        except ValueError:
            print("Meow~~~Server responded hair bulb!")
            exit(2)
        except Exception as e:
            print(type(e))
            exit(3)

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


if __name__ == '__main__':
    youdao = Youdao('中文', 'hellflamedns', '623990957')
    youdao.executor()
    print(youdao.check_raw())
    # print(youdao.web())
    # print(youdao.trans())
    # print(youdao.basic())



