# https://stackoverflow.com/questions/53161395/how-to-draw-networkx-graph-in-flask

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
    G = generate_cardioid(mod, mult)

    nx.draw(G, with_labels=True)

    # generate & return image
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    plt.clf()

    return send_file(img, mimetype="image/png")


def generate_cardioid(mod, mult):
    G = nx.DiGraph()
    return G


if __name__ == "__main__":
    app.run(debug=True)
