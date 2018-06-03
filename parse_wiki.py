

import re
import requests
from bs4 import BeautifulSoup

REG_DATE_PAREN = re.compile(r'\([0-9_\s-]+\)')
REG_TEXT_PAREN = re.compile(r'\s?\(([^)]+)\)\s?')
REG_REF = re.compile(r'\[[0-9]+\]')
REG_DATE = re.compile(r"([0-9]+\s*)?[A-Za-z0-9éèû'\s,-]+\s*(\([^\)]+\))?\s*:")
REG_PUNCT = re.compile(r'[,.]([.,;!?]+)')
REG_YEAR = re.compile(r'^([0-9]+)')
assert REG_DATE.match('5 octobre (ou le 4 décembre) : Rober')
assert REG_DATE.match('26 novembre, Coupe UEFA féminine, demi-finales retour : a')


def on_paren(match:str) -> str:
    text = match.group()
    if any(c.isnumeric() for c in text):
        return ''
    return text


def get_entries(soup, visiteds:set=None) -> [str]:
    visiteds = visiteds or set()
    # find direct entries
    for item in soup.find_all('li'):
        cls = item.get('class') or item.get('id')
        if cls is None and item.text.endswith('.'):
            text = REG_REF.sub('', item.text)
            # print(text)
            # print()
            if REG_DATE.match(text):
                text = text[text.find(':')+1:].strip()
            text = REG_TEXT_PAREN.sub(on_paren, text).strip()
            text = REG_DATE_PAREN.sub('', text).strip()
            text = REG_PUNCT.sub(r'\1', text).strip()
            yield text
    # find detailed articles
    for item in soup.find_all('div'):
        if item.get('class') and item.get('class')[0].startswith('bandeau-section') and item.text.lower().startswith(('article détaillé', 'articles détaillés')):
            for article in item.find_all('a'):
                if not REG_YEAR.match(article.text): continue  # ignore non-year centered articles
                article = article.get('href')
                if not article.startswith('/wiki/'):
                    continue
                if article[len('/wiki/'):].startswith(('D%C3%A9c%C3%A8s_', 'Naissance_')):
                    continue  # ignore births and deaths
                if article in visiteds: continue  # don't do it twice
                visiteds.add(article)
                # print(article)
                article = 'https://fr.wikipedia.org{}'.format(article)
                yield from get_entries_from_url(article, visiteds=visiteds)

def get_entries_from_url(url:str, visiteds:set=None) -> [str]:
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    yield from get_entries(soup, visiteds or set())

def get_entries_from_year(year:int) -> [str]:
    yield from get_entries_from_url('https://fr.wikipedia.org/wiki/{}'.format(year))

def get_entries_from_example() -> [str]:
    with open('./example_wiki.html') as fd:
        soup = BeautifulSoup(fd, 'html.parser')
    yield from get_entries(soup)


if __name__ == "__main__":
    for entry in get_entries_from_year(1938):
        pass
        # print(entry)
    # print('\n'.join(get_entries_from_example()))
