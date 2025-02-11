import os
import sys
from youdao import __version__
from youdao.query import Query
from youdao.storage import Storage


db_path = Storage().db_path
query = Query()


map_target = {
    '--trans': '直接翻译',
    '--web': '网络翻译',
    '--basic': '基本释义',
    '--all': "翻译+基本释义",
    '--help': "显示帮助信息",
    '--clean': "清除数据库",
    "--version": "版本信息",
    '--debug': "调试模式",
    '--comp': "自动补全",
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
    print("\n有道翻译终端程序\n")
    print("Usage:")
    print("  query <word | phrase | sentence> [args...]\t参数后置，查询翻译或解释")
    print("  query [args...] <word | phrase | sentence>\t参数前置，查询翻译或解释\n")
    for i in map_target:
        print("  {},{}\t{}".format(i, short[i], map_target[i]))

    print("\n输入\033[01;31myoudao + 想要查询的内容\033[00m即可\n")
    print("更多帮助信息 \nhttps://github.com/hellflame/query/blob/v{}/README.md\n".format(__version__))


def debug(q):
    print(q.check_raw())


def main():
    argv = sys.argv
    arg_len = len(argv)
    if arg_len == 1:
        help_menu()
    else:
        if arg_len == 2:
            arg = argv[-1]
            if arg in ('-v', '--version'):
                print('YoudaoDict Version {}'.format(__version__))
            elif arg in ('-c', '--clean'):
                if os.path.exists(db_path):
                    os.remove(db_path)
                    print('`{}`  removed'.format(db_path))
                else:
                    print('`{}` not exists, doing nothing'.format(db_path))
            elif arg in ('-h', '--help'):
                help_menu()
            elif arg in ('-cp', '--comp'):
                print("""###-begin-query-completion-###
# simple youdaoDict word auto completion script
# Installation: query -cp >> ~/.bashrc  (or ~/.zshrc)
# or query -cp >> ~/.bash_profile (.etc)
#
_youdao_parser_options()
{
  local curr_arg;
  curr_arg=${COMP_WORDS[COMP_CWORD]}
  COMPREPLY=( $(compgen -W "$(query --shard $curr_arg)" $curr_arg ) );
}
complete -F _youdao_parser_options query
###-end-query-completion-###""")
            elif arg == '--shard':
                print(query.shred_auto_complete(''))
            else:
                if not arg.startswith("-"):
                    query.set_phrase(arg)
                    query.executor()
                    result = query.basic()
                    web_result = query.web()
                    trans = query.trans()
                    if result:
                        print(result)
                    elif not result and query.valid and web_result:
                        print(web_result)
                    elif not result and query.valid and trans:
                        print(trans)
                    else:
                        print(" (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(arg))
                else:
                    help_menu()
        elif arg_len == 3:
            arg = argv[1:]
            if arg[0].startswith('-'):
                if not arg[0] == '--shard' and not arg[1].startswith("-"):
                    query.set_phrase(arg[1])
                    query.executor()

                    if arg[0] in ('-d', '--debug'):
                        debug(query)
                    elif arg[0] in ('-w', '--web'):
                        print(query.web())
                    elif arg[0] in ('-t', '--trans'):
                        print(query.trans())
                    elif arg[0] in ('-b', '--basic'):
                        print(query.basic())
                    elif arg[0] in ('-a', '--all'):
                        print(query.basic())
                        print(query.web())
                        print(query.trans())
                    elif arg[0] in {'-c', '--clean'}:
                        Storage().remove_query(arg[1])
                        print("removed `{}`".format(arg[1]))
                    else:
                        help_menu()
                elif arg[0] == '--shard':
                    print(query.shred_auto_complete(arg[1]))

            elif arg[1].startswith('-'):
                if not arg[0].startswith('-'):
                    query.set_phrase(arg[0])
                    query.executor()
                    if arg[1] in ('-d', '--debug'):
                        debug(query)
                    elif arg[1] in ('-w', '--web'):
                        print(query.web())
                    elif arg[1] in ('-t', '--trans'):
                        print(query.trans())
                    elif arg[1] in ('-b', '--basic'):
                        print(query.basic())
                    elif arg[1] in ('-a', '--all'):
                        print(query.basic())
                        print(query.web())
                        print(query.trans())
                    else:
                        help_menu()
                else:
                    help_menu()
            else:
                temp = " ".join(arg)
                query.set_phrase(temp.strip('-'))
                query.executor()
                result = query.basic()
                if result:
                    print(result)
                elif not result and not query.is_new and query.valid:
                    print(query.trans())
                else:
                    print(" (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(query.phrase))

        elif arg_len == 4:
            arg = argv[1:]
            temp = " ".join(arg)
            query.set_phrase(temp.strip('-'))
            query.executor()
            result = query.basic()
            if result:
                print(result)
            elif query.result and not query.is_new and not result and query.valid:
                print(query.trans())
            else:
                print(" (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(query.phrase))


if __name__ == '__main__':
    main()

