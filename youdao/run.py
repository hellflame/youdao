# coding=utf8
from youdao import Youdao
from paramSeeker import ParamSeeker
from util.config import Config
import os
from random import choice

seeker = ParamSeeker()
keys = [
    {
        'key': '1971137497',
        'key_from': 'privateDict'
    },
    {
        'key': '1189092886',
        'key_from': 'hellflame'
    }
]
config = Config(os.path.expanduser('~') + '/.youdao/config.json', {'keys': keys})
my_config = config.load()['keys']
chosen = choice(my_config)
youdao = Youdao(private_key=chosen['key'], private_key_from=chosen['key_from'])


seeker.set_desc('终端翻译小工具')
seeker.set_usage_desc('youdao 中文')
seeker.set_usage_desc('youdao linux')
seeker.set_usage_desc("youdao this is a sentence that you don\\'t know")
seeker.set_usage_desc('youdao windows -twb')
seeker.set_usage_desc('youdao who --trans')


@seeker.seek('--add', extra={'desc': 'add more key and value pair'})
def add_keys(wanted):
    data = wanted.split(' ')
    if len(data) == 2:
        my_config.append({
            'key': data[0],
            'key_from': data[1]
        })
        config.config = {
            'keys': my_config
        }
        config.save()
    else:
        print("input two values")
    exit(0)


@seeker.seek()
def main(wanted):
    youdao.set_phrase(phrase=wanted)
    youdao.executor()
    result = youdao.basic()
    if result:
        return result
    elif not result and youdao.valid:
        return youdao.trans()
    else:
        return "﹃_﹃ \033[01;31m{}\033[00m ﹄_﹄".format(wanted)


@seeker.seek('--trans', short='-t', is_mark=True, extra={'desc': 'sentence translate'})
def trans(wanted):
    return youdao.trans()


@seeker.seek('--web', short='-w', is_mark=True, extra={'desc': 'web translate'})
def web(wanted):
    return youdao.web()


@seeker.seek('--debug', short='-d', is_mark=True, extra={'desc': 'print the raw data'})
def debug_mode(wanted):
    youdao.set_phrase(wanted)
    return youdao.check_raw()

"""
@seeker.seek('--store', short='-s', extra={'desc': 'enable storage, options: yes/no'})
def enable_storage(wanted):
    if wanted.lower() == 'yes':
        config.config['storage'] = True
    elif wanted.lower() == 'no':
        config.config['storage'] = False
    else:
        print("[yes] or [no] is wanted")
        exit(1)
    config.save()
    return ''
"""


def runner():
    seeker.run()

if __name__ == '__main__':
    runner()

