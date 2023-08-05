# This demonstrates a group of nodes that require a fixed relationship.
# Forward-backward averaging will break the relationship.
from lcapy import Circuit
a = Circuit('opamp-inverting-amplifier3.sch')
s = a.sch
s.draw()
s.ygraph.dot()


