from lcapy import Circuit
a = Circuit()
a.add('V1 1 0 ac; down')
a.add('R1 1 2; right')
a.add('L1 2 3 L1; down')
a.add('W 0 3; right')
#a.L1.v.pprint()


