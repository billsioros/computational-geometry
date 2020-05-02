
from random import randrange


def random_swap(self, elements):
    neighbor = elements[:]

    i, j = randrange(1, len(elements) - 1), randrange(1, len(elements) - 1)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

    return neighbor


def reverse_random_sublist(self, elements):
    neighbor = elements[:]

    i, j = randrange(1, len(elements) - 1), randrange(1, len(elements) - 1)
    neighbor[i:j] = neighbor[i:j][::-1]

    return neighbor
