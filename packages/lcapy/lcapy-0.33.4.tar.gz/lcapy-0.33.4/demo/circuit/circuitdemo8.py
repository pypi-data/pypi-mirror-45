from lcapy import Circuit

cct = Circuit()

cct.add('Vs 1 0 step 10') 
cct.add('R1 1 2 5') 
cct.add('C1 2 0 1 5') 
#cct.add('C1 2 0 1 0') 

cct.C1.V.pprint()

cct.C1.I.pprint()




