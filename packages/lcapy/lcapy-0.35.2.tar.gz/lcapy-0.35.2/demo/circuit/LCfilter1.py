from lcapy import Circuit, j, omega

cct = Circuit()

cct.add('P1 1 0; down')
cct.add('L1 1 2 0.2; right') 
cct.add('C1 2 3 1e-3; right') 
cct.add('R1 3 4 10; down') 
cct.add('W1 0 4; right') 
H = cct.transfer(1, 0, 3, 4)
A = H(j * omega)
A.magnitude.pprint()
A.phase.pprint()


