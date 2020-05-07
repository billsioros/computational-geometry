
from logging import getLogger
from random import randint, random

from mixins import (CrossoverMixin, FitnessMixin, HeuristicMixin, MutateMixin,
                  SelectionMixin)


class GeneticAlgorithm(CrossoverMixin, MutateMixin, FitnessMixin, HeuristicMixin, SelectionMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.MUTATION_PROBABILITY = kwargs['mutation_probability']
        self.FITNESS_THRESHOLD = kwargs['fitness_threshold']

        self.POPULATION_SIZE = kwargs['population_size']
        self.MAX_ITERATIONS = kwargs['max_iterations']

        self.logger = getLogger(self.__class__.__name__)
        self.cache = {}

    def fit(self, individual):
        if self.heuristic is not None:
            self.cache['heuristic'] = self.heuristic(individual)

        population = [individual]
        for _ in range(self.POPULATION_SIZE - 1):
            population.append(self.mutate(individual))

        fitest, max_fitness = None, 0
        for i in range(self.MAX_ITERATIONS):
            self.logger.info(
                f'Iteration: {i:04d}, '
                f'FitnessMixin: {max_fitness:5.3f}'
            )

            _fitness = {
                tuple(individual): self.fitness(individual)
                for individual in population
            }

            population.sort(key=lambda p: _fitness[tuple(p)], reverse=True)

            _fitest = population[0]
            _max_fitness = _fitness[tuple(population[0])]
            if (_max_fitness > max_fitness):
                fitest, max_fitness = _fitest, _max_fitness

            if max_fitness > self.FITNESS_THRESHOLD:
                break

            successors = []
            for i in range(len(population)):
                father = population[randint(0, len(population) / 2 - 1)]
                mother = population[randint(0, len(population) / 2 - 1)]

                child = self.crossover(father, mother)

                if random() < self.MUTATION_PROBABILITY:
                    child = self.mutate(child)

                successors.append(child)

            population = successors

        return fitest
