# This demonstrates the need for forward-backward averaging
from lcapy import Circuit
a = Circuit('net1.sch')
s = a.sch
s.draw()
s.xgraph.dot()


