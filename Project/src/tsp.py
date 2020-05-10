
from random import randint, random, randrange, shuffle

from annealing import SimulatedAnnealing
from decorators import cached
from genetic import GeneticAlgorithm


class Mutate:
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


class Crossover:
    def cut_and_stitch(self, individual_a, individual_b):
        individual_a, individual_b

        offsprint = individual_a[1:len(individual_a) // 2]
        for b in individual_b[1:-1]:
            if b not in offsprint:
                offsprint.append(b)

        return [individual_a[0]] + offsprint + [individual_b[0]]


class Metric:
    def euclidean(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def _cost(self, cities):
        return sum([
            self.metric(cities[i], cities[i + 1])
            for i in range(len(cities) - 1)
        ])


class Fitness:
    def inverse_cost(self, individual):
        return 1.0 / self.cost(individual)

    def unweighted_mst(self, individual):
        v = len(individual) - 1

        return ((v * v) - v + 1) / self.cost(individual)

    def weighted_mst(self, individual):
        return self.heuristic(individual) / self.cost(individual)


class Heuristic:
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


class Select:
    def random_top_half(self, population):
        return population[randint(0, len(population) // 2 - 1)]


class TravellingSalesman(SimulatedAnnealing, GeneticAlgorithm, Mutate, Crossover, Metric, Fitness, Heuristic, Select):
    traits = ['metric', 'heuristic']

    def __init__(
        self,
        metric='euclidean', fitness='weighted_mst',
        mutate='random_swap', crossover='cut_and_stitch', select='random_top_half',
        heuristic='kruskal',
        mutation_probability=0.3, fitness_threshold=0.8, population_size=100,
        max_temperature=100000, cooling_rate=0.000005,
        max_iterations=10000
    ):
        super().__init__(
            metric=metric,
            mutate=mutate,
            max_temperature=max_temperature, cooling_rate=cooling_rate,
            crossover=crossover, select=select,
            fitness=fitness, heuristic=heuristic,
            mutation_probability=mutation_probability,
            fitness_threshold=fitness_threshold,
            population_size=population_size,
            max_iterations=max_iterations
        )

        self.metric = metric
        self.heuristic = heuristic

    def nearest_neighbor(self, depot, cities):
        route, remaining = [depot], cities[:]

        while len(remaining) > 0:
            nearest = (0, self.metric(route[-1], remaining[0]))
            for i in range(1, len(remaining)):
                city = remaining[i]
                distance = self.metric(route[-1], city)
                if distance < nearest[1]:
                    nearest = (i, distance)

            route.append(remaining[nearest[0]])
            del remaining[nearest[0]]

        return route + [depot], self.cost(route + [depot])

    def opt_2(self, depot, cities):
        def reverse_sublist(elements, i, j):
            copy = elements[:]

            copy[i:j] = copy[i:j][::-1]

            return copy

        route = cities[:]
        cost = self.cost([depot] + route + [depot])
        for i in range(0, len(route) - 1):
            for j in range(i + 1, len(route)):
                candidate = reverse_sublist(route, i, j)
                candidate_cost = self.cost([depot] + candidate + [depot])
                if candidate_cost < cost:
                    return self.opt_2(depot, candidate)

        return [depot] + route + [depot], self.cost([depot] + route + [depot])

    def simulated_annealing(self, depot, cities):
        return SimulatedAnnealing.fit(self, [depot] + cities + [depot])

    def genetic_algorithm(self, depot, cities):
        fittest = GeneticAlgorithm.fit(self, [depot] + cities + [depot])

        return fittest, self.cost(fittest)
