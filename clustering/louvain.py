import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def generate_network(n):
    '''
    This function will generate a random weighted network associated to the user specifed
    number of nodes. 
    
    params:
        n (Integer) : The number of nodes you want in your network
    
    returns:
        A networkX multi-graph
        
    example:
        G = generate_network(n)
    '''
    # initialize dictionary with nodes
    graph_dct = {node:[] for node in range(n)}
    nodes = list(range(n))
    
    # generate edges
    for n,edge_list in graph_dct.items():
        edge_c = random.randint(min(nodes), int(max(nodes) / 2))
        el = random.sample(nodes, edge_c)
        graph_dct[n] = el
    
    # create networkx multi-edge graph
    G = nx.MultiGraph(graph_dct)
    return G

n = 50
G = generate_network(n)
# print(nx.info(G))

# visualize graph
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size = 75, alpha = 0.8)
plt.show()

# apply louvain algorithm
partition = nx.algorithms.community.louvain_communities(G)
communities = list(partition)

# color nodes by community
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'black', 'pink', 'brown', 'gray']
color_map = []
for node in G:
    for community in communities:
        if node in community:
            color_map.append(colors[communities.index(community)])

# visualize graph
nx.draw(G, pos, node_color = color_map, node_size = 75, alpha = 0.8)
plt.show()