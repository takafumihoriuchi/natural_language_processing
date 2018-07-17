"""
author : takafumihoriuchi
created in July of 2018
"""
from nltk import Tree


class TreeGenerator(object):
    
    def __init__(self, chart, tokens, start_symbol='S'):
        self.chart = chart
        self.tokens = tokens
        self.start_symbol = start_symbol
        self.passive_edges = None # initialized later
        self.work_stack = [] # for storing states during recursion


    # returns a list of trees, each in nltk.tree.Tree type
    def get_trees(self):
        
        self.passive_edges = self.__extract_passive_edges(self.chart)
        top_arc = self.__get_top_level_arc(self.passive_edges)
        
        if top_arc is None:
            print("FAILURE: no successful parse found")
            return None
        
        # full list of parse trees
        possible_parse_trees = []
        # first search of parse tree; prepare working-stack
        parse_tree = self.__build_parse_tree(top_arc)
        possible_parse_trees.append(parse_tree)

        # search of alternative parse trees
        while self.work_stack:
            tmp_state = self.work_stack.pop(0)
            alt_parse_tree = tmp_state[0]
            alt_arc = tmp_state[1]
            alt_init_nth = tmp_state[2]
            alt_tree = self.__build_parse_tree(alt_arc, alt_parse_tree, alt_init_nth)
            possible_parse_trees.append(alt_tree)

        formatted_possible_parse_trees = []
        for parse_list in possible_parse_trees:
            formatted_parse_tree = self.__format_parse_tree(parse_list)
            formatted_possible_parse_trees.append(formatted_parse_tree)
        
        return formatted_possible_parse_trees


    # recursively search for a parse tree
    # cf. (arc == edge) in meaning
    # cf. edge = (rule, dot_progress, begin_idx, dot_idx)
    def __build_parse_tree(self, arc, init_parse_tree=None, init_nth=None):
        
        # base-case of recursion
        if self.__is_terminant(arc):
            return [arc[0]]

        # initialize parse tree
        if init_parse_tree is None: parse_tree = list([arc[0].lhs()])
        else                      : parse_tree = list(init_parse_tree)
        
        # body of recursion
        progress = arc[2]
        for nth_rhs, each_rhs in enumerate(arc[0].rhs()):
            
            # consider information from working-stack
            alt_arcs = []
            lock = False
            if (init_nth is None): pass
            elif (nth_rhs < init_nth): continue
            elif (init_nth == nth_rhs):
                alt_arcs.append(list(arc))
                lock = True
            else: pass

            # collect adequate edges
            if lock is False:
                for cand_edge in self.passive_edges:
                    symb_match = (cand_edge[0].lhs() == each_rhs)
                    prog_match = (cand_edge[2] == progress)
                    end_match = (cand_edge[3] != len(self.tokens))\
                                if (nth_rhs < len(arc[0].rhs()) - 1)\
                                else (cand_edge[3] == arc[3])
                    if (symb_match and prog_match and end_match):
                        alt_arcs.append(list(cand_edge))

            while alt_arcs:
                # cf. pop(): remove the last item in list
                tmp_arc = list(alt_arcs.pop())
                tmp_state = (list(parse_tree), tmp_arc, nth_rhs)
                self.work_stack.insert(0, tmp_state)
            
            # proceed with the first arc in working-stack
            alt_arc = list((self.work_stack.pop(0))[1])
            parse_tree.append(list(self.__build_parse_tree(alt_arc)))
            progress = alt_arc[3]
        
        return list(parse_tree)


    # cf. arc = (rule, dot_progress, begin_idx, dot_idx)
    def __is_terminant(self, arc):
        return (arc[3] - arc[2] == 1)

    
    # format list to type 'nltk.tree.Tree'
    # eg. parse_list = [S, [NP -> 'I'], [VP, [V -> 'shot'], [...]]]
    def __format_parse_tree(self, parse_list):
        tmp_str_a = str(parse_list)
        tmp_str_b = tmp_str_a.replace("[", "(")
        tmp_str_c = tmp_str_b.replace("]", ")")
        tmp_str_d = tmp_str_c.replace(" -> ", " ")
        tmp_str_e = tmp_str_d.replace(",", "")
        tmp_str_f = tmp_str_e.replace("'", "")
        parse_tree = Tree.fromstring(tmp_str_f)
        return parse_tree


    # cf. edge = (rule, dot_progress, begin_idx, dot_idx)
    def __get_top_level_arc(self, passive_edges):
        top_arc = None
        for edge in passive_edges:
            check_symbol = (str(edge[0].lhs()) == str(self.start_symbol))
            check_beg_idx = (edge[2] == 0)
            check_dot_idx = (edge[3] == len(self.tokens))
            top_check = check_symbol and check_beg_idx and check_dot_idx
            if top_check is True:
                top_arc = edge
                break
        return top_arc


    # cf. edge = (rule, dot_progress, begin_idx, dot_idx)
    def __extract_passive_edges(self, chart):
        passive_edges = []
        for edge in chart:
            if (self.__is_complete(edge)):
                passive_edges.append(edge)
        return passive_edges


    # HACK: want to share this function with Parser class
    # returns True for passive-edges / False for active-edges
    def __is_complete(self, edge):
        rhs_length = len(edge[0].rhs())
        dot_progress = edge[1]
        return (rhs_length == dot_progress)
