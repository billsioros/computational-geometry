
import logging
from random import uniform, seed

import click

from decorators import plot, safe
from helpers import Dictionary
from tsp import TravellingSalesman, TravellingSalesmanTimeWindows


@click.group(chain=True)
@click.option(
    '-d', '--depot',
    type=click.Tuple([float, float]), default=(None, None),
    help='the depot'
)
@click.option(
    '-c', '--cities',
    type=click.INT, default=10,
    help='the number of cities'
)
@click.option(
    '-m', '--metric',
    type=click.STRING, default='euclidean',
    help='the distance metric to be used'
)
@click.option(
    '-x', '--x-axis', 'x_axis',
    type=click.Tuple([float, float]), default=[0, 50],
    help='the horizontal axis limits'
)
@click.option(
    '-y', '--y-axis', 'y_axis',
    type=click.Tuple([float, float]), default=[0, 50],
    help='the vertical axis limits'
)
@click.option(
    '-s', '--seed', 'rng_seed',
    type=click.INT, default=None,
    help='the random number generator seed'
)
@click.option(
    '-f', '--format', 'fmt',
    type=click.STRING, default=None,
    help='the format of the resulting figure file'
)
@click.option(
    '-l', '--logging-lvl', 'logging_lvl',
    type=Dictionary(logging._nameToLevel), default='CRITICAL',
    help='the logging level'
)
@click.option(
    '-p', '--problem',
    type=Dictionary({'tsp': TravellingSalesman, 'tsptw': TravellingSalesmanTimeWindows}), default='tsp',
    help='the class of the problem'
)
@click.pass_context
def cli(
    ctx,
    depot, cities,
    metric,
    x_axis, y_axis,
    rng_seed, fmt, logging_lvl,
    problem
):
    '''Visualization of various `Travelling Salesman` algorithms'''
    if rng_seed is not None:
        seed(rng_seed)

    if depot != (None, None):
        cities -= 1

    cities = [
        (uniform(x_axis[0], x_axis[1]), uniform(y_axis[0], y_axis[1]))
        for i in range(cities)
    ]

    if depot == (None, None):
        depot, cities = cities[0], cities[1:]

    ctx.obj = {
        'depot': depot,
        'cities': cities,
        'metric': metric,
        'x_axis': x_axis,
        'y_axis': y_axis,
        'format': fmt,
        'class': problem
    }

    logging.basicConfig(level=logging_lvl)


@cli.command()
@click.pass_context
@safe
@plot
def nearest_neighbor(*args, **kwargs):
    pass


@cli.command()
@click.pass_context
@safe
@plot
def opt_2(*args, **kwargs):
    pass


@cli.command()
@click.option(
    '-m', '--mutate',
    type=click.STRING, default='random_swap',
    help='the mutation function to be used'
)
@click.option(
    '-t', '--max-temperature', 'max_temperature',
    type=click.FLOAT, default=100000,
    help='the maximum temperature'
)
@click.option(
    '-c', '--cooling-rate', 'cooling_rate',
    type=click.FloatRange(0, 1), default=0.000625,
    help='the cooling rate'
)
@click.option(
    '-i', '--max-iterations', 'max_iterations',
    type=click.INT, default=10000,
    help='the maximum number of iterations'
)
@click.pass_context
@safe
@plot
def simulated_annealing(*args, **kwargs):
    pass


@cli.command()
@click.option(
    '-m', '--mutate',
    type=click.STRING, default='shift_1',
    help='the mutation function to be used'
)
@click.option(
    '--cooling-rate', 'cooling_rate',
    type=click.FloatRange(0, 1), default=0.05,
    help='the cooling rate'
)
@click.option(
    '--acceptance-ratio', 'acceptance_ratio',
    type=click.FloatRange(0, 1), default=0.94,
    help='the initial acceptance ratio'
)
@click.option(
    '--initial-pressure', 'initial_pressure',
    type=click.FLOAT, default=0,
    help='the initial pressure'
)
@click.option(
    '--compression-rate', 'compression_rate',
    type=click.FloatRange(0, 1), default=0.06,
    help='the compression rate'
)
@click.option(
    '--pressure-cap-ratio', 'pressure_cap_ratio',
    type=click.FloatRange(0, 1), default=0.9999,
    help='the pressure cap ratio'
)
@click.option(
    '--iterations-per-temperature', 'iterations_per_temperature',
    type=click.INT, default=30000,
    help='the number of iterations per temperature value'
)
@click.option(
    '--minimum-temperature-changes', 'minimum_temperature_changes',
    type=click.INT, default=100,
    help='the minimum number of temperature changes that have to occur'
)
@click.option(
    '--idle-temperature-changes', 'idle_temperature_changes',
    type=click.INT, default=75,
    help='the maximum number of idle temperature changes'
)
@click.option(
    '--trial-iterations', 'trial_iterations',
    type=click.INT, default=30000,
    help='the number of trial iterations'
)
@click.option(
    '--trial-neighbor-pairs', 'trial_neighbor_pairs',
    type=click.INT, default=5000,
    help='the number of trial neighbor pairs'
)
@click.pass_context
@safe
@plot
def compressed_annealing(*args, **kwargs):
    pass


@cli.command()
@click.option(
    '-m', '--mutate',
    type=click.STRING, default='random_swap',
    help='the mutation function to be used'
)
@click.option(
    '-c', '--crossover',
    type=click.STRING, default='cut_and_stitch',
    help='the crossover function to be used'
)
@click.option(
    '-s', '--select',
    type=click.STRING, default='random_top_half',
    help='the selection function to be used'
)
@click.option(
    '-h', '--heuristic',
    type=click.STRING, default='kruskal',
    help='the heuristic to be used in the calculation of the fitness'
)
@click.option(
    '-f', '--fitness',
    type=click.STRING, default='weighted_mst',
    help='the function determining the fitness of an individual'
)
@click.option(
    '-p', '--mutation-probability', 'mutation_probability',
    type=click.FloatRange(0, 1), default=0.3,
    help='the probability of an individual mutating'
)
@click.option(
    '-t', '--fitness-threshold', 'fitness_threshold',
    type=click.FloatRange(0, 1), default=0.8,
    help='the fitness threshold of acceptable solutions'
)
@click.option(
    '-i', '--max-iterations', 'max_iterations',
    type=click.INT, default=1000,
    help='the maximum number of iterations'
)
@click.option(
    '--population-size', 'population_size',
    type=click.INT, default=50,
    help='the size of the population'
)
@click.pass_context
@safe
@plot
def genetic_algorithm(*args, **kwargs):
    pass


if __name__ == '__main__':
    cli()
