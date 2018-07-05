from nltk import Tree

# an example
tree = Tree('S',[Tree('NP',['Gary']),
                 Tree('VP',[Tree('VT',['plays']),
                            Tree('NP',['baseball'])])])
# tree.draw() # GUI window
tree.pprint()
print(type(tree))

# another exmaple
example = "(S (NP (Det the) (N dog)) (VP (V saw) (NP (NP (Det a) (N man) (PP (P in) (NP (Det the) (N park)))))))"
exampleTree = Tree.fromstring(example)
exampleTree.pprint()
