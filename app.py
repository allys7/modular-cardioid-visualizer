# https://stackoverflow.com/questions/53161395/how-to-draw-networkx-graph-in-flask

import matplotlib
import sys
from flask import Flask, render_template, send_file
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the cardiod generator!"


@app.route("/<int:mod>,<int:mult>")
def cardiod(mod, mult):
    return render_template("cardioid.html", mod=mod, mult=mult)


@app.route("/graph/<int:mod>,<int:mult>")
def graph(mod, mult):
    G, pos = generate_cardioid(mod, mult)

    nx.draw(G, pos=pos, node_color='black', node_size=500, font_color='white',
    font_size=20.0, with_labels=True)

    # generate & return image
    img = BytesIO()
    # plt.figure(figsize=(24,16))
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

    return: (G: DiGraph, pos: dict)
        G:   graph representation of cardioid
        pos: positions of nodes in increasing order
    """

    # create graph, solidify positions of nodes *in natural order*
    G = nx.DiGraph()
    G.add_nodes_from(range(mod))
    plt.figure(figsize=(32,24))
    pos = nx.circular_layout(G)

    # list to track visited numbers
    visited = []

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
            # print(f"Starting loop at {i}")
            # new loop found
            current_num = i

            while current_num not in visited:
                # determine next number & add edge
                next_num = (current_num * mult) % mod

                # if it is a self-referential loop, we just break to avoid
                # adding that edge
                if current_num == next_num:
                    break

                G.add_edge(current_num, next_num)
                visited.append(current_num)
                # print(f"Current num: {current_num}\nNext num: {next_num}\n")

                # iterative step
                current_num = next_num
    return G, pos


if __name__ == "__main__":
    WEB_APP = True
    # web app
    if WEB_APP:
        matplotlib.use("Agg")  # allows background processing? not exactly sure how
        app.run(debug=True)

    LOCAL = not WEB_APP
    # or local
    if LOCAL:
        mod = int(sys.argv[1])
        mult = int(sys.argv[2])
        G, pos = generate_cardioid(mod=mod, mult=mult)
        # nx.draw_circular(G, with_labels=True)
        nx.draw(G, pos=pos, with_labels=True)
        plt.show()
