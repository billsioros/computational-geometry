
from logging import getLogger
from random import randint, random

from trait import Trait


class GeneticAlgorithm(Trait):
    TRAITS = {'mutate', 'crossover', 'fitness', 'select'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.MUTATION_PROBABILITY = kwargs.get('mutation_probability', None)
        self.FITNESS_THRESHOLD = kwargs.get('fitness_threshold', None)

        self.POPULATION_SIZE = kwargs.get('population_size', None)
        self.MAX_ITERATIONS = kwargs.get('max_iterations', None)

        self.logger = getLogger(self.__class__.__name__)

    def fit(self, individual):
        population = [individual]
        for _ in range(self.POPULATION_SIZE - 1):
            population.append(self.mutate(individual))

        fitest, max_fitness = None, 0
        for i in range(self.MAX_ITERATIONS):
            self.logger.info(
                f'Iteration: {i:04d}, '
                f'fitness: {max_fitness:5.3f}'
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
