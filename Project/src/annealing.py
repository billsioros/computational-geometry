
from random import random
from math import exp

from abc import ABC, abstractmethod


class SimulatedAnnealing(ABC):
    def __init__(self, max_temperature, cooling_rate, max_iterations):
        self.MAX_TEMPERATURE = max_temperature
        self.COOLING_RATE = cooling_rate
        self.MAX_ITERATIONS = max_iterations

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

    @abstractmethod
    def cost(self, individual, *args, **kwargs):
        raise NotImplementedError("This method must be overridden")

    @abstractmethod
    def mutate(self, individual, *args, **kwargs):
        raise NotImplementedError("This method must be overridden")
