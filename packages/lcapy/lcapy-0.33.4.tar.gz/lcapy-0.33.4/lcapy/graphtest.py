from lcapy import Circuit
from lcapy.circuitgraph import Circuitgraph
from lcapy.nodalanalysis import Nodalanalysis
        
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


nodal = Nodalanalysis(cct)
