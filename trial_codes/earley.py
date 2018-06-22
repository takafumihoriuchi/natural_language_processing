"""
author : takafumihoriuchi
created in June of 2018
"""

import nltk


def push(stack, state):
    stack.insert(0, state)


class EarleyParser():
    
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens
        self.chart = [[] for _ in range(len(tokens) + 1)]

    def parse(self):
        dummy_grammar = nltk.CFG.fromstring("""gamma -> S""")
        print(dummy_grammar.productions(rhs()))
        dummy_state = (dummy_grammar.productions(lhs='gamma'), 0, 0, 0) # state = (rule, dot_progress, begin_idx, dot_idx)
        self.__enqueue(dummy_state, 0)
        
        # print(self.grammar.productions(rhs=self.tokens[0]))
        for i in range(0, len(self.tokens) + 1):
            for state in self.chart[i]:
                if (not self.__is_complete(state) and not self.__next_is_pos(state)):
                    self.__predictor(state)
                elif (not self.__complete(state) and self.__next_is_pos(state)):
                    self.__scanner(state)
                else:
                    self.__completer(state)

        return self.chart


    def __is_complete(self, state):
        # 右辺の長さとdot_progressが等しければ、completeと判断
        # print(state[0][0].rhs)
        # a = self.grammar.productions(lhs=state[0][0].rhs)
        # print(a)
        # print(state[0][0])
        pass

    def __next_is_pos(self, state):
        pass


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
