# Natural Language Processing

This repository contains implementations of Natural Language Processing related problems.

### contents
- [POS estimator by viterbi algorithm](https://github.com/takafumihoriuchi/natural_language_processing#viterbi_pos_estimatepy)
- [chart parser syntatic analysis](https://github.com/takafumihoriuchi/natural_language_processing#viterbi_pos_estimatepy)

## viterbi_pos_estimate.py

```
takafumihoriuchi$
takafumihoriuchi$
takafumihoriuchi$ python viterbi_pos_estimate.py

+------------------------------------------------------------------------------+
This is a HMM based POS estimator created by Takafumi Horiuchi in May of 2018.
Input of the sentence "We choose to go to the Moon." could output the following:
[('We', 'PRP'), ('choose', 'VB'), ('to', 'TO'), ('go', 'VB'), ('to', 'TO'), ('the', 'DT'), ('moon', 'NN'), ('.', '.')]

loading POS tagsets (may consume few seconds) ...

input a sentence: I want to put a ding in the universe.
POS estimation result:
('I', 'PRP')
('want', 'VBP')
('to', 'TO')
('put', 'VB')
('a', 'DT')
('ding', 'NN')
('in', 'IN')
('the', 'DT')
('universe', 'NN')
('.', '.')

Conditions: Penn-Treebank as POS tagset; train : test = 0.80 : 0.20
--------------------------------------------------------------------------------
measuring precision of model (may consume several minutes) ...
[========================================================================      ]
model precision
token based accuracy    : 0.860571884824592
sentence based accuracy : 0.1417624521072797

POS specific accuracy   :
<s> 	---	 {'correct': 0, 'total': 0, 'accuracy': None}
NNP 	---	 {'correct': 1152, 'total': 1800, 'accuracy': 0.64}
, 	---	 {'correct': 909, 'total': 930, 'accuracy': 0.9774193548387097}
CD 	---	 {'correct': 865, 'total': 1032, 'accuracy': 0.8381782945736435}
NNS 	---	 {'correct': 894, 'total': 1127, 'accuracy': 0.7932564330079858}
JJ 	---	 {'correct': 805, 'total': 1087, 'accuracy': 0.7405703771849126}
MD 	---	 {'correct': 202, 'total': 204, 'accuracy': 0.9901960784313726}
VB 	---	 {'correct': 460, 'total': 498, 'accuracy': 0.9236947791164659}
DT 	---	 {'correct': 1548, 'total': 1611, 'accuracy': 0.9608938547486033}
NN 	---	 {'correct': 2344, 'total': 2901, 'accuracy': 0.807997242330231}
IN 	---	 {'correct': 1843, 'total': 1952, 'accuracy': 0.9441598360655737}
. 	---	 {'correct': 742, 'total': 762, 'accuracy': 0.973753280839895}
VBZ 	---	 {'correct': 280, 'total': 324, 'accuracy': 0.8641975308641975}
VBG 	---	 {'correct': 188, 'total': 261, 'accuracy': 0.7203065134099617}
CC 	---	 {'correct': 391, 'total': 429, 'accuracy': 0.9114219114219114}
VBD 	---	 {'correct': 607, 'total': 743, 'accuracy': 0.8169582772543742}
VBN 	---	 {'correct': 344, 'total': 452, 'accuracy': 0.7610619469026548}
-NONE- 	---	 {'correct': 1321, 'total': 1340, 'accuracy': 0.985820895522388}
RB 	---	 {'correct': 403, 'total': 478, 'accuracy': 0.8430962343096234}
TO 	---	 {'correct': 457, 'total': 464, 'accuracy': 0.9849137931034483}
PRP 	---	 {'correct': 219, 'total': 222, 'accuracy': 0.9864864864864865}
RBR 	---	 {'correct': 7, 'total': 16, 'accuracy': 0.4375}
WDT 	---	 {'correct': 104, 'total': 104, 'accuracy': 1.0}
VBP 	---	 {'correct': 126, 'total': 165, 'accuracy': 0.7636363636363637}
RP 	---	 {'correct': 30, 'total': 34, 'accuracy': 0.8823529411764706}
PRP$ 	---	 {'correct': 119, 'total': 122, 'accuracy': 0.9754098360655737}
JJS 	---	 {'correct': 30, 'total': 38, 'accuracy': 0.7894736842105263}
POS 	---	 {'correct': 185, 'total': 196, 'accuracy': 0.9438775510204082}
`` 	---	 {'correct': 80, 'total': 81, 'accuracy': 0.9876543209876543}
EX 	---	 {'correct': 7, 'total': 7, 'accuracy': 1.0}
'' 	---	 {'correct': 76, 'total': 78, 'accuracy': 0.9743589743589743}
WP 	---	 {'correct': 26, 'total': 26, 'accuracy': 1.0}
: 	---	 {'correct': 73, 'total': 77, 'accuracy': 0.948051948051948}
JJR 	---	 {'correct': 62, 'total': 76, 'accuracy': 0.8157894736842105}
WRB 	---	 {'correct': 24, 'total': 27, 'accuracy': 0.8888888888888888}
$ 	---	 {'correct': 241, 'total': 242, 'accuracy': 0.9958677685950413}
NNPS 	---	 {'correct': 21, 'total': 64, 'accuracy': 0.328125}
WP$ 	---	 {'correct': 4, 'total': 4, 'accuracy': 1.0}
-LRB- 	---	 {'correct': 23, 'total': 26, 'accuracy': 0.8846153846153846}
-RRB- 	---	 {'correct': 22, 'total': 26, 'accuracy': 0.8461538461538461}
PDT 	---	 {'correct': 4, 'total': 6, 'accuracy': 0.6666666666666666}
RBS 	---	 {'correct': 5, 'total': 5, 'accuracy': 1.0}
FW 	---	 {'correct': 0, 'total': 0, 'accuracy': None}
UH 	---	 {'correct': 0, 'total': 0, 'accuracy': None}
SYM 	---	 {'correct': 0, 'total': 0, 'accuracy': None}
LS 	---	 {'correct': 0, 'total': 0, 'accuracy': None}
# 	---	 {'correct': 2, 'total': 2, 'accuracy': 1.0}
+------------------------------------------------------------------------------+

takafumihoriuchi$
takafumihoriuchi$
```


## chart-parser
see [here](https://github.com/takafumihoriuchi/natural_language_processing/tree/master/chart_parser)