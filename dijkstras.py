import networkx as nx # used for drawing the graph as a plot
import numpy as np
import matplotlib.pyplot as plt

G_1 = [[0, 9, 0, 0], [0, 0, 0, 13], [0, 7, 0, 6], [0, 0, 0, 0]] # graph is represented by a matrix where row is starting node of edge and column is finishing node of edge
N = 4
G_2 = np.random.rand(N, N)*10
G_2 = np.around(G_2, decimals = 1)
G_2 = G_2.tolist()
for i in range(N):
    G_2[i][i] = 0

def dijkstras(G, s):

    N = len(G) # the number of nodes
    t_d = [np.inf]*N # tentative distance list, this list will hold the distance to each node from the source s at any given point in the algorithm
    nums = np.arange(0, N) # just a list of numbers from 0 to N-1, these are the labels of the nodes
    visited = [] # list to hold visited nodes
    t_d[s] = 0 # tentative distance of source is 0 because we start from there
    current = s # set the current node to the source s where we start
    d_d = {}  # distance dictionary to select which unvisited node to visit next after we calculate the distance to each neighbour from the current node

    while True: # this will run forever unless there is code below inside the while loop to break the while loop

        for n in nums: # for all possible neighbours

            if G[current][n] != 0 and n not in visited: # if it is actually a neighbour and has not been visited
                if t_d[n] > t_d[current] + G[current][n]: # if the current tentative distance is bigger than the new distance found
                    t_d[n] = t_d[current] + G[current][n] # update tentative distance to new distance found

                d_d[n] = t_d[n] # set the neighbour with index n to point to its tentative distance in this dictionary

        visited.append(current) # put the current node in the visited list so we dont visit it again
        if len(visited) == N: # if we have visited all nodes we have finished the algorithm
            break

        min_unvisited = np.inf  # if this remains infinity after the for loop below it means there is no connection
        for n in nums:
            if n in visited:
                continue
            else:  # if the minimum of the tentative distances of the unvisited nodes is not infinity we can keep going
                min_unvisited = t_d[n]
                break
        if min_unvisited == np.inf:  # if the minimum of the tentative distances of the unvisited nodes is infinite it means there is no edge connecting the source to any other neighbour
            break

        min_val = min(d_d.values()) # we will visit the univisited node with the smallest tentative distance next
        current = list([n for n in d_d.keys() if d_d[n] == min_val])[0] # find the index of the node which has not been visited, is a neighbour of the current node and has the smallest tentative distance
        d_d.pop(current) # d_d stores only unvisited nodes -> tentative distance so we remove the node we are about to visit next

    # Below is for displaying the result of the tentative distance from the source s to each other node
    result = {}
    for n in range(N):
        result[f'{s} -> {n}'] = np.round(t_d[n], decimals = 1)

    print('The shortest distance between {s} and every other node is shown below.')
    print(result)

def my_draw_networkx_edge_labels(G,pos,edge_labels=None,label_pos=0.5,font_size=10,font_color="k",font_family="sans-serif",font_weight="normal",alpha=None,bbox=None,horizontalalignment="center",verticalalignment="center",ax=None,rotate=True,clip_on=True,rad=0):

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5*pos_1 + 0.5*pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0,1), (-1,0)])
        ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
        ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
        ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
        bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items

def visualize_graph(G): # To draw the graph G as a plot

    N = len(G)
    g = nx.DiGraph()
    for i in range(N):
        g.add_node(i)
    for row in range(N):
        for col in range(N):
            if G[row][col] == 0:
                continue
            else:
                g.add_edge(row, col, weight = G[row][col])

    pos = nx.spring_layout(g, seed = 6)
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(g, pos, ax=ax)
    nx.draw_networkx_labels(g, pos, ax=ax)
    curved_edges = [edge for edge in g.edges() if reversed(edge) in g.edges()]
    straight_edges = list(set(g.edges()) - set(curved_edges))
    nx.draw_networkx_edges(g, pos, ax=ax, edgelist=straight_edges)
    arc_rad = 0.25
    nx.draw_networkx_edges(g, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')
    edge_weights = nx.get_edge_attributes(g, 'weight')
    curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
    straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
    my_draw_networkx_edge_labels(g, pos, ax=ax, edge_labels=curved_edge_labels, rotate=False, rad = arc_rad)
    nx.draw_networkx_edge_labels(g, pos, ax=ax, edge_labels=straight_edge_labels, rotate=False)
    plt.show()

print('------------------------------- Solution for G_1 -------------------------------\n')
dijkstras(G_1, 0)
visualize_graph(G_1)
print('\n------------------------------- Solution for G_2 -------------------------------\n')
print('G_2 is shown below\n')
print(np.asarray(G_2))
print()
dijkstras(G_2, 2)
visualize_graph(G_2)



