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
    
    # parse_strategy  = { 'bottom_up'     | 'top_down'    }
    # search_strategy = { 'breadth_first' | 'depth_first' }
    parse_strategy = 'bottom_up'
    search_strategy = 'breadth_first'

    chart = parser.parse(tokens, parse_strategy=parse_strategy, search_strategy=search_strategy)

    tree_gen = TreeGenerator(chart, tokens)
    trees = tree_gen.get_trees()

    print("========================================================")
    print("A chart-parser with parse-tree formatter;")
    print("Created by Takafumi Horiuchi in July of 2018.")
    print("========================================================")
    print("[input]", grammar)
    print("========================================================")
    print("[input] tokens:")
    print(tokens)
    print("========================================================")
    print("[options]")
    print("parse-strategy  :", parse_strategy)
    print("search-strategy :", search_strategy)
    print("========================================================")
    print("[result] chart:")
    for edge in chart:
        print(edge)
    print("========================================================")
    print("[result] trees:")
    for tree in trees:
        print(tree)
    print("========================================================")
    print("[result] number of yielded trees:", len(trees))
    print("========================================================")


if __name__ == '__main__':
    main()


"""
references:
[1] http://cs.union.edu/~striegnk/courses/nlp-with-prolog/html/node71.html
[2] http://www.ling.helsinki.fi/kit/2008s/clt231/nltk-0.9.5/doc/en/ch08.html
[3] https://www.nltk.org/api/nltk.html#nltk.tree.Tree
... and more python related websites
"""