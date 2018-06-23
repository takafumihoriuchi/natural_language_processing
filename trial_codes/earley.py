"""
author : takafumihoriuchi
created in June of 2018
"""

import nltk


def push(stack, state):
    stack.insert(0, state)

def flatten_two_dim_list(two_dim_list):
    return [item for sublist in two_dim_list for item in sublist]


class EarleyParser():
    
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens
        self.chart = [[] for _ in range(len(tokens) + 1)]


    def parse(self):
        dummy_grammar = nltk.CFG.fromstring("""gamma -> S""")
        dummy_state = (dummy_grammar.productions()[0], 0, 0, 0)
        self.__enqueue(dummy_state, 0)
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
        rhs_length = len(state[0].rhs())
        dot_progress = state[1]
        return (rhs_length == dot_progress)


    # state = (rule, dot_progress, begin_idx, dot_idx)
    # "NT -> NT・POS", "POS -> word"、次の次がに単語があれば、next_is_pos == True
    # 単語は、単語を左辺にもつような生成規則の集合は空、という性質を利用して得る
    def __next_is_pos(self, state):
        dot_idx = state[1]
        current_rule = [state[0]]
        next_rules = self.__get_next_rules(current_rule, dot_idx)
        print("next_rules:", next_rules)
        # current state leads to terminal symbols
        if (next_rules == []):
            print("symbol next to dot is a word")
            return False
        next_next_rules = self.__get_next_rules(next_rules)
        print("next_next_rules:", next_next_rules)
        # current state leads to POS
        if (next_next_rules == []):
            print("symbol next to dot is a POS")
            return True
        # if current state leads to non-POS/non-word
        print("symbol next to dot is neither a word nor a POS")
        return False


    # get list of rules as argument
    # return a flat list
    # by specifying the dot_idx, 
    # a list of rules begining with [symbol right after the dot] will be returned
    # dot_index functions properly only when len(rules)==1
    def __get_next_rules(self, rules, dot_idx=None):
        next_rules_all = []
        if len(rules) is 1 and dot_idx is not None:
            rhs_list = [rules[0].rhs()[dot_idx]]
        else:
            rhs_list = [rhs for rule in rules for rhs in rule.rhs()]
        for each_rhs in rhs_list:
            next_rules_part = self.grammar.productions(lhs=each_rhs)
            # indicate that there is a word in the right-hand-side
            if next_rules_part == []:
                return []
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
