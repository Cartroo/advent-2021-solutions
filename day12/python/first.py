#!/usr/bin/env python3.10

from collections import defaultdict
from string import ascii_uppercase
from sys import stdin

# Links are undirected, but we use a directed graph for convenient lookup.
caves = defaultdict(set)
for src, dst in ((s.strip(), d.strip()) for s, d in (line.split("-", 1) for line in stdin)):
    caves[src].add(dst)
    caves[dst].add(src)

# Simple depth-first search via a generator which yields from itself.
# For true recursion, we need to use immutable types (tuple and frozenset).
def find_routes(src, dst, route=(), visited=frozenset()):
    if src[0] not in ascii_uppercase:
        visited = visited.union((src,))
    route += (src,)
    if src == dst:
        yield route
    else:
        for next_hop in (i for i in caves[src] if i not in visited):
            yield from find_routes(next_hop, dst, route, visited)

print(f"Number of routes={sum(1 for i in find_routes('start', 'end'))}")
