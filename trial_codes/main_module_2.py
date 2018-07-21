"""
author : takafumihoriuchi
created in July of 2018
"""
from nltk import data
from nltk import CFG
from parser_module import Parser
from tree_module import TreeGenerator


def main():

    grammar_atis = data.load('grammars/large_grammars/atis.cfg')
    print(grammar_atis)
    sent_flights = "show me northwest flights to detroit."
    tokens_flights = sent_flights.replace(".", " .").split()
    print(tokens_flights)
    #import sys
    #sys.exit(1)

    #grammar = CFG.fromstring("""
    #    S   -> NP VP
    #    PP  -> P NP
    #    NP  -> Det N | Det N PP | 'I'
    #    VP  -> V NP | VP PP
    #    Det -> 'an' | 'my'
    #    N   -> 'elephant' | 'pajamas'
    #    V   -> 'shot'
    #    P   -> 'in'
    #    """)

    #tokens = "I shot an elephant in my pajamas.".strip(".").split()

    # parser = Parser(grammar)
    parser = Parser(grammar_atis)
    
    # parse_strategy  = { 'bottom_up'     | 'top_down'    }
    # search_strategy = { 'breadth_first' | 'depth_first' }
    ps = 'bottom_up'
    ss = 'depth_first'

    # chart = parser.parse(tokens, parse_strategy=ps, search_strategy=ss)
    chart = parser.parse(tokens_flights, start_symbol='SIGMA', parse_strategy=ps, search_strategy=ss)

    # tree_gen = TreeGenerator(chart, tokens)
    tree_gen = TreeGenerator(chart, tokens_flights, start_symbol='SIGMA')

    trees = tree_gen.get_trees()

    print("========================================================")
    print("A chart-parser with parse-tree formatter;")
    print("Created by Takafumi Horiuchi in July of 2018.")
    print("========================================================")
    # print("[input]", grammar)
    print("[input]", grammar_atis)
    print("========================================================")
    print("[input] tokens:")
    # print(tokens)
    print(tokens_flights)
    print("========================================================")
    print("[options] parse-strategy  :", ps)
    print("          search-strategy :", ss)
    print("========================================================")
    print("[result] chart:")
    for edge in chart:
        print(edge)
    print("========================================================")
    print("[result] trees:")
    for tree in trees:
        print("")
        print(tree)
        print("")
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


### flight detroit に対応するように拡張する上で、直面したこと：

- "."を切り外してはいけない
- start symbolが'S'ではなく'SIGMA'
- 終端記号の判定方法、pajamasの例では、右辺のlen()が1なら終端と判定していたが、atisはそうは行かない
  # cf. arc = (rule, dot_progress, begin_idx, dot_idx)
  def __is_terminant(self, arc):
      return (arc[3] - arc[2] == 1)
- treeがリストの時点で、不完全な木は省く必要がある。
  do this by: listの状態で、str()にして、左から順に、"show", "me", ... 
  があるかどうかを確かめる。見つけた時点で、それより前の位置には戻らない。
"""
