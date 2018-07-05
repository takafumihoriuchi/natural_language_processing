"""
author : takafumihoriuchi
created in July of 2018
"""
import nltk


# def index_rules(grammar):
#     pass
#     return rules_l, rules_r


def push(stack, state):
    stack.insert(0, state)


class Parser():
    
    def __init__(self, grammar):
        self.grammar = grammar
        # self.rules_l, self.rules_r = index_rules(grammar)
        self.chart = []
        self.agenda = [] # list of tuples such as "(0, 1, NP, ('I',), 1, None)"


    # parse_strategy  = { 'bottom_up'     | 'top_down'    }
    # search_strategy = { 'breadth_first' | 'depth_first' }
    def parse(self, tokens, start_symbol='S',
              parse_strategy='bottom_up', search_strategy='breadth_first'):
        
        self.start_symbol = start_symbol
        self.__initialize(tokens, start_symbol, parse_strategy, search_strategy)

        while (self.agenda):
            edge = self.agenda.pop(0)  # pop from agenda
            print("from agenda", edge)
            self.__process_edge(edge, parse_strategy, search_strategy)

        # self.__check_success()
        print(self.chart)
        self.trees = self.__make_trees(tokens)
        return self.trees


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __initialize(self, tokens, start_symbol, parse_strategy, search_strategy):
        for i in reversed(range(len(tokens))): # change this depending on pushing to stack or queue, want 'I' at top, and 'pajamas' on the bottom
            print(i)
            rule = self.grammar.productions(rhs=tokens[i])[0]
            dot_progress = len(rule.rhs())
            begin_idx = i
            dot_idx = i + 1
            passive_edge = (rule, dot_progress, begin_idx, dot_idx)
            self.__add_to_agenda(passive_edge)



   # def __check_success(self):
   #      pass


    def __process_edge(self, edge, parse_strategy, search_strategy):
        self.__add_to_chart(edge)
        if self.__is_complete(edge) is False:  # edge is an active arc
            self.__forward_fundamental_rule(edge)
        else:
            self.__backward_fundamental_rule(edge)  # edge is a passive arc
        self.__make_predictions(edge, parse_strategy)


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __is_complete(self, edge):
        rhs_length = len(edge[0].rhs())
        dot_progress = edge[1]
        return (rhs_length == dot_progress)


    def __add_to_chart(self, edge):
        if edge not in self.chart:
            self.chart.insert(0, edge)  # push to chart


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __forward_fundamental_rule(self, edge):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.rhs()[dot_progress]
        succeeding_edges = self.__get_all_matching_edges(calling_fun='ff', stack=self.chart, rule_lhs=B, begin_idx=dot_idx)
        for each_edge in succeeding_edges:
            new_rule = current_rule
            new_dotp = dot_progress + 1
            new_bidx = begin_idx
            new_didx = each_edge[3]
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge)


    def __backward_fundamental_rule(self, edge):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.lhs()
        precedent_edges = self.__get_all_matching_edges(calling_fun='bf', stack=self.chart, rule_rhs=B, dot_idx=begin_idx)
        for each_edge in precedent_edges:
            new_rule = each_edge[0]
            new_dotp = each_edge[1] + 1
            new_bidx = each_edge[2]
            new_didx = dot_idx
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge)


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __get_all_matching_edges(self, calling_fun=None, stack=None, rule_lhs=None, rule_rhs=None, begin_idx=None, dot_idx=None):
        # for forward_fundamental
        # (B -> y・, [j,k])
        if (calling_fun == 'ff'):
            lhs_list = []
            for edge in stack:
                if edge[0].lhs() == rule_lhs:
                    lhs_list.append(edge)
            lhs_rhs_list = []
            for edge in lhs_list:
                if self.__is_complete(edge):
                    lhs_rhs_list.append(edge)
            lhs_rhs_bidx_list = []
            for edge in lhs_rhs_list:
                if edge[2] == begin_idx:
                    lhs_rhs_bidx_list.append(edge)
            return lhs_rhs_bidx_list
        # for backward_fundamental
        # (A -> a・Bb, [i,j])
        elif (calling_fun == 'bf'):
            rhs_list = []
            for edge in stack:
                if self.__is_complete(edge):
                    continue
                dot_prog = edge[1]
                if (edge[0].rhs()[dot_prog] == rule_rhs):
                    rhs_list.append(edge)
            rhs_didx_list = []
            for edge in rhs_list:
                if edge[3] == dot_idx:
                    rhs_didx_list.append(edge)
            return rhs_didx_list
        # called from unknown function
        else:
            return []


    # スタック　＝＞　深さ優先探索
    # キュー　　＝＞　幅優先探索
    def __add_to_agenda(self, edge):
        if (edge not in self.agenda) and (edge not in self.chart):
            self.agenda.insert(0, edge)  # push to agenda


    def __make_predictions(self, edge, parse_strategy):
        if (parse_strategy == "top_down") and (not self.__is_complete):
            self.__top_down_predict(edge)
        elif (parse_strategy == "bottom_up") and (self.__is_complete):
            self.__bottom_up_predict(edge)


    def __top_down_predict(self, edge):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.rhs()[dot_progress]
        succceeding_grammars = self.__get_all_matching_grammars(calling_fun='td', rule_lhs=B)
        for each_grammar in succceeding_grammars:
            new_rule = each_grammar
            new_dotp = 0
            new_bidx = dot_idx
            new_didx = dot_idx
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge)


    # bottom up (look at passive arcs)
    # only predict new constituents based on already completed ones
    def __bottom_up_predict(self, edge):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.lhs()
        precedent_grammars = self.__get_all_matching_grammars(calling_fun='bu', rule_rhs=B)
        for each_grammar in precedent_grammars:
            new_rule = each_grammar
            new_dotp = 1 # The dot is right behind the arrow???? if so, new_dotp = 0
            new_bidx = begin_idx
            new_didx = dot_idx
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge)


    def __get_all_matching_grammars(self, calling_fun=None, rule_lhs=None, rule_rhs=None, begin_idx=None, dot_idx=None):
        # for top_down_predict
        # (B -> y)
        if (calling_fun == 'td'):
            lhs_list = []
            for each_grammar in self.grammar:
                if each_grammar.lhs()[0] == rule_lhs:
                    lhs_list.append()
            return lhs_list
        # for bottom_up_predict
        elif (calling_fun == 'bu'):
            rhs_list = []
            for each_grammar in self.grammar.productions():
                if each_grammar.rhs()[0] == rule_rhs:
                    rhs_list.append(each_grammar)
            return rhs_list
        # called from unknown function
        else:
            return []


    # returns a list of trees, each in "nltk.tree.Tree" type
    def __make_trees(self, tokens):
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

    tokens = "I shot an elephant in my pajamas.".strip(".").split()
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
    # print(len(bp_trees))
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
    # print(len(tp_trees))
    """
    Out[16]: 2
    """



if __name__ == '__main__':
    main()

"""
references:
[1] http://cs.union.edu/~striegnk/courses/nlp-with-prolog/html/node71.html

"""