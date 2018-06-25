"""
author : takafumihoriuchi
created in June of 2018
"""
import nltk


def push(stack, state):
    # stack.insert(0, state)
    stack.append(state)
    # 末尾にくっつけないと「for state in self.chart[i]:」が進行しない

def flatten_two_dim_list(two_dim_list):
    return [item for sublist in two_dim_list for item in sublist]


class EarleyParser():
    
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens
        self.chart = [[] for _ in range(len(tokens) + 1)]


    def parse(self):
        # dummy_grammar = nltk.CFG.fromstring("""S -> NP VP""")
        dummy_grammar = nltk.CFG.fromstring("""gamma -> S""")
        dummy_state = (dummy_grammar.productions()[0], 0, 0, 0)
        self.__enqueue(dummy_state, 0)
        for i in range(0, len(self.tokens) + 1):
            for state in self.chart[i]:
                print("evaluating state :", state)
                if (not self.__is_complete(state)):
                    print("calling PREDICTOR")
                    self.__predictor(state)
                else:
                    print("calling COMPLETER")
                    self.__completer(state)
                # print(self.chart)
                for entry in self.chart:
                    print(entry)
                print("=================")
        return self.chart


    # state = (rule, dot_progress, begin_idx, dot_idx)
    def __predictor(self, state):
        current_rule = [state[0]]
        dot_progress = state[1]
        dot_idx = state[3]
        next_rules = self.__get_next_rules(current_rule, dot_progress)
        print("current_rule", current_rule)
        print("next_rules", next_rules)
        if next_rules == []:
            new_state = (state[0], dot_progress + 1, dot_idx, dot_idx + 1)
            self.__enqueue(new_state, dot_idx + 1)
            return
        for next_rule in next_rules:
            new_state = (next_rule, 0, dot_idx, dot_idx)
            self.__enqueue(new_state, dot_idx)


    # state = (rule, dot_progress, begin_idx, dot_idx)
    def __completer(self, state):
        current_rule = state[0] # (B -> y・)
        begin_idx = state[2] # j
        dot_idx = state[3] # k
        B = current_rule.lhs() # e.g. NP
        # for each (A -> a ・ B b, [i,j]) in chart[j] do
        for state_in_chart in self.chart[begin_idx]:
            print("state_in_chart", state_in_chart)
            dot_idx_in_chart = state_in_chart[3]
            # 位置について弾く
            if not (dot_idx_in_chart == begin_idx):
                continue
            rule_in_chart = state_in_chart[0]
            dot_progress_in_chart = state_in_chart[1]
            rhs_in_chart = rule_in_chart.rhs()
            # ルールの進捗状況によって弾く
            for new_dot_progress, rhs_symbol in enumerate(rhs_in_chart):
                if (rhs_symbol == B) and (dot_progress_in_chart == new_dot_progress):
                    begine_idx_chart = state_in_chart[2]
                    new_state = (rule_in_chart, new_dot_progress + 1, begine_idx_chart, dot_idx)
                    print("new_state", new_state)
                    self.__enqueue(new_state, dot_idx)
                    break
            

    def __enqueue(self, state, chart_entry):
        if (chart_entry > len(self.tokens)):
            return # ignore (parse already finished)
        if state not in self.chart[chart_entry]:
            push(self.chart[chart_entry], state)


    # state = (rule, dot_progress, begin_idx, dot_idx)
    # 'lenght_of_right_hand_side'と'progress_of_dot'が等しければcompleteと判断
    def __is_complete(self, state):
        rhs_length = len(state[0].rhs())
        dot_progress = state[1]
        return (rhs_length == dot_progress)


    # get list of rules as argument
    # return a flat list
    # by specifying the dot_idx, 
    # a list of rules begining with [symbol right after the dot] will be returned
    # dot_index functions properly only when len(rules)==1
    def __get_next_rules(self, rules, dot_progress=None):
        next_rules_all = []
        if len(rules) is 1 and dot_progress is not None:
            rhs_list = [rules[0].rhs()[dot_progress]]
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



def main():

    # NP は、POSでもあり、非終端記号でもあるため、
    # J&Mに乗っているアルゴリズムでは、この文法は扱えない。
    # そこで、scannerを除いたアルゴリズムを実装した。
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
    
    for entry in chart:
        print(entry)


if __name__ == '__main__':
    main()


"""
"I shot an elephant in my pajamas."

S   -> NP VP
PP  -> P NP
NP  -> Det N | Det N PP | 'I'
VP  -> V NP | VP PP
Det -> 'an' | 'my'
N   -> 'elephant' | 'pajamas'
V   -> 'shot'
P   -> 'in'

# edited ver.
S   -> NP VP | NPI VP
PP  -> P NP | P NPI
NP  -> Det N | Det N PP
NPI -> 'I'
VP  -> V NP | VP PP | V NPI
Det -> 'an' | 'my'
N   -> 'elephant' | 'pajamas'
V   -> 'shot'
P   -> 'in'
"""

"""
"book that flight"

S -> NP  VP
S -> Aux NP VP
S -> VP
NP -> Det NOM
NOM -> Noun
NOM -> Noun NOM
VP -> Verb
VP -> Verb NP
Det -> that | this | a | the
Noun -> book | flight | meal | man
Verb -> book | include | read
Aux -> does
"""