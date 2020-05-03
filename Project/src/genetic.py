
from logging import getLogger
from random import randint, random

from base import Crossover, Fitness, Heuristic, Mutate


class GeneticAlgorithm(Crossover, Mutate, Fitness, Heuristic):
    def __init__(
        self,
        *args,
        mutate='random_swap', crossover='cut_and_stitch',
        fitness='weighted_mst', heuristic='kruskal',
        mutation_probability=0.3, fitness_threshold=0.8,
        population_size=100, max_iterations=10000,
        **kwargs
    ):
        super(GeneticAlgorithm, self).__init__(
            crossover=crossover, mutate=mutate,
            fitness=fitness, heuristic=heuristic
        )

        self.MUTATION_PROBABILITY = mutation_probability
        self.FITNESS_THRESHOLD = fitness_threshold

        self.POPULATION_SIZE = population_size
        self.MAX_ITERATIONS = max_iterations

        self.logger = getLogger(self.__class__.__name__)

    def fit(self, individual):
        if self.heuristic is not None:
            self.fitness.heuristic = self.heuristic(self, individual)

        population = [individual]
        for _ in range(self.POPULATION_SIZE - 1):
            population.append(self.mutate(self, individual))

        fitest, max_fitness = None, 0
        for i in range(self.MAX_ITERATIONS):
            self.logger.info(f'Iteration: {i}, Fitness: {max_fitness}')

            _fitness = {
                tuple(individual): self.fitness(self, individual)
                for individual in population
            }

            population.sort(key=lambda p: _fitness[tuple(p)], reverse=True)

            _fitest = population[0]
            _max_fitness = _fitness[tuple(population[0])]
            if (_max_fitness > max_fitness):
                fitest, max_fitness = _fitest, _max_fitness

            # TODO
            # if max_fitness > self.FITNESS_THRESHOLD:
            #     break

            successors = []
            for i in range(len(population)):
                father = population[randint(0, len(population) / 2 - 1)]
                mother = population[randint(0, len(population) / 2 - 1)]

                child = self.crossover(self, father, mother)

                if random() < self.MUTATION_PROBABILITY:
                    child = self.mutate(self, child)

                successors.append(child)

            population = successors

        return fitest
