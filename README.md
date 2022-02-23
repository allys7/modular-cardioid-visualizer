# Modular Cardioid Visualizer

This is a simple web app that I created after seeing [Mathologer's video](https://youtu.be/6ZrO90AI0c8) about Tesla's 'Vortex Mathematics', which he believed held the secret to the universe.
In reality, these shapes just come from mathematical properties relating to modular arithmetic.
I am (tangentially) learning about this in my introduction to cryptography class, so I figured it would be fun to implement the program that Mathologer mentioned in his video.
It was a good excuse for me to learn some about [Flask](https://palletsprojects.com/p/flask/) and [NetworkX](https://networkx.org/), two Python packages I used to generate the graph.

# Examples

![Modulus 282, multiplier 2](/static/283,2.png)
![Modulus 173, multiplier 4](/static/173,4.png)
![Modulus 842, multiplier 7](/static/842,7.png)

# Current Features

- Dynamic graph generation based on modulus and multiplier
- Edge coloring based on the 'distance' that it covers (e.g., from 1 to 5 is a distance of 4)
- Functional webapp

### Todo

- Color each loop individually
- Faster image generation
- Cleaner webapp UI

# Usage

I don't have a way to host this, since GitHub Pages won't serve dynamic pages. Instead, if you are interested in playing
with this, you can run the Flask server on your own machine by following the instructions below:

~~~
$ git clone https://github.com/allys7/modular-cardioid-generator.git
$ cd modular-cardioid-generator/
$ python -m pip venv env/
$ source ./env/bin/activate
$ pip install -r ./requirements.txt
~~~

If that is too much work for you and you just want to make pretty pictures,
check out these implementations by others:

[Owen Betchel](https://owenbechtel.com/games/times-tables/),
[Liam](https://tiusic.com/vortex.html)
