
from abc import ABC, abstractmethod
from math import isclose
from random import randint, random


class GeneticAlgorithm(ABC):
    def __init__(self, mutation_probability, max_iterations, fitness_threshold):
        self.MUTATION_PROBABILITY = mutation_probability
        self.MAX_ITERATIONS = max_iterations
        self.FITNESS_THRESHOLD = fitness_threshold

    def fit(self, population):
        fitest, max_fitness = population[0], self.fitness(population[0])

        for i in range(self.MAX_ITERATIONS):
            _fitness = {tuple(p): self.fitness(p) for p in population}

            population.sort(key=lambda p: _fitness[tuple(p)], reverse=True)

            _fitest = population[0]
            _max_fitness = _fitness[tuple(population[0])]
            if (_max_fitness > max_fitness):
                fitest, max_fitness = _fitest, _max_fitness

            if isclose(max_fitness, self.FITNESS_THRESHOLD):
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

    @abstractmethod
    def crossover(self, father, mother, *args, **kwargs):
        raise NotImplementedError("This method must be overridden")

    @abstractmethod
    def mutate(self, individual, *args, **kwargs):
        raise NotImplementedError("This method must be overridden")

    @abstractmethod
    def fitness(self, individual, *args, **kwargs):
        raise NotImplementedError("This method must be overridden")
