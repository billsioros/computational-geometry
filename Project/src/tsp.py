
from random import shuffle

import crossovers
import metrics
import mutations
from annealing import SimulatedAnnealing
from genetic import GeneticAlgorithm


class TravellingSalesman(SimulatedAnnealing, GeneticAlgorithm):
    def __init__(
        self,
        metric='euclidean', mutate='random_swap', crossover='interleave',
        mutation_probability=0.3, fitness_threshold=0.8,
        max_temperature=100000, cooling_rate=0.000005,
        max_iterations=10000
    ):
        self.metric = metric
        self.mutate = mutate
        self.crossover = crossover

        self.MUTATION_PROBABILITY = mutation_probability
        self.FITNESS_THRESHOLD = fitness_threshold

        self.MAX_TEMPERATURE = max_temperature
        self.COOLING_RATE = cooling_rate

        self.MAX_ITERATIONS = max_iterations

    @property
    def metric(self):
        return self.__metric

    @metric.setter
    def metric(self, metric):
        if isinstance(metric, str):
            try:
                metric = metric.lower().replace("-", "_")
                self.__metric = getattr(metrics, metric)
            except:
                raise AssertionError(f'No metric named {metric}')
        elif callable(metric):
            self.__metric
        elif isinstance(metric, list):
            self.__metric = lambda v1, v2: metric[v1][v2]
        else:
            raise AssertionError(f'Unexpected metric type {type(metric)}')

    @property
    def mutate(self):
        return self.__mutate

    @mutate.setter
    def mutate(self, mutate):
        if isinstance(mutate, str):
            try:
                mutate = mutate.lower().replace("-", "_")
                self.__mutate = getattr(mutations, mutate)
            except:
                raise AssertionError(f'No mutation named {mutate}')
        elif callable(mutate):
            self.__mutate = mutate
        else:
            raise AssertionError(f'Unexpected mutation type {type(mutate)}')

    @property
    def crossover(self):
        return self.__crossover

    @crossover.setter
    def crossover(self, crossover):
        if isinstance(crossover, str):
            try:
                crossover = crossover.lower().replace("-", "_")
                self.__crossover = getattr(crossovers, crossover)
            except:
                raise AssertionError(f'No crossover named {crossover}')
        elif callable(crossover):
            self.__crossover = crossover
        else:
            raise AssertionError(
                f'Unexpected crossover type {type(crossover)}')

    def cost(self, cities):
        return sum([self.metric(cities[i], cities[i + 1]) for i in range(len(cities) - 1)])

    def fitness(self, individual):
        return 0

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
        def reverse_sublist(points, i, j):
            mutation = points[:]

            mutation[i:j] = mutation[i:j][::-1]

            return mutation

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

    def genetic_algorithm(self, depot, cities, population_size=100):
        population, partial = [[depot] + cities + [depot]], cities[:]
        for _ in range(population_size - 1):
            shuffle(partial)
            population.append([depot] + partial + [depot])

        fittest = GeneticAlgorithm.fit(self, population)

        return fittest, self.cost(fittest)
