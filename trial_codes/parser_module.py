"""
author : takafumihoriuchi
created in July of 2018
"""
class Parser(object):

    def __init__(self, grammar):
        self.grammar = grammar
        self.chart = []
        self.agenda = []


    # parse_strategy  = { 'bottom_up'     | 'top_down'    }
    # search_strategy = { 'breadth_first' | 'depth_first' }
    def parse(self, tokens, start_symbol='S',
              parse_strategy='bottom_up', search_strategy='breadth_first'):
        self.__initialize(tokens, start_symbol, parse_strategy, search_strategy)
        while (self.agenda):
            edge = self.agenda.pop(0)
            self.__process_edge(edge, parse_strategy, search_strategy)
        # HACK: need to clear chart (and agenda) for next use?
        return self.chart


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __initialize(self, tokens, start_symbol, parse_strategy, search_strategy):
        # add lexical-rules to chart/agenda
        for i in reversed(range(len(tokens))):
            rule = self.grammar.productions(rhs=tokens[i])[0]
            dot_prog = len(rule.rhs()) # (=1, indicate all rhs was found)
            terminant_passive_edge = (rule, dot_prog, i, i+1)
            if parse_strategy is 'top_down':
                self.__add_to_chart(terminant_passive_edge)
            elif parse_strategy is 'bottom_up':
                self.__add_to_agenda(terminant_passive_edge, search_strategy)
        if parse_strategy is 'top_down':
            top_level_rules = []
            for rule in self.grammar.productions():
                if str(rule.lhs()) == str(start_symbol):
                    top_level_rules.append(rule)
            for tlr in top_level_rules:
                top_level_edge = (tlr, 0, 0, 0)
                self.__add_to_agenda(top_level_edge, search_strategy)


    def __process_edge(self, edge, parse_strategy, search_strategy):
        self.__add_to_chart(edge)
        # combine active-arc with passive-arc (and vice-versa)
        if self.__is_complete(edge) is False: # edge is an active-arc
            self.__forward_fundamental_rule(edge, search_strategy)
        else: # edge is a passive-arc
            self.__backward_fundamental_rule(edge, search_strategy)
        self.__make_predictions(edge, parse_strategy, search_strategy)


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __forward_fundamental_rule(self, edge, search_strategy):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.rhs()[dot_progress]
        succedent_edges = self.__get_matching_edges_ff(B, dot_idx)
        for each_edge in succedent_edges:
            new_rule = current_rule
            new_dotp = dot_progress+1
            new_bidx = begin_idx
            new_didx = each_edge[3]
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge, search_strategy)


    def __backward_fundamental_rule(self, edge, search_strategy):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.lhs()
        precedent_edges = self.__get_matching_edges_bf(B, begin_idx)
        for each_edge in precedent_edges:
            new_rule = each_edge[0]
            new_dotp = each_edge[1]+1
            new_bidx = each_edge[2]
            new_didx = dot_idx
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge, search_strategy)


    def __make_predictions(self, edge, parse_strategy, search_strategy):
        if (parse_strategy == "top_down") and (not self.__is_complete):
            self.__top_down_predict(edge, search_strategy) # edge is active
        elif (parse_strategy == "bottom_up") and (self.__is_complete):
            self.__bottom_up_predict(edge, search_strategy) # edge is passive


    def __top_down_predict(self, edge, search_strategy):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.rhs()[dot_progress]
        succedent_grammars = self.__get_matching_grammars_td(B)
        for each_grammar in succedent_grammars:
            new_rule = each_grammar
            new_dotp = 0
            new_bidx = dot_idx
            new_didx = dot_idx
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge, search_strategy)


    # bottom up (look at passive arcs)
    # only predict new constituents based on already completed ones
    def __bottom_up_predict(self, edge, search_strategy):
        current_rule = edge[0]
        dot_progress = edge[1]
        begin_idx    = edge[2]
        dot_idx      = edge[3]
        B = current_rule.lhs()
        precedent_grammars = self.__get_matching_grammars_bu(B)
        for each_grammar in precedent_grammars:
            new_rule = each_grammar
            new_dotp = 1
            new_bidx = begin_idx
            new_didx = dot_idx
            new_edge = (new_rule, new_dotp, new_bidx, new_didx)
            self.__add_to_agenda(new_edge, search_strategy)


    # order of entry does not matter
    # return: 'True' if insertion success; 'False' if failed
    def __add_to_chart(self, edge):
        if edge not in self.chart:
            self.chart.insert(0, edge) # (=push)
            return True
        return False


    # order of entry depends on search_strategy
    # stack => depth_first_search, queue => breadth_first_search
    # return: 'True' if insertion success; 'False' if failed
    def __add_to_agenda(self, edge, search_strategy):
        if (edge not in self.agenda) and (edge not in self.chart):
            if search_strategy is 'depth_first':
                self.agenda.insert(0, edge) # (=push to stack)
            elif search_strategy is 'breadth_first':
                self.agenda.append(edge) # (=insert to queue)
            return True
        return False


    # return: 'True' if edge is passive; 'False' if edge is active
    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __is_complete(self, edge):
        rhs_length = len(edge[0].rhs())
        dot_progress = edge[1]
        return (rhs_length == dot_progress)


    # extract edge of: (B -> y・, [j,k])
    def __get_matching_edges_ff(self, rule_lhs, begin_idx):
        lhs_list = []
        for edge in self.chart:
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

    
    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # extract edge of: (A -> a・Bb, [i,j])
    def __get_matching_edges_bf(self, rule_rhs, dot_idx):
        rhs_list = []
        for edge in self.chart:
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

    
    # extract grammar of: (B -> y)
    def __get_matching_grammars_td(self, rule_lhs):
        lhs_list = []
        for each_grammar in self.grammar:
            if each_grammar.lhs()[0] == rule_lhs:
                lhs_list.append()
        return lhs_list


    # extract grammar of: (A -> B b)
    def __get_matching_grammars_bu(self, rule_rhs):
        rhs_list = []
        for each_grammar in self.grammar.productions():
            if each_grammar.rhs()[0] == rule_rhs:
                rhs_list.append(each_grammar)
        return rhs_list
