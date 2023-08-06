# This does not work since static attributes need to be defined in advance.

class A(object):

    conj = B


class B(object):

    conj = A

    
    
    
