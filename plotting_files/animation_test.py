from matplotlib import pyplot as plt, animation
import networkx as nx
import random

data, ids, addresses = get_opensea_trade_data(series)

plt.rcParams["figure.figsize"] = [8, 8]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()


G = nx.DiGraph()
G.add_nodes_from([0, 1, 2, 3, 4, 5])
pos = nx.spring_layout(G, seed=4)

nx.draw(G, pos = pos, with_labels=True)

def animate(frame):
   fig.clear()
   num1 = random.randint(0, 5)
   num2 = random.randint(0, 5)
   G.add_edges_from([(num1, num2)])
   nx.draw(G, pos = pos, with_labels=True)

ani = animation.FuncAnimation(fig, animate, frames=6, interval=100, repeat=True)

plt.show()