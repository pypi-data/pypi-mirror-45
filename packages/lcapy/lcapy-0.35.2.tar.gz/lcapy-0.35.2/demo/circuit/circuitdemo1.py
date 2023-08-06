from lcapy import Circuit

cct = Circuit()

cct.add('Vs 1 0 step') 
cct.add('Ra 1 2') 
cct.add('Rb 2 0') 


cct.Rb.V.pprint()
cct.Rb.v.pprint()

cct.Rb.I.pprint()
cct.Rb.i.pprint()

