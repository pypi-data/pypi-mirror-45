from lcapy import pprint, Circuit

cct = Circuit()

cct.add('Is 1 0 -10') 
cct.add('R1 1 0 5') 


pprint(cct.V)

pprint(cct.I)



