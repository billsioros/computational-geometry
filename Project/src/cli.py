
import logging
from random import randrange, seed

import click
from matplotlib import pyplot as plt

from tsp import TravellingSalesman

logger = logging.getLogger("CLI")


def plot(method):
    from functools import wraps

    @wraps(method)
    def wrapper(ctx, **kwargs):
        tsp = TravellingSalesman(**{
            'metric': ctx.obj['metric'],
            **kwargs
        })

        route, cost = getattr(tsp, method.__name__)(
            ctx.obj['depot'], ctx.obj['cities']
        )

        figure = plt.figure()

        plt.title(
            f'{method.__name__.replace("_", " ").title()} '
            f'(Cities: {len(route) - 1}, Cost: {cost})'
        )

        logger.info(f"{method.__name__}: {cost}")

        dx, dy = route[0]
        xs, ys = [c[0] for c in route[1:]], [c[1] for c in route[1:]]

        plt.scatter(xs, ys, c='blue', label='Depot')

        plt.scatter([dx], [dy], c='red', label='Cities')
        plt.text(
            dx - 0.5 if dx < 0 else dx + 0.5,
            dy - 0.5 if dy < 0 else dy + 0.5,
            f'({dx}, {dy})', fontsize=10
        )

        plt.plot([dx] + xs, [dy] + ys, 'k--', label='Route')

        plt.xlim(
            (ctx.obj['x_axis'][0] - 1) * 1.1,
            (ctx.obj['x_axis'][1] + 1) * 1.1
        )
        plt.ylim(
            (ctx.obj['y_axis'][0] - 1) * 1.1,
            (ctx.obj['y_axis'][1] + 1) * 1.1
        )
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.grid()
        plt.legend()

        if ctx.obj['format'] is not None:
            figure.savefig(
                f'{method.__name__}_{len(route) - 1:03d}_{cost:05d}.{ctx.obj["format"]}',
                format=ctx.obj['format']
            )
        else:
            plt.show()

        ctx.obj['cities'] = route[1:-1]

    return wrapper


@click.group(chain=True)
@click.option(
    '-d', '--depot',
    type=click.Tuple([int, int]), default=(None, None),
    help='the depot (starting point)'
)
@click.option(
    '-n', '--cities',
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
    type=click.Tuple([int, int]), default=[0, 50],
    help='the horizontal axis limits'
)
@click.option(
    '-y', '--y-axis', 'y_axis',
    type=click.Tuple([int, int]), default=[0, 50],
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
    type=click.STRING, default='INFO',
    help='the logging level (INFO, DEBUG, e.t.c)'
)
@click.pass_context
def cli(
    ctx,
    depot, cities, metric,
    x_axis, y_axis,
    rng_seed, fmt, logging_lvl
):
    """Visualization of various `Travelling Salesman` algorithms"""
    if rng_seed is not None:
        seed(rng_seed)

    if depot != (None, None):
        cities -= 1

    cities = [
        (randrange(x_axis[0], x_axis[1]), randrange(y_axis[0], y_axis[1]))
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
        'format': fmt
    }

    logging.basicConfig(
        level=logging._levelToName.get(logging_lvl.upper(), "INFO")
    )


@cli.command()
@click.pass_context
@plot
def nearest_neighbor(ctx):
    pass


@cli.command()
@click.pass_context
@plot
def opt_2(ctx):
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
    type=click.FLOAT, default=0.000625,
    help='the cooling rate'
)
@click.option(
    '-i', '--max-iterations', 'max_iterations',
    type=click.INT, default=10000,
    help='the maximum number of iterations'
)
@click.pass_context
@plot
def simulated_annealing(
    ctx,
    mutate,
    max_temperature, cooling_rate, max_iterations
):
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
    type=click.FLOAT, default=0.3,
    help='the probability of an individual mutating'
)
@click.option(
    '-t', '--fitness-threshold', 'fitness_threshold',
    type=click.FLOAT, default=0.8,
    help='the fitness threshold of acceptable solutions'
)
@click.option(
    '-i', '--max-iterations', 'max_iterations',
    type=click.INT, default=1000,
    help='the maximum number of iterations'
)
@click.option(
    '-n', '--population-size', 'population_size',
    type=click.INT, default=50,
    help='the size of the population'
)
@click.pass_context
@plot
def genetic_algorithm(
    ctx,
    mutate, crossover, select, heuristic, fitness,
    mutation_probability, fitness_threshold,
    max_iterations, population_size
):
    pass


if __name__ == '__main__':
    cli()
