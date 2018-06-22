class ChartParser(ParserI):
    """
    A generic chart parser.  A "strategy", or list of
    ``ChartRuleI`` instances, is used to decide what edges to add to
    the chart.  In particular, ``ChartParser`` uses the following
    algorithm to parse texts:

    | Until no new edges are added:
    |   For each *rule* in *strategy*:
    |     Apply *rule* to any applicable edges in the chart.
    | Return any complete parses in the chart
    """
    def __init__(self, grammar, strategy=BU_LC_STRATEGY, trace=0,
                 trace_chart_width=50, use_agenda=True, chart_class=Chart):
        """
        Create a new chart parser, that uses ``grammar`` to parse
        texts.

        :type grammar: CFG
        :param grammar: The grammar used to parse texts.
        :type strategy: list(ChartRuleI)
        :param strategy: A list of rules that should be used to decide
            what edges to add to the chart (top-down strategy by default).
        :type trace: int
        :param trace: The level of tracing that should be used when
            parsing a text.  ``0`` will generate no tracing output;
            and higher numbers will produce more verbose tracing
            output.
        :type trace_chart_width: int
        :param trace_chart_width: The default total width reserved for
            the chart in trace output.  The remainder of each line will
            be used to display edges.
        :type use_agenda: bool
        :param use_agenda: Use an optimized agenda-based algorithm,
            if possible.
        :param chart_class: The class that should be used to create
            the parse charts.
        """
        self._grammar = grammar
        self._strategy = strategy
        self._trace = trace
        self._trace_chart_width = trace_chart_width
        # If the strategy only consists of axioms (NUM_EDGES==0) and
        # inference rules (NUM_EDGES==1), we can use an agenda-based algorithm:
        self._use_agenda = use_agenda
        self._chart_class = chart_class

        self._axioms = []
        self._inference_rules = []
        for rule in strategy:
            if rule.NUM_EDGES == 0:
                self._axioms.append(rule)
            elif rule.NUM_EDGES == 1:
                self._inference_rules.append(rule)
            else:
                self._use_agenda = False

def grammar(self):
    return self._grammar


def _trace_new_edges(self, chart, rule, new_edges, trace, edge_width):
    if not trace: return
    print_rule_header = trace > 1
    for edge in new_edges:
        if print_rule_header:
            print('%s:' % rule)
            print_rule_header = False
        print(chart.pretty_format_edge(edge, edge_width))

def chart_parse(self, tokens, trace=None):
    """
    Return the final parse ``Chart`` from which all possible
    parse trees can be extracted.

    :param tokens: The sentence to be parsed
    :type tokens: list(str)
    :rtype: Chart
    """
    if trace is None: trace = self._trace
    trace_new_edges = self._trace_new_edges

    tokens = list(tokens)
    self._grammar.check_coverage(tokens)
    chart = self._chart_class(tokens)
    grammar = self._grammar

    # Width, for printing trace edges.
    trace_edge_width = self._trace_chart_width // (chart.num_leaves() + 1)
    if trace: print(chart.pretty_format_leaves(trace_edge_width))

    if self._use_agenda:
        # Use an agenda-based algorithm.
        for axiom in self._axioms:
            new_edges = list(axiom.apply(chart, grammar))
            trace_new_edges(chart, axiom, new_edges, trace, trace_edge_width)

        inference_rules = self._inference_rules
        agenda = chart.edges()
        # We reverse the initial agenda, since it is a stack
        # but chart.edges() functions as a queue.
        agenda.reverse()
        while agenda:
            edge = agenda.pop()
            for rule in inference_rules:
                new_edges = list(rule.apply(chart, grammar, edge))
                if trace:
                    trace_new_edges(chart, rule, new_edges, trace, trace_edge_width)
                agenda += new_edges

    else:
        # Do not use an agenda-based algorithm.
        edges_added = True
        while edges_added:
            edges_added = False
            for rule in self._strategy:
                new_edges = list(rule.apply_everywhere(chart, grammar))
                edges_added = len(new_edges)
                trace_new_edges(chart, rule, new_edges, trace, trace_edge_width)

    # Return the final chart.
    return chart


def parse(self, tokens, tree_class=Tree):
    chart = self.chart_parse(tokens)
    return iter(chart.parses(self._grammar.start(), tree_class=tree_class))
