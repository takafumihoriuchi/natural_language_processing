# chart parser
```
tkf-hruc:chart_parser takafumih$
tkf-hruc:chart_parser takafumih$
tkf-hruc:chart_parser takafumih$ python main_module.py 
========================================================
A chart-parser with parse-tree formatter;
Created by Takafumi Horiuchi in July of 2018.
========================================================
[input] Grammar with 13 productions (start state = S)
    S -> NP VP
    PP -> P NP
    NP -> Det N
    NP -> Det N PP
    NP -> 'I'
    VP -> V NP
    VP -> VP PP
    Det -> 'an'
    Det -> 'my'
    N -> 'elephant'
    N -> 'pajamas'
    V -> 'shot'
    P -> 'in'
========================================================
[input] tokens:
['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
========================================================
[options]
parse-strategy  : bottom_up
search-strategy : breadth_first
========================================================
[result] chart:
(VP -> VP PP, 1, 1, 7)
(S -> NP VP, 2, 0, 7)
(S -> NP VP, 1, 2, 7)
(VP -> V NP, 2, 1, 7)
(VP -> VP PP, 2, 1, 7)
(NP -> Det N PP, 3, 2, 7)
(VP -> VP PP, 1, 1, 4)
(S -> NP VP, 2, 0, 4)
(S -> NP VP, 1, 5, 7)
(PP -> P NP, 2, 4, 7)
(S -> NP VP, 1, 2, 4)
(VP -> V NP, 2, 1, 4)
(NP -> Det N PP, 2, 5, 7)
(NP -> Det N, 2, 5, 7)
(NP -> Det N PP, 2, 2, 4)
(NP -> Det N, 2, 2, 4)
(NP -> Det N PP, 1, 5, 6)
(NP -> Det N, 1, 5, 6)
(PP -> P NP, 1, 4, 5)
(NP -> Det N PP, 1, 2, 3)
(NP -> Det N, 1, 2, 3)
(VP -> V NP, 1, 1, 2)
(S -> NP VP, 1, 0, 1)
(N -> 'pajamas', 1, 6, 7)
(Det -> 'my', 1, 5, 6)
(P -> 'in', 1, 4, 5)
(N -> 'elephant', 1, 3, 4)
(Det -> 'an', 1, 2, 3)
(V -> 'shot', 1, 1, 2)
(NP -> 'I', 1, 0, 1)
========================================================
[result] trees:
(S
  (NP I)
  (VP
    (V shot)
    (NP (Det an) (N elephant) (PP (P in) (NP (Det my) (N pajamas))))))
(S
  (NP I)
  (VP
    (VP (V shot) (NP (Det an) (N elephant)))
    (PP (P in) (NP (Det my) (N pajamas)))))
========================================================
[result] number of yielded trees: 2
========================================================
tkf-hruc:chart_parser takafumih$ 
tkf-hruc:chart_parser takafumih$ 
tkf-hruc:chart_parser takafumih$ 
```