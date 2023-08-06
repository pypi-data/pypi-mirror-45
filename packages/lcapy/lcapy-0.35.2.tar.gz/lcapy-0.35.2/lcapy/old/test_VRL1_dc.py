from lcapy import Circuit
a = Circuit()
a.add('V1 1 0')
a.add('R1 1 2')
a.add('L1 2 0 L1 {V1 / R1}')
#a.L1.v.pprint()


