import igraph as ig
import networkx as nx
import numpy as np
import random
import pickle
from triangulate import triangulate_ig, is_chordal_ig
"""
Generate Graph of size N with K components
Each component is sampled from ER(N/K, p)
"""

def get_er_graph(n,p,chordal=False):
    g = ig.Graph.Erdos_Renyi(n, p=p)
    if chordal: return triangulate_ig(g, debug=False)
    return g

def get_er_components_graph(num_comp, comp_size, p, chordal=False):
    g = ig.Graph()

    for comp_idx in xrange(num_comp):
        num_nodes = len(g.vs)
        new_comp = get_er_graph(comp_size, p, chordal=chordal)

        new_nodes = len(new_comp.vs)
        new_edges = [(e.source, e.target) for e in new_comp.es]
        new_edges = [(s+num_nodes, t+num_nodes) for s,t in new_edges]

        g.add_vertices(new_nodes)
        g.add_edges(new_edges)

    return g

def get_unif_sample(g, p):
    nodes = [n for n in g.vs if random.random() < p]
    return g.subgraph(nodes)

def get_subsampled_data(g, every=1):
    subsampled = {p: get_unif_sample(g,p) for p in np.loadtxt('ER/probs.txt')[::every]}
    return subsampled