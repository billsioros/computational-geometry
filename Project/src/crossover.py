
from random import randint, random


def cut_and_stitch(self, individual_a, individual_b):
    individual_a, individual_b

    offsprint = individual_a[1:len(individual_a) // 2]
    for b in individual_b[1:-1]:
        if b not in offsprint:
            offsprint.append(b)

    return [individual_a[0]] + offsprint + [individual_b[0]]
