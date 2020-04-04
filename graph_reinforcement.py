from collections import defaultdict
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Graph():

    # Store all paths from a starting vertex to a finish vertex
    paths = []

    def __init__(self, order):
        # Order of a graph is the number of vertices
        self.order = order
        # Store the graph as dictionary with keys being
        # the nodes and values being their neighbours in a list
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        # u points to v
        self.graph[u].append(v)

    def _get_all_paths(self, current_node, finish, visited, path):
        visited[current_node] = True
        path.append(current_node)
        if current_node == finish:
            self.paths.append(tuple(path))
        else:
            for neighbor in self.graph[current_node]:
                if visited[neighbor] == False:
                    # Once the depth traversal finishes for the first neighbour in this loop
                    # the function starts from here and evaluates visited[neighbour] = True and starts
                    # poping items (ie start walking back the path until it finds a node with an unexplored
                    # neighbour and the depth traversal starts again
                    self._get_all_paths(neighbor, finish, visited, path)
        # Pop removes the last item inserted which is the last element of path
        path.pop()
        visited[current_node] = False

    def get_all_paths(self, start, finish):
        visited = [False]*self.order
        path = []
        self._get_all_paths(start, finish, visited, path)
        return self.paths

    def draw_graph(self):
        g = nx.DiGraph()
        for i in range(15):
            g.add_node(i)
        g.add_edge(0, 2)
        g.add_edge(2, 1)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        g.add_edge(3, 5)
        g.add_edge(4, 5)
        g.add_edge(5, 8)
        g.add_edge(5, 7)
        g.add_edge(7, 6)
        g.add_edge(7, 10)
        g.add_edge(10, 11)
        g.add_edge(10, 12)
        g.add_edge(11, 9)
        g.add_edge(11, 13)
        g.add_edge(12, 14)
        nx.draw_networkx(g)

# Build graph
g = Graph(15)
g.add_edge(0, 2)
g.add_edge(2, 1)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(3, 5)
g.add_edge(4, 5)
g.add_edge(5, 8)
g.add_edge(5, 7)
g.add_edge(7, 6)
g.add_edge(7, 10)
g.add_edge(10, 11)
g.add_edge(10, 12)
g.add_edge(11, 9)
g.add_edge(11, 13)
g.add_edge(12, 14)
g.draw_graph()
plt.show()

paths_dict = {}  # Store in this dictionary all possible paths from 0 to a dead-end in the graph
end_nodes = [1, 6, 8, 9, 13, 14]  # Dead-end nodes
for end_node in end_nodes:
    start = 0
    finish = end_node
    paths_dict[end_node] = g.get_all_paths(start, finish)
    g.paths = []

all_paths = [paths_dict[key] for key in list(paths_dict.keys())]
all_paths_flat = []
for i in range(len(all_paths)):
    for path in all_paths[i]:
        all_paths_flat.append(list(path))


def get_reward_matrix(finish, g):
    reward_matrix = np.array(np.ones(shape=(g.order, g.order), dtype='int'))
    reward_matrix *= 0
    for i in range(g.order):
        if len(g.graph[i]) != 0:
            for neighbour in g.graph[i]:
                if neighbour == finish:
                    reward_matrix[i][neighbour] = 100
                else:
                    reward_matrix[i][neighbour] = -1
    return reward_matrix


def reinforcement_learning(paths):
    scores = {}
    reward_matrix = get_reward_matrix(14, g)
    for path in paths:
        score = 0
        for i in range(len(path) - 1):
            current = path[i]
            next = path[i+1]
            score += reward_matrix[current][next]
        scores[score] = path
    max_score = max(list(scores.keys()))
    return scores[max_score]


print('The shortest path based on a reinforcement reward system is: ')
print(reinforcement_learning(all_paths_flat))
