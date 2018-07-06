"""
author : takafumihoriuchi
created in July of 2018
"""
from nltk import CFG
from parser_module import Parser
from tree_module import TreeGenerator


def main():

    grammar = CFG.fromstring("""
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

    parser = Parser(grammar)
    chart = parser.parse(tokens, parse_strategy='bottom_up')
    print(chart)

    tree_gen = TreeGenerator(chart)
    tree = tree_gen.get_tree()
    print(tree)

    ###

    # bp_trees = parser.parse(tokens, parse_strategy='bottom_up')
    # print(len(bp_trees))

    # tp_trees = parser.parse(tokens, parse_strategy='top_down')
    # print(len(tp_trees))



if __name__ == '__main__':
    main()


"""
references:
[1] http://cs.union.edu/~striegnk/courses/nlp-with-prolog/html/node71.html
[2] http://www.ling.helsinki.fi/kit/2008s/clt231/nltk-0.9.5/doc/en/ch08.html
"""