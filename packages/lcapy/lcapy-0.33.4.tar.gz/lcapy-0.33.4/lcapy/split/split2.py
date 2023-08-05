# This works since other classes known when they are instantiated

class A(object):

    def __init__(self):
        self.conj = B


class B(object):

    def __init__(self):
        self.conj = A
    
    
    
