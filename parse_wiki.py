

import re
from bs4 import BeautifulSoup

REG_DATE_PAREN = re.compile(r'\([0-9_\s-]+\)')
REG_TEXT_PAREN = re.compile(r'\s?\(([^)]+)\)\s?')
REG_REF = re.compile(r'\[[0-9]+\]')
REG_DATE = re.compile(r'([0-9]+\s*)?[A-Za-zéè]+\s*(\([^\)]+\))?\s*:')
assert REG_DATE.match('5 octobre (ou le 4 décembre) : Rober')


def on_paren(match:str) -> str:
    text = match.group()
    if any(c.isnumeric() for c in text):
        return ''
    return text


def get_entries(soup) -> [str]:
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
            yield text

if __name__ == "__main__":
    with open('example_wiki.html') as fd:
        soup = BeautifulSoup(fd, 'html.parser')
    entries = tuple(get_entries(soup))
    print('\n'.join(entries))
