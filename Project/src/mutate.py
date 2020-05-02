
from random import randrange


def random_swap(elements):
    neighbor = elements[:]

    i, j = randrange(1, len(elements) - 1), randrange(1, len(elements) - 1)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

    return neighbor


def reverse_random_sublist(elements):
    neighbor = elements[:]

    i, j = randrange(1, len(elements) - 1), randrange(1, len(elements) - 1)
    neighbor[i:j] = neighbor[i:j][::-1]

    return neighbor
