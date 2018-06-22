"""
author : takafumihoriuchi
created in June of 2018
"""
import nltk


def index_rules(grammar):
    pass
    return rules_l, rules_r



class Parser():
    
    def __init__(self, grammar):
        self.grammar = grammar
        self.rules_l, self.rules_r = index_rules(grammar)
        self.chart = []
        self.agenda = [] # list of tuples such as "(0, 1, NP, ('I',), 1, None)"


    # parse_strategy  = { 'bottom_up'     | 'top_down'    }
    # search_strategy = { 'breadth_first' | 'depth_first' }
    def parse(self, tokens, start_symbol='S',
              parse_strategy='bottom_up', search_strategy='breadth_first'):
        
        self.start_symbol = start_symbol
        self.initialize(tokens, start_symbol, parse_strategy, search_strategy)
        
        while (self.agenda):
            edge = self.agenda.pop(0)  # remove the item at the given position in the list, and return it
            print("from agenda", edge)
            self.process_edge(edge, parse_strategy, search_strategy)
        
        self.trees = self.make_trees(tokens)
        return self.trees


    def initialize(self, tokens, start_symbol, parse_strategy, search_strategy):
        pass


    def process_edge(self, edge, parse_strategy, search_strategy):
        add_to_chart(edge)
        if complete(edge) is False:
            forward_fundamental_rule(edge)
        else:
            backward_fundamental_rule(edge)
        make_predictions(edge)


    def add_to_chart(self, edge):
        pass


    def complete(self, edge):
        pass


    def forward_fundamental_rule(self, edge):
        pass


    def backward_fundamental_rule(self, edge):
        pass


    def add_to_agenda(self, edge):
        pass


    def make_predictions(self, edge):
        pass


    def top_down_predict(self):
        pass

    def bottom_up_preduct(self):
        pass

    # returns a list of trees, each in "nltk.tree.Tree" type
    def make_trees(self, tokens):
        pass



def main():

    grammar = nltk.CFG.fromstring("""
        S   -> NP VP
        PP  -> P NP
        NP  -> Det N | Det N PP | 'I'
        VP  -> V NP | VP PP
        Det -> 'an' | 'my'
        N   -> 'elephant' | 'pajamas'
        V   -> 'shot'
        P   -> 'in'
        """)
    """
    Out[11]: <Grammar with 13 productions>
    """
    parser = Parser(grammar)

    tokens = "I shot an elephant in my pajamas".split()
    """
    Out[10]: ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
    """
    
    bp_trees = parser.parse(tokens, parse_strategy='bottom_up')
    """
    from agenda (0, 1, NP, ('I',), 1, None)
    add_to_chart (0, 1, NP, ('I',), 1, None)
    [bwd fundamental] edge (0, 1, NP, ('I',), 1, None)
    [bu predict] triggered (0, 1, NP, ('I',), 1, None)
    append_to_agenda (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    append_to_agenda (0, 1, NP, (NP, PP), 1, [(0, 1, NP, ('I',), 1, None)])
    from agenda (1, 2, V, ('shot',), 1, None)
    add_to_chart (1, 2, V, ('shot',), 1, None)
    ....
    """
    print(len(bp_trees))
    """
    Out[14]: 2
    """

    tp_trees = parser.parse(tokens, parse_strategy='top_down')
    """
    from agenda (0, 0, S, (NP, VP), 0, [])
    add_to_chart (0, 0, S, (NP, VP), 0, [])
    [fwd fundamental] edge (0, 0, S, (NP, VP), 0, [])
    New edge (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    append_to_agenda (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    [td predict] triggered (0, 0, S, (NP, VP), 0, [])
    append_to_agenda (0, 0, NP, (Det, N), 0, [])
    append_to_agenda (0, 0, NP, (Det, NP), 0, [])
    append_to_agenda (0, 0, NP, (NP, PP), 0, [])
    append_to_agenda (0, 0, NP, (N, N), 0, [])
    append_to_agenda (0, 0, NP, ('I',), 0, [])
    append_to_agenda (0, 0, NP, ('time',), 0, [])
    from agenda (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    add_to_chart (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    [fwd fundamental] edge (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    [td predict] triggered (0, 1, S, (NP, VP), 1, [(0, 1, NP, ('I',), 1, None)])
    ...
    """
    print(len(tp_trees))
    """
    Out[16]: 2
    """



if __name__ == '__main__':
    main()
