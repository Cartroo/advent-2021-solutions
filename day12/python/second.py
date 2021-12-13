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
def find_routes(src, dst, route=(), visited=frozenset(), small_cave_twice=False):
    route += (src,)
    if src == dst:
        yield route
    else:
        alternative_visited = None
        if src[0] not in ascii_uppercase:
            if not small_cave_twice and len(route) > 1:
                alternative_visited = visited
            visited = visited.union((src,))
        for next_hop in (i for i in caves[src] if i not in visited):
            if alternative_visited is None:
                yield from find_routes(next_hop, dst, route, visited, small_cave_twice)
            else:
                # If we haven't yet used our "visit twice" card on this route, we need to
                # check the routes with and without visiting twice, and union them.
                first_pass = frozenset(find_routes(next_hop, dst, route, visited, small_cave_twice))
                second_pass = frozenset(find_routes(next_hop, dst, route, alternative_visited, True))
                yield from second_pass.union(first_pass)

print(f"Number of routes={sum(1 for i in find_routes('start', 'end'))}")
