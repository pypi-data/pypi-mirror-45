from lcapy import Circuit
a = Circuit('buffers.sch')
s = a.sch
s.draw()
s.ygraph.dot(stage=2)


