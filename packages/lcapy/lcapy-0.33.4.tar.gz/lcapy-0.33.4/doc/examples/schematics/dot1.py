from lcapy import Circuit
a = Circuit('net1.sch')
s = a.sch
s.draw()
s.xgraph.dot(stage=2)

