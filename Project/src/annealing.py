
from logging import getLogger
from math import exp
from random import random

from trait import Trait


class SimulatedAnnealing(Trait):
    traits = ['mutate', 'cost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'mutate' in kwargs:
            self.mutate = kwargs['mutate']
        if 'cost' in kwargs:
            self.cost = kwargs['cost']

        self.MAX_TEMPERATURE = kwargs['max_temperature']
        self.COOLING_RATE = kwargs['cooling_rate']
        self.MAX_ITERATIONS = kwargs['max_iterations']

        self.logger = getLogger(self.__class__.__name__)

    def acceptance_probability(self, current_cost, candidate_cost, temperature):
        if candidate_cost < current_cost:
            return 1
        else:
            return exp((current_cost - candidate_cost) / temperature)

    def fit(self, initial):
        current, best = initial, initial
        current_cost = best_cost = self.cost(current)

        temperature, iteration = self.MAX_TEMPERATURE, 0
        while iteration < self.MAX_ITERATIONS and temperature > 1:
            self.logger.info(
                f'Iteration: {iteration:04d}, '
                f'Temperature: {temperature:09.3f}, '
                f'Score: {best_cost:04d}'
            )

            candidate = self.mutate(current)
            candidate_cost = self.cost(candidate)

            if self.acceptance_probability(current_cost, candidate_cost, temperature) > random():
                current, current_cost = candidate, candidate_cost

            if current_cost < best_cost:
                best, best_cost = current, current_cost
                temperature, iteration = self.MAX_TEMPERATURE, 0

            iteration += 1
            temperature *= (1 - self.COOLING_RATE)

        return best, best_cost
