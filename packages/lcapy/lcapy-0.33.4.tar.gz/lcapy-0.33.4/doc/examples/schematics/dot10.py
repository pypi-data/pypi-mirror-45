from lcapy import Circuit
a = Circuit('cmos1.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


