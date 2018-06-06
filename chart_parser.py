def index_rules(grammar):
	pass


class parser():
	
	def __init__(self, grammar):
		self.grammar = grammar
		self.rules_l, self.rules_r = index_rules(grammar)
		self.chart = []
		self.agenda = []

	def parse(self, tokens, start_symbol='S', strategy=BU, search=BF):
		self.start_symbol = start_symbol
		self.__initialize(tokens, start_symbol, strategy, search)
		while (self.agenda):
			edge = self.agenda.pop(0)
			print("from agenda", edge)
			self.__process_edge(edge, strategy, search)
		self.trees = self.__make_trees(tokens)
		return self.trees

	def __initialize(self, tokens, start_symbol, strategy, search):
		pass

	def __process_edge(edge, strategy, search):
		pass

	def __make_trees(tokens):
		pass


def main():
	pass


if __name__ == '__main__':
	main()
