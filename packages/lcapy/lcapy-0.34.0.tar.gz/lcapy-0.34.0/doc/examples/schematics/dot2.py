from lcapy import Circuit
a = Circuit('opamp-inverting-amplifier2.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


