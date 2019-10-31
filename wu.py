import pickle, json, os, sys, csv, random, operator
from collections import defaultdict, Counter, deque
import numpy as np
import pandas as pd
import igraph as ig
import networkx as nx
import scipy.stats as scs
from itertools import combinations, product

def get_elimination_ordering(g):
    weights = {nid: 0 for nid in g.vs.indices}
    alpha = {}
    for k in xrange(len(g.vs)):
        max_nid = max(weights, key=lambda k: weights[k])
        for nb in g.vs[max_nid].neighbors():
            if nb.index in weights: weights[nb.index] += 1
        alpha[max_nid] = k
        del weights[max_nid]

    inv_alpha = {v:k for k,v in alpha.items()} # order value -> nid
    _, order = zip(*sorted(inv_alpha.items()))
    return order

def get_cj_values_from_order(g, order=None):
    if not order: order = get_elimination_ordering(g)
    cj = {}
    for i, o1 in enumerate(order):
        nbors = set([nb.index for nb in g.vs[o1].neighbors()])
        count = 0.
        for j in xrange(i):
            if j in nbors: count += 1
        cj[o1] = count
    return cj

def unsmoothed_estimator(p, cj_vals):
    count = 0.
    c = (p-1)/p
    for cj in cj_vals:
        count += c**cj
    return count/p

def smoothed_estimator(p, cj_vals, N, d, w):
    mu = p/(2-3*p)*abs(np.log((N*p)/(1+ d*w)))
    def get_weight(k):
        if p > 0.5: return 1
        return 1.-scs.poisson.cdf(k, mu)

    count = 0.
    c = (p-1)/p

    for cj in cj_vals:
        count += (c**cj)*get_weight(cj)
    return count/p







