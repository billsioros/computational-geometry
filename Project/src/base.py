
import crossover
import fitness
import heuristic
import metric
import mutate


def multi_type(package_name):
    from functools import wraps

    package = globals()[package_name]

    def wrapper(method):
        @wraps(method)
        def setter(self, value):
            if isinstance(value, str):
                try:
                    value = value.lower().replace("-", "_")
                    setattr(self, f"_{package_name}", getattr(package, value))
                except:
                    raise ImportError(f'No {package_name} named {value}')
            elif value is None or callable(value):
                setattr(self, f"_{package_name}", value)
            elif isinstance(value, list):
                setattr(self, f"_{package_name}", lambda v1, v2: value[v1][v2])
            else:
                raise TypeError(
                    f'Unexpected {package_name} type {type(value)}'
                )

        return setter

    return wrapper


class Trait(object):
    def __init__(self, *args, **kwargs):
        super(Trait, self).__init__()


class Mutate(Trait):
    def __init__(self, *args, **kwargs):
        super(Mutate, self).__init__(*args, **kwargs)
        self.mutate = kwargs['mutate']

    @property
    def mutate(self):
        return self._mutate

    @mutate.setter
    @multi_type('mutate')
    def mutate(self, value):
        pass


class Crossover(Trait):
    def __init__(self, *args, **kwargs):
        super(Crossover, self).__init__(*args, **kwargs)
        self.crossover = kwargs['crossover']

    @property
    def crossover(self):
        return self._crossover

    @crossover.setter
    @multi_type('crossover')
    def crossover(self, value):
        pass


class Metric(Trait):
    def __init__(self, *args, **kwargs):
        super(Metric, self).__init__(*args, **kwargs)
        self.metric = kwargs['metric']

    @property
    def metric(self):
        return self._metric

    @metric.setter
    @multi_type('metric')
    def metric(self, value):
        pass

    def cost(self, cities):
        return sum([
            self.metric(self, cities[i], cities[i + 1])
            for i in range(len(cities) - 1)
        ])


class Fitness(Trait):
    def __init__(self, *args, **kwargs):
        super(Fitness, self).__init__(*args, **kwargs)
        self.fitness = kwargs['fitness']

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    @multi_type('fitness')
    def fitness(self, value):
        pass


class Heuristic(Trait):
    def __init__(self, *args, **kwargs):
        super(Heuristic, self).__init__(*args, **kwargs)
        self.heuristic = kwargs['heuristic']

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    @multi_type('heuristic')
    def heuristic(self, value):
        pass
