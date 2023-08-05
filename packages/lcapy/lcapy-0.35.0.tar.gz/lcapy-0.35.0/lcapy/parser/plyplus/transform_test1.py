from plyplus import Grammar, STransformer
from grammar4 import grammar
#from grammar3 import grammar
#from grammar2 import grammar

parser = Grammar(grammar)



class Transformer(STransformer):

    def rname(self, node):
        print(node.head, node.tail)

    def object(self, node):
        result = {}
        for i in node.tail:
            result.update( i )
   

r = parser.parse('R1 2 3 4')

t = Transformer().transform(r)
