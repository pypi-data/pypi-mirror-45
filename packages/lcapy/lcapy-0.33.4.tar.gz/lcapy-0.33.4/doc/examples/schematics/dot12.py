from lcapy import Circuit
a = Circuit('Q1c.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


