
def kruskal(self, route):
    edges = []
    for u in route[:-1]:
        for v in route[:-1]:
            if u != v:
                edges.append((u, v, self.metric(self, u, v)))

    edges.sort(key=lambda edge: edge[2])

    cost, components = 0, {v: set([v]) for v in route}

    mst = set()
    for u, v, d in edges:
        if not components[u].intersection(components[v]):
            mst.add((u, v))
            cost += d

            components[u] = components[u].union(components[v])
            components[v] = components[u]

            for root, component in components.items():
                if u in component or v in component:
                    for vertex in component:
                        components[root] = components[root].union(
                            components[vertex])

    return mst, cost
