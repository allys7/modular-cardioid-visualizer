# https://stackoverflow.com/questions/53161395/how-to-draw-networkx-graph-in-flask

from math import exp
from turtle import color, width
import matplotlib
import sys
from flask import Flask, render_template, send_file, redirect
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("cardioid.html", mod=9, mult=2)


@app.route("/<int:mod>,<int:mult>")
def cardiod(mod, mult):
    return render_template("cardioid.html", mod=mod, mult=mult)


@app.route("/graph/<int:mod>,<int:mult>")
def graph(mod, mult):
    G, pos, colors = generate_cardioid(mod, mult)

    # arbitrary functions for font and node size
    # graph options
    options = {
        # nodes
        "node_color": "#A0CBE2",
        "with_labels": False,
        "font_size": 2 + (20*exp(-1*mod/70)),
        "node_size": 10 + (1190*exp(-1*mod/70)),

        # edges
        "width": .5,
    }
    
    nx.draw(G, pos, edge_color=colors, **options)

    # generate & return image
    img = BytesIO()
    # plt.figure(figsize=(24,16))
    plt.box(False)
    plt.savefig(img, dpi=320)
    img.seek(0)
    plt.close()

    return send_file(img, mimetype="image/png")


def generate_cardioid(mod: int, mult: int):
    """
    function to generate the cardioid shape given a modulus and a multiplier.

    mod: int
        the modulus to operate under
    mult: int
        the multiplier to use in each step

    return: (G: DiGraph, pos: dict, distances: dict)
        G:   graph representation of cardioid
        pos: positions of nodes in increasing order
        distances: the unique distance values, used for coloring
    """

    # create graph, solidify positions of nodes *in natural order*
    G = nx.DiGraph()
    colormap = plt.cm.get_cmap('rainbow')
    G.add_nodes_from(range(mod))
    plt.figure(figsize=(12, 8))
    pos = nx.circular_layout(G)

    # list to track visited numbers as well as distances between nodes
    visited = []
    distances = {}

    # main loop
    for i in range(mod):
        """
        The basic idea of this algorithm is to repeatedly calculate the next
        number in line until we reach a number we have seen before. Once we
        reach a visited value, we can be certain that any following connection
        already exists in our graph. This process is repeated on each value from
        0 to the modulus to ensure every loop is found.
        """
        if i not in visited:
            # new loop found
            current_num = i

            while current_num not in visited:
                # determine next number & add edge
                next_num = (current_num * mult) % mod

                # if it is a self-referential loop, we just break to avoid
                # adding that edge
                if current_num == next_num:
                    break

                diff = abs(next_num - current_num)
                key = (current_num, next_num)
                if key not in distances:
                    distances[key] = diff

                G.add_edge(current_num, next_num)
                visited.append(current_num)

                # iterative step
                current_num = next_num

    # add edges coloring based on distance dict
    max_dist = max(distances.values())
    min_dist = min(distances.values())
    edge_colors = []
    for edge in G.edges():
        edge_colors.append(colormap((distances[edge] - min_dist) / (max_dist - min_dist)))

    return G, pos, edge_colors


if __name__ == "__main__":
    WEB_APP = True
    # web app
    if WEB_APP:
        # allows background processing? not exactly sure how
        matplotlib.use("Agg")
        app.run(debug=True)

    LOCAL = not WEB_APP
    # or local
    if LOCAL:
        mod = int(sys.argv[1])
        mult = int(sys.argv[2])
        G, pos, edge_colors = generate_cardioid(mod=mod, mult=mult)

        # arbitrary functions for font and node size
        divisor = 70
        size_font = 2 + (20*exp(-1*mod/divisor))
        size_node = 10 + (1190*exp(-1*mod/divisor))
        colors = range(G.number_of_edges())
        # graph options
        options = {
            # nodes
            "node_color": "#A0CBE2",
            "with_labels": False,
            "font_size": 2 + (20*exp(-1*mod/divisor)),
            "node_size": 10 + (1190*exp(-1*mod/divisor)),

            # edges
            "width": .5,
        }

        nx.draw(G, pos, edge_color=edge_colors, **options)

        plt.show()
