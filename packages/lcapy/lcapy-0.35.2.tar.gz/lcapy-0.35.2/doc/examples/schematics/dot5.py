from lcapy import Circuit
# This demonstrates the need for forward-backward averaging
a = Circuit('net2.sch')
s = a.sch
s.draw()
s.xgraph.dot()


