# coding=utf8
import os
import json
__author__ = "hellflame"


class Youdao:
    def __init__(self, phrase='', db_path=''):
        self.phrase = phrase.lower()
        self.result = {}
        self.valid = True
        self.raw = ''
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.expanduser('~/.youdao.sqlite3.db')

    def set_phrase(self, phrase):
        self.phrase = phrase.lower()

    def valid_check(self):
        if 'translation' not in self.result or \
                (len(self.result['translation']) == 1 and self.result['translation'][0] == self.result['query']):
            self.valid = False
            return False
        return True

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


if __name__ == '__main__':
    youdao = Youdao('fox')
    print (youdao.shred_auto_complete('f'))


