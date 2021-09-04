import numpy as np

def bellman_ford(nodes, edges, source_index = 0):

    """
    :param nodes: A list of integers from 0 to V-1
    :param edges: A dictionary of 2-tuples pointing to a float: (u,v) -> edge weight from u to v
    :param source_index: An integer from 0 to V-1
    :return: path_lengths (which is a dictionary v -> shortest path from source to v), paths (which is a dictionary v -> list of vertices forming shortest path from source to v)
    """

    path_lengths = {v: float('inf') for v in nodes}  # The value for each key v is the current shortest distance from source to v

    path_lengths[source_index] = 0  # Set the path length from source to source to 0

    paths = {v: [] for v in nodes}  # The value for each key v will be a list containing the current shortest path from source to v

    paths[source_index] = [source_index]  # Set the path from source to source to just a list containing the source

    for i in range(len(nodes)-1): # Iterate V-1 times, note below Bellman-Ford does not care which order you traverse the edges

        for (u, v), w_uv in edges.items():  # Edges is a dictionary with (u, v) as a key and w_uv as a value, edges.items returns a list where each element in the list is a 2-tuple with the first element being the key ie (u, v) and the second element is the value

            tmp = path_lengths[u] + w_uv  # Path length from source to u + weight from u to v

            if tmp < path_lengths[v]:  # If the path length from source to u + weight from u to v is less than path length from source to v then we update

                path_lengths[v] = tmp  # Make the update to a shortest path length value

                paths[v] = paths[u] + [v]  # Make the update to a better path

    for (u, v), w_uv in edges.items():

        if path_lengths[u] + w_uv < path_lengths[v]:  # The path_legnths dictionary is now optimised after V-1 iterations and should not find a better path_length to update unless there is a negative cycle, if it does then there is a negative cycle that would keep decreasing the path length to minus infinity

            print('Graph has a negative-weight cycle')
            break

    return path_lengths, paths


# 0 : euro, 1 : USD, 2 : GBP, 3 : Canada dollar

edges_tmp = {(0, 1): 1.1879, (1, 0): 0.8418, (0, 2): 0.85697, (2, 0): 1.1669, (0, 3): 1.737, (3, 0): 0.67181,
             (1, 2): 0.72143, (2, 1): 1.3861, (1, 3): 1.253, (3, 1): 0.79808, (2, 3): 1.7396, (3, 2): 0.57575}
edges = {(u, v): -np.log(w_uv) for (u, v), w_uv in edges_tmp.items()}
nodes = np.arange(0, max(max(edges_tmp.keys()))+1)  # The +1 is because upper limit is not inclusive in arange

path_lengths, paths = bellman_ford(nodes, edges, source_index=0)

print(paths)

# There can be a maximum of V-1 = 3 edges for each path if the graph contains no negative cycles
print(edges_tmp[(0,3)]*edges_tmp[(3,2)]*edges_tmp[(2,0)])


