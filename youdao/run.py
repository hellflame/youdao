# coding=utf8
from youdao import Youdao
from paramSeeker import ParamSeeker

seeker = ParamSeeker()
youdao = Youdao()

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
        youdao.status.set_API_key(data[0], data[1])
        print ("add key pair done, it keys error, use --remove")
    else:
        print("input two values")
    exit(0)


@seeker.seek('--remove', extra={'desc': 'remove broken keys'})
def add_keys(wanted):
    data = wanted.split(' ')
    if len(data) == 1:
        youdao.status.remove_API_key(data[0])
        print ("remove key pair done")
    else:
        print("tell me the key name ")
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


@seeker.seek('--clean', short='-c', is_mark=True, extra={'desc': 'clean the db'})
def web(wanted):
    import os
    os.remove(youdao.db_path)
    return youdao.db_path + '  removed'


def runner():
    seeker.run()

if __name__ == '__main__':
    runner()

