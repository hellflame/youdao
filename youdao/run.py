#!/usr/bin/env python2.7
# coding=utf8

import os
import sys
from youdao import Youdao
from sqlsaver import SQLSaver

db_path = SQLSaver().db_path
youdao = Youdao()

__version__ = '4.0.5'
__author__ = "hellflame"

reload(sys)
sys.setdefaultencoding("utf8")

map_target = {
    '--trans': '直接翻译',
    '--web': '网络翻译',
    '--basic': '基本释义',
    '--all': "翻译+基本释义",
    '--help': "显示帮助信息",
    '--clean': "清除数据库",
    "--version": "版本信息",
    '--debug': "调试模式",
    '--comp': "自动补全"
}

short = {
    '--trans': "-t",
    '--web': '-w',
    '--basic': '-b',
    '--all': '-a',
    '--help': '-h',
    '--clean': '-c',
    '--version': '-v',
    '--debug': '-d',
    '--comp': '-cp'
}


def help_menu():
    print "\n有道翻译终端程序\n"
    print "Usage:"
    print "  youdao <word | phrase | sentence> [args...]\t参数后置，查询翻译或解释"
    print "  youdao [args...] <word | phrase | sentence>\t参数前置，查询翻译或解释\n"
    for i in map_target:
        print "  {},{}\t{}".format(i, short[i], map_target[i])

    print "\n输入\033[01;31myoudao + 想要查询的内容\033[00m即可\n"
    print "更多帮助信息 \nhttps://github.com/hellflame/youdao/blob/v{}/README.md\n".format(__version__)


def main():
    argv = sys.argv
    arg_len = len(argv)
    if arg_len == 1:
        help_menu()
    else:
        if arg_len == 2:
            arg = argv[-1]
            if arg in ('-v', '--version'):
                print 'YoudaoDict Version {}'.format(__version__)
            elif arg in ('-c', '--clean'):
                os.remove(db_path)
                print db_path + '  removed'
            elif arg in ('-h', '--help'):
                help_menu()
            elif arg in ('-cp', '--comp'):
                print youdao.complete_code()
            elif arg == '--shard':
                print youdao.shred_auto_complete('')
            else:
                if not arg.startswith("-"):
                    youdao.set_phrase(arg)
                    youdao.executor()
                    result = youdao.basic()
                    web_result = youdao.web()
                    trans = youdao.trans()
                    if result:
                        print result
                    elif not result and youdao.valid and web_result:
                        print web_result
                    elif not result and youdao.valid and trans:
                        print trans
                    else:
                        print " (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(arg)
                else:
                    help_menu()
        elif arg_len == 3:
            arg = argv[1:]
            if arg[0].startswith('-'):
                if not arg[0] == '--shard' and not arg[1].startswith("-"):
                    youdao.set_phrase(arg[1])
                    youdao.executor()

                    if arg[0] in ('-d', '--debug'):
                        print youdao.check_raw()
                    elif arg[0] in ('-w', '--web'):
                        print youdao.web()
                    elif arg[0] in ('-t', '--trans'):
                        print youdao.trans()
                    elif arg[0] in ('-b', '--basic'):
                        print youdao.basic()
                    elif arg[0] in ('-a', '--all'):
                        print youdao.basic()
                        print youdao.web()
                        print youdao.trans()
                    else:
                        help_menu()
                elif arg[0] == '--shard':
                    print youdao.shred_auto_complete(arg[1])

            elif arg[1].startswith('-'):
                if not arg[0].startswith('-'):
                    youdao.set_phrase(arg[0])
                    youdao.executor()
                    if arg[1] in ('-d', '--debug'):
                        print youdao.check_raw()
                    elif arg[1] in ('-w', '--web'):
                        print youdao.web()
                    elif arg[1] in ('-t', '--trans'):
                        print youdao.trans()
                    elif arg[1] in ('-b', '--basic'):
                        print youdao.basic()
                    elif arg[1] in ('-a', '--all'):
                        print youdao.basic()
                        print youdao.web()
                        print youdao.trans()
                    else:
                        help_menu()
                else:
                    help_menu()
            else:
                temp = " ".join(arg)
                youdao.set_phrase(temp.strip('-'))
                youdao.executor()
                result = youdao.basic()
                if result:
                    print result
                elif not result and not youdao.is_new and youdao.valid:
                    print youdao.trans()
                else:
                    print " (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(youdao.phrase)

        elif arg_len == 4:
            arg = argv[1:]
            temp = " ".join(arg)
            youdao.set_phrase(temp.strip('-'))
            youdao.executor()
            result = youdao.basic()
            if result:
                print result
            elif youdao.result and not youdao.is_new and not result and youdao.valid:
                print youdao.trans()
            else:
                print " (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(youdao.phrase)


if __name__ == '__main__':
    main()

