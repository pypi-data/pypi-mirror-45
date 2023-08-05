from lcapy import Circuit

cct = Circuit()

# Non-inverting opamp
cct.add('Vs 1 0 step 10') 
# Cannot have floating voltage source so tie to ground with arbitrary R
cct.add('Ri 1 0') 
cct.add('R1 2 0') 
cct.add('R2 3 2') 
cct.add('E1 3 0 2 1 1e6') 


cct.E1.V.pprint()

cct.E1.I.pprint()


