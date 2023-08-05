from lcapy import Circuit
a = Circuit('ic1.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


