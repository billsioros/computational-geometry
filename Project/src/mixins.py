
from random import randint, random, randrange


def cached(method):
    from functools import wraps

    @wraps(method)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, 'cache'):
            setattr(wrapper, 'cache', method(*args, **kwargs))

        return wrapper.cache

    return wrapper


class TraitMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def to_method(self, value):
        if value is None or callable(value):
            return value
        elif isinstance(value, str):
            return getattr(self, value.lower().replace("-", "_"))
        elif isinstance(value, list):
            return lambda v1, v2: value[v1][v2]
        else:
            raise TypeError(f'Unexpected type {type(value)}')


class MutateMixin(TraitMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mutate = kwargs['mutate']

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

    @property
    def mutate(self):
        return self._mutate

    @mutate.setter
    def mutate(self, value):
        self._mutate = self.to_method(value)


class CrossoverMixin(TraitMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.crossover = kwargs['crossover']

    def cut_and_stitch(self, individual_a, individual_b):
        individual_a, individual_b

        offsprint = individual_a[1:len(individual_a) // 2]
        for b in individual_b[1:-1]:
            if b not in offsprint:
                offsprint.append(b)

        return [individual_a[0]] + offsprint + [individual_b[0]]

    @property
    def crossover(self):
        return self._crossover

    @crossover.setter
    def crossover(self, value):
        self._crossover = self.to_method(value)


class MetricMixin(TraitMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.metric = kwargs['metric']

    def euclidean(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, value):
        self._metric = self.to_method(value)

    def cost(self, cities):
        return sum([
            self.metric(cities[i], cities[i + 1])
            for i in range(len(cities) - 1)
        ])


class FitnessMixin(TraitMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fitness = kwargs['fitness']

    def inverse_cost(self, individual):
        return 1.0 / self.cost(individual)

    def unweighted_mst(self, individual):
        v = len(individual) - 1

        return ((v * v) - v + 1) / self.cost(individual)

    def weighted_mst(self, individual):
        return self.heuristic(individual) / self.cost(individual)

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = self.to_method(value)


class HeuristicMixin(TraitMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.heuristic = kwargs['heuristic']

    @cached
    def kruskal(self, route):
        edges = []
        for u in route[:-1]:
            for v in route[:-1]:
                if u != v:
                    edges.append((u, v, self.metric(u, v)))

        edges.sort(key=lambda edge: edge[2])

        cost, components = 0, {v: set([v]) for v in route}

        for u, v, d in edges:
            if not components[u].intersection(components[v]):
                cost += d

                components[u] = components[u].union(components[v])
                components[v] = components[u]

                for root, component in components.items():
                    if u in component or v in component:
                        for vertex in component:
                            components[root] = components[root].union(
                                components[vertex])

        return cost

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    def heuristic(self, value):
        self._heuristic = self.to_method(value)


class SelectionMixin(TraitMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.select = kwargs['select']

    def random_top_half(self, population):
        return population[randint(0, len(population) // 2 - 1)]

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, value):
        self._select = self.to_method(value)
