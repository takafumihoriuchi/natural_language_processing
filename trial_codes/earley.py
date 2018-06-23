"""
author : takafumihoriuchi
created in June of 2018
"""

import nltk


def push(stack, state):
    stack.insert(0, state)

def flatten_two_dim_list(two_dim_list):
    return [item for sublist in two_dim_list for item in sublist]

"""
def flatten_nest_list(nest_list):
    working_list = nest_list
    try:
        check_error = working_list[0][0]
        tmp_list = []
        for item in working_list:
            tmp_list.append(item)
        tmp_list = [item for sublist in tmp_list for item in sublist]
        flatten_nest_list(tmp_list)
    except TypeError:
        flat_list = working_list
        return flat_list
"""

class EarleyParser():
    
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens
        self.chart = [[] for _ in range(len(tokens) + 1)]

    def parse(self):
        dummy_grammar = nltk.CFG.fromstring("""gamma -> S""")
        # print( dummy_grammar.productions()[0].lhs() )
        dummy_state = (dummy_grammar.productions()[0], 0, 0, 0)
        self.__enqueue(dummy_state, 0)
        
        # print(self.grammar.productions(rhs=self.tokens[0]))
        for i in range(0, len(self.tokens) + 1):
            for state in self.chart[i]:
                if (not self.__is_complete(state) and not self.__next_is_pos(state)):
                    self.__predictor(state)
                elif (not self.__is_complete(state) and self.__next_is_pos(state)):
                    self.__scanner(state)
                else:
                    self.__completer(state)

        return self.chart


    # state = (rule, dot_progress, begin_idx, dot_idx)
    # 'lenght_of_right_hand_side'と'progress_of_dot'が等しければcompleteと判断
    def __is_complete(self, state):
        rhs_len = len(state[0].rhs())
        if (state[1] == rhs_len):
            return True
        else:
            return False
        

    # state = (rule, dot_progress, begin_idx, dot_idx)
    # "NT -> POS"・"POS -> word"、次の次がに単語があれば、next_is_pos == True
    def __next_is_pos(self, state):
        current_rule = [state[0]]
        next_rules = __get_next_rules(current_rule)
        # if next_rules==[]: current state leads to terminal symbols
        if not next_rules:
            return False
        next_next_rules = __get_next_rules(next_rules)
        # if next_next_rules: current state leads to POS
        if not next_next_rules:
            return True
        # if current state leads to non-POS/non-word
        return False
        """
        for each_rhs_sym in current_rule.rhs():
            next_rules = self.grammar.productions(lhs=each_rhs_sym)
            for next_rule in next_rules:
                for next_rule_rhs in next_rule.rhs():
                    if next_rule_rhs in self.tokens:
                        print("yes-next-is-pos:", next_rule)
                        return True
                print("no-next-is-not-pos:", next_rule)
                return False
        """

    # return a flat list
    def __get_next_rules(self, rule):
        next_rules_all = []
        for each_rhs_sym in rule.rhs():
            next_rules_part = self.grammar.productions(lhs=each_rhs_sym)
            next_rules_all.append(next_rules_part)
        next_rules_all_flat = flatten_two_dim_list(next_rules_all)
        return next_rules_all_flat


    def __predictor(self, state):
        pass


    def __scanner(self, state):
        pass


    def __completer(self, state):
        pass


    def __enqueue(self, state, chart_entry):
        if state not in self.chart[chart_entry]:
            push(self.chart[chart_entry], state)



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

    parser = EarleyParser(grammar, tokens)
    chart = parser.parse()
    print(chart)


if __name__ == '__main__':
    main()
