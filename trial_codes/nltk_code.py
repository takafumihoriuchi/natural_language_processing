import nltk


print("\n--- Ambiguous Grammar ---")

groucho_grammar = nltk.CFG.fromstring("""
	S -> NP VP
	PP -> P NP
	NP -> Det N | Det N PP | 'I'
	VP -> V NP | VP PP
	Det -> 'an' | 'my'
	N -> 'elephant' | 'pajamas'
	V -> 'shot'
	P -> 'in'
	""")

sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
parser = nltk.ChartParser(groucho_grammar)
trees = parser.parse(sent)
for tree in trees:
	print(tree)

"""
(S
  (NP I)
  (VP
    (VP (V shot) (NP (Det an) (N elephant)))
    (PP (P in) (NP (Det my) (N pajamas)))))
(S
  (NP I)
  (VP
    (V shot)
    (NP (Det an) (N elephant) (PP (P in) (NP (Det my) (N pajamas))))))
"""


print("\n--- Recursive Descent Parsing ---")

grammar1 = nltk.CFG.fromstring("""
	S -> NP VP
	VP -> V NP | V NP PP
	PP -> P NP
	V -> "saw" | "ate" | "walked"
	NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
	Det -> "a" | "an" | "the" | "my"
	N -> "man" | "dog" | "cat" | "telescope" | "park"
	P -> "in" | "on" | "by" | "with"
	""")

sent = "Mary saw Bob".split()
rd_parser = nltk.RecursiveDescentParser(grammar1)
for tree in rd_parser.parse(sent):
	print(tree)

"""
(S (NP Marry) (VP (V saw) (NP Bob)))
"""


print("\n--- Shift Reduce Parsing ---")

sent = "Mary saw a dog".split()
sr_parser = nltk.ShiftReduceParser(grammar1, trace=2)
for tree in sr_parser.parse(sent):
	print(tree)

