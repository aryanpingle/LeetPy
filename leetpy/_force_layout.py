import math
from random import randint, random
import re as regex
from typing import TypeVar, TypedDict, Optional, Dict, List, Tuple, Sequence

# TODO: Add documentation

Vertex = TypeVar("Vertex")


class EmbedNode:
    def __init__(self) -> None:
        self.pos: complex = 0 + 0j


# AREA = 100 * 100
L = 35  # math.sqrt(AREA / |V|)
DELTA = 0.975


def unit(vector: complex) -> complex:
    if abs(vector) == 0:
        return vector
    return vector / abs(vector)


def dot(v1: complex, v2: complex) -> float:
    return (v1.real * v2.real) + (v1.imag * v2.imag)


def f_rep(u: EmbedNode, v: EmbedNode, L: float) -> complex:
    u_to_v = v.pos - u.pos
    if abs(u_to_v) == 0:
        u_to_v = 1
    u_to_v = u_to_v / abs(u_to_v)

    dist = abs(u.pos - v.pos)
    magnitude = (L**2) / dist
    return magnitude * (-u_to_v)


def f_attr(u: EmbedNode, v: EmbedNode, L: float) -> complex:
    u_to_v = v.pos - u.pos
    if abs(u_to_v) == 0:
        u_to_v = 1
    u_to_v = u_to_v / abs(u_to_v)

    # TODO: Squaring is mathematically correct but causes large attractive forces
    dist = abs(u.pos - v.pos)
    # dist = abs(u.pos - v.pos) ** 2
    magnitude = dist / L
    return magnitude * u_to_v


def create_embedding(vertices: Sequence[Vertex]) -> Dict[Vertex, EmbedNode]:
    embeds: Dict[Vertex, EmbedNode] = {}

    points = set()
    for v in vertices:
        embeds[v] = EmbedNode()
        pos = 0 + 0j
        while pos in points:
            pos = randint(-100, +100) + 1j * randint(-100, +100)
        points.add(pos)
        embeds[v].pos = pos

    return embeds


def calculate_forces(
    vertices: Sequence[Vertex],
    graph: Dict[Vertex, List[Vertex]],
    embeds: Dict[Vertex, EmbedNode],
) -> Dict[Vertex, complex]:
    """
    Calculate forces on every vertex.
    """
    # L = math.sqrt(AREA / len(vertices))
    F = {v: 0 + 0j for v in vertices}

    for u in vertices:
        f_rep_sum = 0 + 0j
        for v in vertices:
            if u == v:
                continue
            f_rep_sum += f_rep(embeds[u], embeds[v], L)

        f_attr_sum = 0 + 0j
        for v in graph[u]:
            f_attr_sum += f_attr(embeds[u], embeds[v], L)

        F[u] = f_rep_sum + f_attr_sum

    return F


def apply_forces(
    vertices: Sequence[Vertex],
    graph: Dict[Vertex, List[Vertex]],
    embeds: Dict[Vertex, EmbedNode],
    forces: Dict[Vertex, complex],
):
    """
    Performs one iteration of adding forces.
    """
    for u in vertices:
        embeds[u].pos += DELTA * forces[u]
