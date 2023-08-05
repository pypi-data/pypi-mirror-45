import networkx
from networkx import Graph, DiGraph, simple_cycles

# construct a graph using a dict: {node:[connected_nodes]}
G = Graph(
    {'A':['B','G','H'],
     'B':['A','C','D'],
     'C':['B','D','E'],
     'D':['B','C','E','F','G', 'H'],
     'E':['C','D','F'],
     'F':['D','E','G'],
     'G':['A','D','F','H'],
     'H':['A','D','G'],
    }
)

# optional: draw the graph for verification
labels = dict(zip(G.nodes(),G.nodes()))
networkx.draw_networkx(G,labels=labels)

# simple_cycles only accepts DiGraphs. convert G to a bi-directional
# digraph. note that every edge of G will be included in this list!
DG = DiGraph(G)
list(simple_cycles(DG))
