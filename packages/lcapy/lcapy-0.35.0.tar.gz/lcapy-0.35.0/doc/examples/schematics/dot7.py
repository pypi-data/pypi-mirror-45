from lcapy import Circuit
a = Circuit('ic2.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


