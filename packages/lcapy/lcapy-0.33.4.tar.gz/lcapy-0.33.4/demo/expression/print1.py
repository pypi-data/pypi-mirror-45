from lcapy import Vdc, R, L, C, pprint
import numpy as np
from matplotlib.pyplot import figure, savefig, show

a = (Vdc(5) + L(10)) | C(1, 5)
b = a.load(R(5))


print('general')
b.V.general().pprint()

print('canonical')
b.V.canonical().pprint()

print('ZPK')
b.V.ZPK().pprint()

print('partfrac')
b.V.partfrac().pprint()

print('mixedfrac')
b.V.mixedfrac().pprint()


