"""
formats to support: adjacency list, edge list, adjacency matrix
"""

# TODO: Add documentation for functions
# TODO: Allow graphing points on a plane
# TODO: Allow custom random functions for create()

import math
from random import randint, random
import re as regex
from typing import TypeVar, TypedDict, Optional, Dict, List, Tuple, Sequence

Vertex = TypeVar("Vertex")
Edge = Tuple[Vertex, Vertex]
Graph = Dict[Vertex, List[Vertex]]


class UndirectedGraph:
    @staticmethod
    def create_from_edge_list(
        vertices: Sequence[Vertex], edge_list: Sequence[Tuple[Vertex, Vertex]]
    ) -> Graph[Vertex]:
        graph: Graph = {}

        for vertex in vertices:
            graph[vertex] = []

        for edge in edge_list:
            v1, v2 = edge
            graph[v1].append(v2)
            graph[v2].append(v1)

        return graph

    @staticmethod
    def print(graph: Graph):
        for vertex in graph:
            edge_repr = "[" + ", ".join(map(str, graph[vertex])) + "]"
            print(f"{vertex}: {edge_repr}")

    @staticmethod
    def save_as_svg(
        vertices: Sequence[Vertex],
        edge_list: Sequence[Tuple[Vertex, Vertex]],
        coords: Dict[Vertex, Tuple[float, float]],
        svg_filename: str,
    ):
        text_g = []
        node_g = []
        edge_g = []

        NODE_RADIUS = 999
        for u in vertices:
            for v in vertices:
                if u == v:
                    continue
                NODE_RADIUS = min(
                    NODE_RADIUS,
                    math.hypot(coords[u][0] - coords[v][0], coords[u][1] - coords[v][1])
                    / 4,
                )
        FONT_HEIGHT = NODE_RADIUS
        CHAR_WIDTH = FONT_HEIGHT / 2

        def get_centered_text_svg(text: str, cx: float, cy: float) -> str:
            baseline_x = cx - (CHAR_WIDTH * (len(text) / 2))
            baseline_y = cy + (FONT_HEIGHT / 2) * 0.8
            return f"""
            <text x="{baseline_x}" y="{baseline_y}" style="font-family: monospace; font-size: {FONT_HEIGHT};"
            >{text}</text>
            """

        def add_edge(v1: Vertex, v2: Vertex):
            x1, y1 = coords[v1]
            x2, y2 = coords[v2]
            edge_g.append(
                f"""<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{NODE_RADIUS / 10}"></line>"""
            )

        def add_node(vertex: Vertex):
            x, y = coords[vertex]
            node_g.append(
                f"""<ellipse cx="{x}" cy="{y}" rx="{NODE_RADIUS}" ry="{NODE_RADIUS}" fill="white" stroke="black" stroke-width="{NODE_RADIUS / 10}"></ellipse>"""
            )
            text_g.append(get_centered_text_svg(str(vertex), x, y))

        for v in vertices:
            add_node(v)
        for s, t in edge_list:
            add_edge(s, t)

        x_bounds = [0, 0]
        y_bounds = [0, 0]
        for v in vertices:
            x, y = coords[v]
            x_bounds[0] = min(x_bounds[0], x)
            x_bounds[1] = max(x_bounds[1], x)
            y_bounds[0] = min(y_bounds[0], y)
            y_bounds[1] = max(y_bounds[1], y)
        SVG_WIDTH = x_bounds[1] - x_bounds[0] + (4 * NODE_RADIUS)
        SVG_HEIGHT = y_bounds[1] - y_bounds[0] + (4 * NODE_RADIUS)

        code = f"""
        <svg
        version="1.1"
        viewBox="{x_bounds[0] - 2*NODE_RADIUS} {y_bounds[0] - 2*NODE_RADIUS} {SVG_WIDTH} {SVG_HEIGHT}"
        xmlns="http://www.w3.org/2000/svg">
          <g>{''.join(edge_g)}</g>
          <g>{''.join(node_g)}</g>
          <g>{''.join(text_g)}</g>
        </svg>
        """

        # Remove newlines and leading spaces in lines (for compression)
        code = regex.sub(r"\s*(\n\s*)+", " ", code)

        with open(svg_filename, "w") as f:
            f.write(code)

    @staticmethod
    def draw(
        vertices: Sequence[Vertex],
        edge_list: Sequence[Tuple[Vertex, Vertex]],
        svg_filename: str,
    ):
        from ._force_layout import apply_forces, calculate_forces, create_embedding

        G = UndirectedGraph.create_from_edge_list(vertices, edge_list)

        embeds = create_embedding(vertices)

        ITERATION_LIMIT = 500
        EPSILON = 0.01

        iteration = 0
        F = calculate_forces(vertices, G, embeds)
        for iteration in range(ITERATION_LIMIT):
            apply_forces(vertices, G, embeds, F)
            F = calculate_forces(vertices, G, embeds)

            if max(abs(f) for f in F.values()) < EPSILON:
                break

        coords = {v: (embeds[v].pos.real, embeds[v].pos.imag) for v in vertices}
        print(f"Iterations = {iteration}")
        print(f"Min F = {min(abs(f) for f in F.values())}")
        print(f"Max F = {max(abs(f) for f in F.values())}")
        UndirectedGraph.save_as_svg(vertices, edge_list, coords, svg_filename)

    @staticmethod
    def draw_steps(
        vertices: Sequence[Vertex],
        edge_list: Sequence[Tuple[Vertex, Vertex]],
        svg_filename: str,
    ):
        from ._force_layout import apply_forces, calculate_forces, create_embedding

        G = UndirectedGraph.create_from_edge_list(vertices, edge_list)

        embeds = create_embedding(vertices)

        # Initial computation
        coords = {v: (embeds[v].pos.real, embeds[v].pos.imag) for v in vertices}
        UndirectedGraph.save_as_svg(vertices, edge_list, coords)

        F = calculate_forces(vertices, G, embeds)

        while True:
            choice = input("How many iterations? ").strip()

            if choice == "":
                choice = "1"
            iterations = int(choice)

            if iterations == 0:
                break

            for _ in range(iterations):
                apply_forces(vertices, G, embeds, F)
                F = calculate_forces(vertices, G, embeds)

            coords = {v: (embeds[v].pos.real, embeds[v].pos.imag) for v in vertices}
            print(f"Min F = {min(abs(f) for f in F.values())}")
            print(f"Max F = {max(abs(f) for f in F.values())}")
            print(f"{coords = }")
            UndirectedGraph.save_as_svg(vertices, edge_list, coords, svg_filename)
