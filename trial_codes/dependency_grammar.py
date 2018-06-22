import nltk


groucho_dep_grammar = nltk.DependencyGrammar.fromstring("""
	'shot' -> 'I' | 'elephant' | 'in'
	'elephant' -> 'an' | 'in'
	'in' -> 'pajamas'
	'pajamas' -> 'my'
	""")

pdp = nltk.ProjectiveDependencyParser(groucho_dep_grammar)

sent = "I shot an elephant in my pajamas".split()

trees = pdp.parse(sent)

for tree in trees:
	print(tree)
