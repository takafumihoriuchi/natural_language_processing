"""
author : takafumihoriuchi
created in July of 2018
"""

from parser_module import Parser
from tmp_tree_module import TreeGenerator
from nltk import CFG


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
    # chart = parser.parse(tokens, parse_strategy='top_down', search_strategy='breadth_first')
    # chart = parser.parse(tokens, parse_strategy='top_down', search_strategy='depth_first')
    chart = parser.parse(tokens, parse_strategy='bottom_up', search_strategy='breadth_first')
    # chart = parser.parse(tokens, parse_strategy='bottom_up', search_strategy='depth_first')
    print(chart)
    tree_gen = TreeGenerator(chart, tokens)
    tree = tree_gen.get_tree()
    print("==========================")
    for edge in tree_gen.passive_edges:
        print(edge)
    print("==========================")
    print(tree)
    print(len(tree))

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
[3] https://www.nltk.org/api/nltk.html#nltk.tree.Tree
"""