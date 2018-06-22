"""
author : takafumihoriuchi
created in June of 2018
"""
import nltk





def init_wfst(tokens, grammar):
    num_tokens = len(tokens)
    wfst = [[None for i in range(num_tokens + 1)] for j in range(num_tokens + 1)]
    # [[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
    for i in range(num_tokens):
        productions = grammar.productions(rhs=tokens[i]) # production rule that right-hand-side is i-th token
        # [NP -> 'I'] # when i=0
        wfst[i][i+1] = productions[0].lhs() # 'productions' can contain several ruls # why is it [0] here?
    return wfst


def complete_wfst(wfst, tokens, grammar, trace=False):
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions()) # create dict of (key, value) => key: value
    # {(NP, VP): S, (P, NP): PP, (Det, N): NP, (Det, N, PP): NP, ('I',): NP, (V, NP): VP, (VP, PP): VP, ('an',): Det, ('my',): Det, ('elephant',): N, ('pajamas',): N, ('shot',): V, ('in',): P}
    num_tokens = len(tokens)
    for span in range(2, num_tokens + 1):
        for start in range(num_tokens + 1 - span):
            end = start + span
            for mid in range(start + 1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                if (nt1 and nt2 and (nt1,nt2)) in index:
                    wfst[start][end] = index[(nt1,nt2)]
                    if trace:
                        print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % \
                        (start, nt1, mid, nt2, end, start, index[(nt1,nt2)], end))
    return wfst


def display(wfst, tokens):
    print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(wfst))))
    for i in range(len(wfst)-1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-4s" % (wfst[i][j] or '.'), end=" ")
        print()







def index_rules(grammar):
    pass
    # return rules_l, rules_r


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
            current_edge = self.agenda.pop(0)  # remove the item at the given position in the list, and return it
            print("from agenda", current_edge)
            self.process_edge(current_edge, parse_strategy, search_strategy)
        
        self.trees = self.make_trees(tokens)
        return self.trees


    def initialize(self, tokens, start_symbol, parse_strategy, search_strategy):
        # 作ったstate(edge)をagendaに追加していく。
        # この追加の仕方が戦略によって変化する
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

    tokens = "I shot an elephant in my pajamas.".strip(".").split()

    # wfst is the base of chart-parser
    # WFST = Well-Formed Substring Table
    wfst0 = init_wfst(tokens, grammar)
    display(wfst0, tokens)
    print()
    wfst1 = complete_wfst(wfst0, tokens, grammar, trace=True)
    display(wfst1, tokens)
    print()


    # parser = Parser(grammar)
    
    # bp_trees = parser.parse(tokens, parse_strategy='bottom_up')
    
    #  ( where-state-begins, where-dot-lies, simbol-on-left, simbol-on-right-(,) , 1, []) 
    """
    from agenda             (0, 1, NP, ('I',)    , 1, None                          )
    add_to_chart            (0, 1, NP, ('I',)    , 1, None                          )
    [bwd fundamental] edge  (0, 1, NP, ('I',)    , 1, None                          )
    [bu predict] triggered  (0, 1, NP, ('I',)    , 1, None                          )
    append_to_agenda        (0, 1, S , (NP, VP)  , 1, [(0, 1, NP, ('I',), 1, None)] )
    append_to_agenda        (0, 1, NP, (NP, PP)  , 1, [(0, 1, NP, ('I',), 1, None)] )
    from agenda             (1, 2, V , ('shot',) , 1, None                          )
    add_to_chart            (1, 2, V , ('shot',) , 1, None                          )
    ....
    """
    # print(len(bp_trees))
    """
    Out[14]: 2
    """

    # tp_trees = parser.parse(tokens, parse_strategy='top_down')
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
    # print(len(tp_trees))
    """
    Out[16]: 2
    """

    # nltk sample
    # parser = nltk.ChartParser(grammar)
    # for tree in parser.parse(tokens):
    #     print(tree)
    """
    ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
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



if __name__ == '__main__':
    main()

"""
参考：
https://www.inf.ed.ac.uk/teaching/courses/anlp/lectures/15/
"""