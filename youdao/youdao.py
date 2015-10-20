# coding=utf8
import sys
from urllib import quote
from urllib2 import urlopen, URLError
from json import loads, dumps
from random import choice
from instantDB.controller import Controller
from os import popen
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = "hellflame"

My_keys = [
    {
        'key': '1971137497',
        'key_from': 'privateDict'
    },
    {
        'key': '1189092886',
        'key_from': 'hellflame'
    },
    {
        'key': '623990957',
        'key_from': 'hellflamedns'
    },
    {
        'key': '93848407',
        'key_from': 'hellflameyoudao'
    }
]
keymap = {
    '-h': 'help',
    '--help': 'help',
    '-w': 'web',
    '--web': 'web',
    '-t': 'trans',
    '--translate': 'trans',
    '--trans': 'trans',
    '-b': 'basic',
    '--base': 'basic'
    }


DB_PATH = "{}/.youdao".format(popen("echo $HOME").read().strip())


def pre_check(func):
    def _dec(self, * args):
        if not self.data:
            print ("未获取到所查内容!")
        elif self.data.get('errorCode', ''):
            print ("返回码错误!")
        elif 'web' not in self.data and 'basic' not in self.data\
                and (len(self.data['translation']) == 1 and self.data['translation'][0] == self.data['query']):
            print("米有发现﹃_﹃ \033[01;31m{}\033[00m ﹄_﹄这个单词额".format(self.data['query']))
        else:
            if not self.DB.search(self.target):
                self.DB.insert(self.target, dumps(self.data))
            return func(self, * args)
    return _dec

chs = choice(My_keys)

key_from = chs['key_from']
key = chs['key']


class Youdao:
    def __init__(self, word, private_key_from=key_from, private_key=key):
        self.data_url = "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&type=data&doctype=json&version=1.1&q={}".\
            format(private_key_from, private_key, quote(word))
        self.target = word
        self.has_basic = False
        self.has_web = False
        self.has_trans = False
        self.DB = Controller(data_dir=DB_PATH)
        self.data = self.init_data()
        self.result = False

    @pre_check
    def web(self):
        """ -w or --web => 返回结果中将带有网络释义,若无网络释义则选项无效 """
        temp = ""
        if "web" not in self.data:
            return temp
        temp += "网络释义 \033[01;34m>>>\033[00m\n"
        for i in self.data['web']:
            temp += '\t' + i['key'] + '\n\t'
            for j in i['value']:
                temp += '  ' + j + ','
            temp += '\n'
        return temp

    @pre_check
    def trans(self):
        """-t or --trans or --translate => 返回结果中将带有翻译, 若无翻译则此选项无效 """
        temp = ""
        if 'translation' not in self.data:
            return temp
        temp += '翻译 \033[01;33m>>>\033[00m\n'
        for i in self.data['translation']:
            temp += '\t' + i + '\n'
        return temp

    @pre_check
    def basic(self):
        """-b or --basic => 返回结果中将带有基本释义,若无基本释义则此选项无效,此选项在主函数调用时为默认选项 """
        temp = ""
        data = self.data.get('basic', '')
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

    def init_data(self):
        try:
            result = self.DB.search(self.target)
            if result:
                reader = result
            else:
                handle = urlopen(self.data_url, timeout=3)
                reader = loads(handle.read())
                handle.close()
            if 'basic' in reader:
                self.has_basic = True
            if 'web' in reader:
                self.has_web = True
            if 'translation' in reader:
                self.has_trans = True
            return reader
        except URLError:
            print("网络连接故障")
        except ValueError:
            print("数据获取失败")
        except Exception, e:
            print (type(e))
        return None

    @pre_check
    def sum_up(self, basic=True, web=False, trans=False):
        temp = "\033[01;31m{}\033[00m\n".format(self.data['query'])
        pitch = False
        if basic and self.has_basic:
            temp += self.basic()
            pitch = True
        if web and self.has_web:
            temp += self.web()
            pitch = True
        if trans and self.has_trans:
            temp += self.trans()
            pitch = True
        if not pitch:
            if self.has_web:
                temp += self.web()
                pitch = True
        if not pitch and self.trans():
            temp += self.trans()
        return temp


def arg_piper():
    argv = sys.argv
    argc = len(argv)
    spit = {
        'basic': False,
        'web': False,
        'trans': False,
        'help': False,
        'word': ''
    }
    if argc == 1:
        spit['help'] = True
        return spit
    if argc >= 2:
        mark = True
        if argc == 3:
            for i in argv:
                if i in ('--basic', '--trans', '--translate',
                         '--help', '--web', '--all'):
                    mark = False
                    break
        if mark and argc == 3:
            simple = {
                'b': 'basic',
                'w': 'web',
                'h': 'help',
                't': 'trans'
            }
            for i in argv[1:3]:
                if i.startswith('-') and len(i) >= 2 and not i.startswith('--'):
                    for j in i[1:]:
                        if 'a' in j:
                            spit['basic'] = True
                            spit['web'] = True
                            spit['trans'] = True
                        if j in simple:
                            spit[simple[j]] = True
                else:
                    spit['word'] += i + ' '
            if not spit['web'] and not spit['trans'] and not spit['basic']:
                spit['basic'] = True
            return spit
        else:
            for i in argv[1:]:
                if not i.startswith('-'):
                    spit['word'] += i + ' '
                else:
                    if i == '--all':
                        spit['basic'] = True
                        spit['web'] = True
                        spit['trans'] = True
                    if i in keymap:
                        spit[keymap[i]] = True
            if not spit['web'] and not spit['trans'] and not spit['basic']:
                spit['basic'] = True
            return spit


def help_():
    help_str = "deploy like this\n\tyoudao the sentence you don\\'t know\n\t" \
               "youdao 中文\n\tyoudao linux -wtb\n\tyoudao hellflame --trans\n\tyoudao -w hehe \n\t...\n"
    help_str += "\n\t" + "-b or\n\t\t --basic => 返回结果中将带有基本释义,为默认选项"
    help_str += "\n\t" + "-w or\n\t\t --web => 返回结果中将带有网络释义"
    help_str += "\n\t" + "-t or\n\t\t --trans \n\t\t --translate => 返回结果中将带有翻译"
    help_str += "\n\t" + "-a or\n\t\t --all => 输出所有查询内容,相当于 -wbt 等\n"
    print (help_str)


def main():
    args = arg_piper()
    if not args['word']:
        print("请输入需要查询的单词~~")
        return help_()
    if args['help']:
        return help_()
    youdao = Youdao(args['word'])
    result = youdao.sum_up(args['basic'], args['web'], args['trans'])
    if result:
        print(result)
    else:
        print('')

if __name__ == '__main__':
    main()




