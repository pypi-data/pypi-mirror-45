from lcapy import *
from numpy import logspace
from matplotlib.pyplot import figure, savefig, show

N = Vstep(20) + R(5) + C(10)
f = logspace(-2, 4, 400)
Isc = N.Isc

fig = figure()
ax = fig.add_subplot(111)
ax.loglog(f, abs(Isc.frequency_response(f)), linewidth=2)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Current (A/Hz)')
ax.grid(True)
show()

savefig('series-RLC-frequency1.png')
