import asyncio
import bs4
import httpx

from urllib.parse import quote


class Spider(object):
    def __init__(self, lang='eng'):
        self._html_url = "http://dict.youdao.com/w/{}/".format(lang)
        self._headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/65.0.3325.146 Safari/537.36",
            "Cookie": "domain=.query.com"
        }

    async def fetch(self, target):
        url = self._html_url + quote(target.replace('/', ''))
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=self._headers)
                resp.raise_for_status()
                return resp.content
        except httpx.ConnectError:
            pass

    @staticmethod
    def parse(raw_content):
        soup = bs4.BeautifulSoup(raw_content, 'html.parser')
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
            return {
                'pronounces': pronounces,
                'translate': translate,
                'web_translate': web_translate
            }
        else:
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
                return {
                    'possibles': possibles
                }
            return None


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(Spider().fetch('chinese')))

