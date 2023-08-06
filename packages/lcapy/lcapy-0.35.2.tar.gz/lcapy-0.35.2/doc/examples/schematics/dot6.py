from lcapy import Circuit
a = Circuit('opamp-differential-amplifier1.sch')
s = a.sch
s.draw()
s.ygraph.dot()


