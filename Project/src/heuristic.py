
def kruskal(self, route):
    edges = []
    for u in route[:-1]:
        for v in route[:-1]:
            if u != v:
                edges.append((u, v, self.metric(self, u, v)))

    edges.sort(key=lambda edge: edge[2])

    cost, components = 0, {v: set([v]) for v in route}

    for u, v, d in edges:
        if not components[u].intersection(components[v]):
            cost += d
            components[u] = components[u].union(components[v])
            components[v] = components[v].union(components[u])

    return cost
