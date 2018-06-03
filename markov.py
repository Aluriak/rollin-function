
import random
from itertools import islice
from collections import defaultdict, deque

def window(it:iter, size:int) -> [()]:
    it = iter(it)
    q = deque(islice(it, 0, size), maxlen=size)
    yield tuple(q)
    assert len(q) == size
    for item in it:
        q.append(item)
        yield tuple(q)


assert tuple(window('abcd', 2)) == (('a', 'b'), ('b', 'c'), ('c', 'd'))


def train(entries:iter, order:int=3) -> dict:
    """Return a markov model trained on given data"""
    entries = iter(entries)
    start = tuple(next(entries) for _ in range(order))
    # do the counting
    counts = defaultdict(lambda: defaultdict(int))
    counts[start][next(entries)] = 1
    for *starts, item in window(entries, size=order+1):
        counts[tuple(starts)][item] += 1

    # normalize to get probabilities
    model = defaultdict(dict)
    for starts, count in counts.items():
        total_count = sum(count.values())
        model[starts] = {item: count / total_count for item, count in count.items()}

    return dict(model)


def generate(model:dict, start:iter, maxlen:int=0, stop_items=()):
    start = tuple(start)
    assert start in model
    q = deque(start, maxlen=len(start))
    curlen = 0
    while maxlen == 0 or curlen < maxlen or (stop_items and curlen >= maxlen and item.endswith(stop_items)):
        item = step(model, tuple(q))
        q.append(item)
        yield item
        curlen += 1

def step(model:dict, start:tuple) -> object:
    choice = random.random()
    if start not in model:
        print(start)
        print(len(model))
        model[start]
    for item, val in model[start].items():
        choice -= val
        if choice <= 0:
            return item
    raise RuntimeError("Impossible choice at {} ; model: {}".format(choice, model[start]))
