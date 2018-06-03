
import os
import random
import marshal
import itertools
import markov
import parse_wiki
import rollin


CORPUS_SAVE = 'corpus.cache'


def make_model_from_years(years:[int], order:int=6) -> dict:
    if os.path.exists(CORPUS_SAVE):
        with open(CORPUS_SAVE, 'rb') as fd:
            corpus = marshal.load(fd)
    else:
        corpus = []
        for year in years:
            print('YEAR:', year)
            corpus.append(tuple(parse_wiki.get_entries_from_year(year)))
        corpus = '\n'.join(itertools.chain.from_iterable(corpus))

        with open(CORPUS_SAVE, 'wb') as fd:
            marshal.dump(corpus, fd)

    return markov.train(corpus.split(' '), order=2)

def generate_from_model(model:dict, maxlen:int=1000) -> str:
    start = random.choice(tuple(model.keys()))
    return ' '.join(start) + ' '.join(markov.generate(model, start=start, maxlen=maxlen, stop_items='.'))


def main_example():
    """Show a usage example with the example data"""
    corpus = '\n'.join(parse_wiki.get_entries_from_example())
    # print(corpus, end='\n\n')
    model = markov.train(corpus, order=6)
    start = random.choice(tuple(model.keys()))
    print(''.join(start) + ''.join(markov.generate(model, start=start, maxlen=1000, stop_items='.')))


if __name__ == "__main__":
    print('TRAINING…', end='')
    model = make_model_from_years(rollin.annees_rollin())
    print(' DONE !')
    print(generate_from_model(model, maxlen=1000))
