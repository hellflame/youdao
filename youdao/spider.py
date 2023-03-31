# coding=utf8

import sys
import bs4
import requests
from contextlib import contextmanager

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class Spider(object):
    def __init__(self, lang='eng', timeout=3):
        self.__html_url = "http://dict.youdao.com/w/{}/".format(lang)
        self.__headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/65.0.3325.146 Safari/537.36",
            "Cookie": "domain=.youdao.com"
        }
        self.__timeout = timeout

    @contextmanager
    def soup(self, target_word):
        """get bs soup context"""
        url = self.__html_url + quote(target_word.replace('/', ''))
        try:
            resp = requests.get(url, timeout=self.__timeout, headers=self.__headers)
            if not resp.status_code == 200:
                sys.stderr.write('链接 `{}` 非法状态码: {}\r\n'.format(url, resp.status_code))
            else:
                yield bs4.BeautifulSoup(resp.content, 'html.parser')
        except requests.Timeout:
            sys.stderr.write('链接 `{}` 请求超时\r\n'.format(url))
            yield None
        except requests.ConnectionError:
            sys.stderr.write('链接 `{}` 连接失败\r\n'.format(url))
            yield None
        except Exception as e:
            sys.stderr.write('链接 `{}` 连接时发生未知错误\r\n'.format(e.message))
            yield None

    def deploy(self, word):
        """format spider raw data"""
        with self.soup(word) as soup:
            if soup is None:
                # error handle
                return None, None
            match = soup.find(class_='keyword')
            if match:
                # pronunciation
                wordbook = soup.find(class_='wordbook-js')
                _pronounce = wordbook.find_all(class_='pronounce')
                pronounces = []
                translate = []
                web_translate = []
                word_phrase = []
                if not _pronounce:
                    _pronounce = wordbook.find_all(class_='phonetic')
                for p in _pronounce:
                    temp = p.get_text().replace(' ', '').replace('\n', '')
                    if not temp:
                        continue
                    pronounces.append(p.get_text().replace(' ', '').replace('\n', ''))

                # translation
                _trans = soup.find(class_='trans-container')
                if _trans and _trans.find('ul'):
                    _normal_trans = _trans.find('ul').find_all('li')
                    if not _normal_trans:
                        _normal_trans = _trans.find('ul').find_all(class_='wordGroup')
                    for _nt in _normal_trans:
                        title = _nt.find(class_='contentTitle')
                        type_ = _nt.find('span')
                        if title and type_ and title != type_:
                            title = title.get_text()
                            type_ = type_.get_text()
                        else:
                            title = _nt.get_text()
                            type_ = ''
                        tmp = (type_ + title).replace('\n', '')
                        if tmp.count(' ') > 4:
                            tmp = tmp.replace("  ", '')
                        translate.append(tmp)

                # web translation
                _web_trans = soup.find(id="tWebTrans")
                if _web_trans:
                    for i in _web_trans.find_all('span', class_=None):
                        temp = i.get_text().replace('\n', '').replace(' ', '')
                        if not temp:
                            continue
                        web_translate.append(temp)

                    # word phrase
                    _word_phrase = _web_trans.find(id='webPhrase')
                    if _word_phrase:
                        for i in _word_phrase.find_all(class_='wordGroup'):
                            title = i.find(class_='contentTitle')
                            if not title:
                                continue
                            title = title.get_text()
                            word_phrase.append({
                                'phrase': title,
                                'explain': i.get_text().replace('\n', '').replace(title, '').replace(' ', '')
                            })
                return 0, {
                    'pronounces': pronounces,
                    'translate': translate,
                    'web_translate': web_translate
                }
            else:
                # sentence translate may go here, but I won't use youdao. Better use google translate
                similar = soup.find(class_='error-typo')
                if similar:
                    possibles = []
                    similar = similar.find_all(class_='typo-rel')
                    for s in similar:
                        title = s.find(class_='title')
                        content = s.get_text()
                        if title:
                            title = title.get_text().replace(' ', '').replace('\n', '')
                            content = content.replace(title, '').replace(' ', '').replace('\n', '')
                        else:
                            continue
                        possibles.append({
                            'possible': title,
                            'explain': content
                        })
                    return 1, {
                        'possibles': possibles
                    }
                return None, None


if __name__ == '__main__':
    print(Spider().deploy('chinese'))

