#!/usr/bin/env python2.7
# coding=utf8

import os
import sys
from youdao import Youdao

youdao = Youdao()

__version__ = '3.2.0'

map_target = {
    '--trans': '直接翻译',
    '--web': '网络翻译',
    '--basic': '基本释义',
    '--all': "翻译+基本释义",
    '--a-key': '添加API key',
    '--r-key': '删除API key',
    '--help': "显示帮助信息",
    '--clean': "清除数据库",
    "--update": "更新数据库",
    "--version": "版本信息",
    '--debug': "调试模式"
}

short = {
    '--trans': "-t",
    '--web': '-w',
    '--basic': '-b',
    '--a-key': '-k',
    '--r-key': '-r',
    '--all': '-a',
    '--help': '-h',
    '--clean': '-c',
    '--update': '-u',
    '--version': '-v',
    '--debug': '-d'
}


def help_menu():
    print "\n有道翻译终端程序\n"
    print "Usage:"
    print "  youdao <word | phrase | sentence> [args...]\t参数后置，查询翻译或解释"
    print "  youdao [args...] <word | phrase | sentence>\t参数前置，查询翻译或解释\n"
    for i in map_target:
        print "  {},{}\t{}".format(i, short[i], map_target[i])

    print "\n程序一开始应该便可用，输入\033[01;31myoudao + 想要查询的内容\033[00m即可\n"
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
                os.remove(youdao.db_path)
                print youdao.db_path + '  removed'
            elif arg in ('-h', '--help'):
                help_menu()
            elif arg in ('-k', '--a-key'):
                result = youdao.status.API_list()
                if not len(result):
                    print "You Have NOT Give Me Any Keys"
                else:
                    for i, j in result:
                        print "key: {}\nfrom: {}\n".format(i, j)

            elif arg in ('-u', '--update'):
                youdao.update()

            else:
                youdao.set_phrase(arg)
                youdao.executor()
                result = youdao.basic()
                if result:
                    print result
                elif not result and youdao.valid:
                    print youdao.trans()
                else:
                    print " (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(arg)
        elif arg_len == 3:
            arg = argv[1:]
            if arg[0] in ('-r', '--r-key'):
                target = arg[1]
                youdao.status.remove_API_key(target)
                print "key pair removed"

            elif arg[0].startswith('-'):
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

            elif arg[1].startswith('-'):
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
                youdao.set_phrase(" ".join(arg))
                youdao.executor()
                result = youdao.basic()
                if result:
                    print result
                elif not result and youdao.valid:
                    print youdao.trans()
                else:
                    print " (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(youdao.phrase)

        elif arg_len == 4:
            arg = argv[1:]
            if arg[0] in ('-k', '--a-key'):
                youdao.status.set_API_key(arg[1], arg[2])
                print "key pair added, if error happens, use -r to remove them"
            else:
                youdao.set_phrase(" ".join(arg))
                youdao.executor()
                result = youdao.basic()
                if result:
                    print result
                elif not result and youdao.valid:
                    print youdao.trans()
                else:
                    print " (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(youdao.phrase)

if __name__ == '__main__':
    main()

