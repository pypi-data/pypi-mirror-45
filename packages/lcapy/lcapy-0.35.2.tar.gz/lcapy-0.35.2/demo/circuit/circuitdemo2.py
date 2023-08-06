from lcapy import Circuit

cct = Circuit()

cct.add('V_s fred 0 step') 
cct.add('R_a fred bert') 
cct.add('R_b bert 0') 


cct.R_b.V.pprint()

cct.R_b.I.pprint()




