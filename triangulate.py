import pickle, json, os, sys, csv, random, operator
from collections import defaultdict, Counter, deque
import numpy as np
import pandas as pd
import igraph as ig
import networkx as nx
import seaborn as sns
import scipy.stats as scs
import matplotlib.pyplot as plt
import numpy.linalg as la
from itertools import combinations, product

def ig_to_nx(ig_graph, directed=False, nodes=None):
    """map igraph Graph object to networkx Graph object"""
    g = nx.DiGraph() if directed else nx.Graph()
    nodes = nodes if nodes else ig_graph.vs
    edges = ig_graph.induced_subgraph(nodes).es if nodes else ig_graph.es
    for node in nodes: g.add_node(node.index, **node.attributes())
    for edge in edges: g.add_edge(edge.source, edge.target)
    return g

def is_chordal_ig(g):
    g = ig_to_nx(g)
    return nx.is_chordal(g)

def triangulate_nx(g, debug=True):
    # Maximum Cardinality Search for Computing Minimal Triangulations of Graphs
    def has_proper_path(u, v):
        valid_nodes = [u,v]+[x for x in indices if w[x] < w[u]]
        subgraph = g.subgraph(valid_nodes)
        return nx.has_path(subgraph, u, v)

    F, alpha = set(), {}
    indices = {nid: 0 for nid in g.nodes()}
    w = indices.copy()

    for i in sorted(indices, reverse=True):
        if debug and i % 10 == 0: print i,
        v, S = max(indices.keys(), key=lambda x: w[x]), set()
        for u in indices:
            if (u!=v) and (g.has_edge(u,v) or has_proper_path(u, v)): S.add(u)
        for u in S:
            w[u] += 1
            if not g.has_edge(u,v):  F.add((u,v) if u<v else (v,u))
        alpha[v] = i
        del indices[v]

    h = g.copy()
    h.add_edges_from(list(F))
    return g, h, F

def triangulate_ig(g, debug=True):
    g_nx = ig_to_nx(g)
    g_nx, h_nx, F = triangulate_nx(g_nx, debug=debug)
    assert nx.is_chordal(h_nx)
    gc = g.copy()
    gc.add_edges(F)
    return gc