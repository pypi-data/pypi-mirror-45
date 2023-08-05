from lcapy import Circuit
a = Circuit('opamp5.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


