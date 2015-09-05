#!/usr/bin/python
#coding=utf8

__author__ = 'linux'
from sys import argv
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from urllib import quote
from urllib2 import urlopen, URLError
url = "http://fanyi.youdao.com/openapi.do?keyfrom=privateDict&key=1971137497&type=data&doctype=json&version=1.1&q={}"
keymap = {
    "word": "-W",
    'web': '-w',
    'trans': '-t',
    'basic': '-b',
    'help_': '-h'
}
key_meaning = {
    '-W': "设置要查询的单词，默认第一个非参数单词也可以设置该参数",
    '-w': "显示网络释义",
    '-t': '显示翻译内容',
    '-b': '显示基本释义，为默认选项',
    '-h': '显示本提示'
}


def argSeeker(header):
    for i in argv:
        index = argv.index(i)
        if i == header:
            if len(argv) > index + 1 and not argv[index + 1].startswith("-"):
                return argv[index + 1]
            else:
                return True
    return False


def web(data):
    result = data.get('web', '')
    temp = ''
    if result:
        temp += '网络释义 >>>\n'
        for i in result:
            temp += '\t' + i.get('key') + '\n\t'
            for j in i.get('value'):
                temp += j + ','
            temp += '\n'
    else:
        temp += "米有发现→_→ {} 这个单词额".format(data.get('query', ''))
    return temp


def trans(data):
    result = data.get('translation', '')
    temp = ''
    if result:
        temp += '翻译 >>>\n'
        for i in result:
            temp += '\t' + i + '\n'
    else:
        temp += web(data)
    return temp


def basic(data):
    result = data.get('basic', '')
    temp = ''
    if result:
        temp += '基本释义 >>>\n'
    else:
        temp += web(data)
        return temp
    phonetic = result.get('phonetic', '')
    us_phonetic = result.get('us-phonetic', '')
    uk_phonetic = result.get('uk-phonetic', '')
    base = result.get('explains', '')
    if phonetic:
        temp += "\t[{}]\n".format(phonetic)
    if us_phonetic:
        temp += "\tus. [{}]\n".format(us_phonetic)
    if uk_phonetic:
        temp += "\tuk. [{}]\n".format(uk_phonetic)
    if base:
        for i in base:
            temp += '\t' + i + "\n"
    else:
        temp += web(data)
    return temp


def help_():
    result = "deploy like this\n\tyoudao word | [-w -t -W -b -h] args"
    for k in key_meaning:
        result += '\n\t' + k + ' ==> ' + key_meaning[k]
    return result


def get_data(word):
    try:
        handle = urlopen(url.format(quote(word)), timeout=3)
        from json import loads
        reader = loads(handle.read())
        handle.close()
        """
        from json import dumps
        print dumps(reader, indent=1)
        """
        return reader
    except URLError:
        print('网络连接出现问题')
    except Exception, e:
        print type(e)
    return False

if __name__ == '__main__':
    choice = {}
    result = ''
    if len(argv) >= 2:
        for j in keymap:
            choice[j] = argSeeker(keymap[j])
        if not argv[1].startswith('-'):
            choice['word'] = argv[1]
    else:
        for m in keymap:
            choice[m] = False
        choice['help_'] = True
    if choice['word']:
        temp = get_data(choice['word'])
        if temp:
            print(choice['word'])
            del choice['help_']
            del choice['word']
            if True not in choice.values():
                choice['basic'] = True
            for i in choice:
                if choice[i]:
                    result += eval(i)(temp)
    elif choice['help_']:
        result += help_()
    """
    print(choice)"""
    print(result)
