from lcapy import Circuit
from matplotlib.pyplot import subplots
import networkx as nx

class Circuitgraph(nx.Graph):

    def __init__(self, cct):

        super(Circuitgraph, self).__init__()
        self.cct = cct

        self.add_nodes_from(cct.node_list)

        node_map = cct.node_map

        for name in cct.branch_list:
            elt = cct.elements[name]
            if len(elt.nodes) < 2:
                continue
            self.add_edge(node_map[elt.nodes[0]], node_map[elt.nodes[1]], name=name)

    def loops(self):
        
        DG = nx.DiGraph(G)
        cycles = list(nx.simple_cycles(DG))

        loops = []
        for cycle in cycles:
            if len(cycle) > 2:
                cycle = sorted(cycle)
                if cycle not in loops:
                    loops.append(cycle)        
        return loops

    def draw(self):
        """Use matplotlib to draw circuit graph."""

        fig, ax = subplots(1)
        
        pos = nx.spring_layout(G)
        
        labels = dict(zip(G.nodes(), G.nodes()))
        nx.draw_networkx(G, pos, ax, labels=labels)
        
        edge_labels=dict([((u, v), d['name'])
                          for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        
cct = Circuit("""                                                       
V1 1 0 {u(t)}; down
R1 1 2 4; right=2
L1 2 3 0.5; down=2
W1 0 3; right
""")


G = Circuitgraph(cct)

G.draw()

# Print nodes in loops
for loop in G.loops():
    print(loop)

# Print which node connects to which
for node in G:
    for edge in G[node]:
        print(node, G[node][edge]['name'])
