import os
import argparse
from youdao import __version__
from youdao.query import Query
from youdao.storage import Storage


def parse(args=None):
    parser = argparse.ArgumentParser(
        description="有道翻译终端程序",
        epilog="更多帮助信息 \nhttps://github.com/hellflame/youdao/blob/v{}/README.md\n".format(__version__)
    )

    parser.add_argument("words", nargs="*", help="查询内容")
    parser.add_argument("-v", "--version", action="store_true", help="版本信息")

    group = parser.add_argument_group(title="翻译")
    group.add_argument("-t", "--trans", action="store_true", help="直接翻译")
    group.add_argument("-w", "--web", action="store_true", help="网络翻译")
    group.add_argument("-a", "--all", action="store_true", help="翻译+基本释义")

    group = parser.add_argument_group(title="管理")
    group.add_argument("--clean", action="store_true", help="清除本地词库")
    group.add_argument("-r", "--raw", action="store_true", help="展示词库原始响应")
    group.add_argument("-cp", "--comp", action="store_true", help="自动不全脚本")
    group.add_argument("--shard", action="store_true", help="查询本地匹配")

    return parser, parser.parse_args(args)


def main(args=None):
    parser, parsed = parse(args)
    if parsed.version:
        return print('YoudaoDict Version {}'.format(__version__))
    if parsed.clean:
        db_path = Storage().db_path
        if os.path.exists(db_path):
            os.remove(db_path)
            print('`{}` removed'.format(db_path))
        else:
            print('`{}` not exists, doing nothing'.format(db_path))
        return
    if parsed.comp:
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
    words = " ".join(parsed.words).lower()
    if not words:
        return parser.print_help()
    if parsed.shard:
        return print(Query().shred_auto_complete(words))
    q = Query()
    q.set_phrase(words)
    q.executor()
    result = q.basic()
    if not result:
        return print(" (╯▔皿▔ )╯ \033[01;31m{}\033[00m ㄟ(▔皿▔ ㄟ)".format(words))
    if parsed.raw:
        return print(q.check_raw())
    if parsed.trans:
        return print(q.trans() or "暂无相关翻译")
    if parsed.web:
        return print(q.web() or "暂无相关网络释义")
    if parsed.all:
        print(q.basic())
        print(q.web())
        print(q.trans())
        return
    print(result)


if __name__ == '__main__':
    main()

