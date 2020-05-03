
from random import shuffle

from annealing import SimulatedAnnealing
from genetic import GeneticAlgorithm


class TravellingSalesman(SimulatedAnnealing, GeneticAlgorithm):
    def __init__(
        self,
        metric='euclidean', fitness='weighted_mst',
        mutate='random_swap', crossover='interleave',
        heuristic='kruskal',
        mutation_probability=0.3, fitness_threshold=0.8, population_size=100,
        max_temperature=100000, cooling_rate=0.000005,
        max_iterations=10000
    ):
        super(TravellingSalesman, self).__init__(
            metric=metric,
            mutate=mutate,
            max_temperature=max_temperature, cooling_rate=cooling_rate,
            crossover=crossover, fitness=fitness, heuristic=heuristic,
            mutation_probability=mutation_probability,
            fitness_threshold=fitness_threshold,
            population_size=population_size,
            max_iterations=max_iterations
        )

    def nearest_neighbor(self, depot, cities):
        route, remaining = [depot], cities[:]

        while len(remaining) > 0:
            nearest = (0, self.metric(self, route[-1], remaining[0]))
            for i in range(1, len(remaining)):
                city = remaining[i]
                distance = self.metric(self, route[-1], city)
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
