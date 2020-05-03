
from logging import getLogger
from math import exp
from random import random

from base import Metric, Mutate


class SimulatedAnnealing(Metric, Mutate):
    def __init__(
        self,
        *args,
        metric='euclidean', mutate='random_swap',
        max_temperature=100000, cooling_rate=0.000005,
        max_iterations=10000,
        **kwargs
    ):
        super(SimulatedAnnealing, self).__init__(
            metric=metric, mutate=mutate
        )

        self.MAX_TEMPERATURE = max_temperature
        self.COOLING_RATE = cooling_rate
        self.MAX_ITERATIONS = max_iterations

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

            candidate = self.mutate(self, current)
            candidate_cost = self.cost(candidate)

            if self.acceptance_probability(current_cost, candidate_cost, temperature) > random():
                current, current_cost = candidate, candidate_cost

            if current_cost < best_cost:
                best, best_cost = current, current_cost
                temperature, iteration = self.MAX_TEMPERATURE, 0

            iteration += 1
            temperature *= (1 - self.COOLING_RATE)

        return best, best_cost
