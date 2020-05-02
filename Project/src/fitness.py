
def inverse_cost(self, individual):
    return 1.0 / self.cost(individual)


def unweighted_mst(self, individual):
    v = len(individual) - 1

    return ((v * v) - v + 1) / self.cost(individual)


def weighted_mst(self, individual):
    return weighted_mst.heuristic / self.cost(individual)
