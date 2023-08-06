from lcapy import Circuit

cct = Circuit()

cct.add('V1 1 0 acstep 10 100') 
cct.add('R1 1 2 5') 
cct.add('C1 2 0 1') 


cct.C1.V.pprint()

cct.C1.I.pprint()

