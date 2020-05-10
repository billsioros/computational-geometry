
from logging import getLogger
from random import randint, random

from trait import Trait


class GeneticAlgorithm(Trait):
    traits = ['mutate', 'crossover', 'fitness', 'select']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'mutate' in kwargs:
            self.mutate = kwargs['mutate']
        if 'crossover' in kwargs:
            self.crossover = kwargs['crossover']
        if 'fitness' in kwargs:
            self.fitness = kwargs['fitness']
        if 'select' in kwargs:
            self.select = kwargs['select']

        self.MUTATION_PROBABILITY = kwargs['mutation_probability']
        self.FITNESS_THRESHOLD = kwargs['fitness_threshold']

        self.POPULATION_SIZE = kwargs['population_size']
        self.MAX_ITERATIONS = kwargs['max_iterations']

        self.logger = getLogger(self.__class__.__name__)

    def fit(self, individual):
        population = [individual]
        for _ in range(self.POPULATION_SIZE - 1):
            population.append(self.mutate(individual))

        fitest, max_fitness = None, 0
        for i in range(self.MAX_ITERATIONS):
            self.logger.debug(
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
                father = self.select(population)
                mother = self.select(population)

                child = self.crossover(father, mother)

                if random() < self.MUTATION_PROBABILITY:
                    child = self.mutate(child)

                successors.append(child)

            population = successors

        return fitest
