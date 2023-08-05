"""
This module defines the components for modified nodal analysis.  The components
are defined at the bottom of this file.

Copyright 2015, 2016 Michael Hayes, UCECE

"""

from __future__ import print_function
import numpy as np


class Cpt(object):

    def stamp(self, cct, **kwargs):
        raise NotImplementedError('stamp method not implemented for %s' % self)


class NonLinear(object):

    def stamp(self, cct, **kwargs):
        raise NotImplementedError('cannot analyse non-linear component %s' % self)


class TimeVarying(object):

    def stamp(self, cct, **kwargs):
        raise NotImplementedError('cannot analyse time-varying component %s' % self)


class OpenCircuit(object):

    def stamp(self, cct, **kwargs):
        pass


class Resistor(object):


classes = {}

def defcpt(name, base, docstring):
    
    if isinstance(base, str):
        base = classes[base]

    newclass = type(name, (base, ), {'__doc__': docstring})

    classes[name] = newclass


# Dynamically create classes.

defcpt('C', Capacitor, 'Capacitor')

defcpt('D', NonLinear, 'Diode')
defcpt('Dled', 'D', 'LED')
defcpt('Dphoto', 'D', 'Photo diode')
defcpt('Dschottky', 'D', 'Schottky diode')
defcpt('Dtunnel', 'D', 'Tunnel diode')
defcpt('Dzener', 'D', 'Zener diode')

defcpt('E', VCS, 'VCVS')
defcpt('Eopamp', Opamp, 'Opamp')
defcpt('Efdopamp', FDOpamp, 'Fully differential opamp')
defcpt('F', VCS, 'VCCS')
defcpt('G', CCS, 'CCVS')
defcpt('H', CCS, 'CCCS')

defcpt('I', CurrentSource, 'Current source')
defcpt('Isin', 'I', 'Sinusoidal current source')
defcpt('Idc', 'I', 'DC current source')
defcpt('Iac', 'I', 'AC current source')

defcpt('J', NonLinear, 'N JFET transistor')
defcpt('Jnjf', 'J', 'N JFET transistor')
defcpt('Jpjf', 'J', 'P JFET transistor')

defcpt('L', OnePort, 'Inductor')

defcpt('M', NonLinear, 'N MOSJFET transistor')
defcpt('Mnmos', 'M', 'N channel MOSJFET transistor')
defcpt('Mpmos', 'M', 'P channel MOSJFET transistor')

defcpt('O', OpenCircuit, 'Open circuit')
defcpt('P', OpenCircuit, 'Port')

defcpt('Q', NonLinear, 'NPN transistor')
defcpt('Qpnp', 'Q', 'PNP transistor')
defcpt('Qnpn', 'Q', 'NPN transistor')

defcpt('R', Resistor, 'Resistor')

defcpt('SW', TimeVarying, 'Switch')
defcpt('SWno', 'SW', 'Normally open switch', 'closing switch')
defcpt('SWnc', 'SW', 'Normally closed switch')
defcpt('SWpush', 'SW', 'Pushbutton switch')

defcpt('TF', Transformer, 'Transformer')
defcpt('TP', TwoPort, 'Two port')

defcpt('V', VoltageSource, 'Voltage source')
defcpt('Vsin', 'V', 'Sinusoidal voltage source')
defcpt('Vdc', 'V', 'DC voltage source')
defcpt('Vstep', 'V', 'Step voltage source')
defcpt('Vac', 'V', 'AC voltage source')

defcpt('W', Wire, 'Wire')
defcpt('Y', Admittance, 'Admittance')
defcpt('Z', Impedance, 'Impedance')
