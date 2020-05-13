
def cached(method):
    from functools import wraps

    @wraps(method)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, 'cache'):
            setattr(wrapper, 'cache', method(*args, **kwargs))

        return wrapper.cache

    return wrapper


def plot(method):
    from matplotlib import pyplot as plt
    from functools import wraps

    @wraps(method)
    def wrapper(ctx, **kwargs):
        tsp = ctx.obj['class'](**{
            'metric': ctx.obj['metric'],
            'service': ctx.obj['service'],
            'timewindow': ctx.obj['timewindow'],
            **kwargs
        })

        route, cost = getattr(tsp, method.__name__)(
            ctx.obj['depot'], ctx.obj['cities']
        )

        figure = plt.figure()

        plt.title(
            f'{method.__name__.replace("_", " ").title()} '
            f'(Cities: {len(route) - 1}, Cost: {cost:07.2f})'
        )

        dx, dy = route[0]
        xs, ys = [c[0] for c in route[1:]], [c[1] for c in route[1:]]

        plt.scatter(xs, ys, c='blue', label='Cities')

        plt.scatter([dx], [dy], c='red', label='Depot')
        plt.text(
            dx - 0.5 if dx < 0 else dx + 0.5,
            dy - 0.5 if dy < 0 else dy + 0.5,
            f'({dx:05.2f}, {dy:5.2f})', fontsize=10
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


def safe(method):
    from click import echo, style
    from functools import wraps

    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            name = method.__name__.replace("_", " ").title()
            echo(style(f"{name}: ", bold=True) + str(e))
            exit(1)

    return wrapper
