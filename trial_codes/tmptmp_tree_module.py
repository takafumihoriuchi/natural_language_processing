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


    # returns a list of trees, each in nltk.tree.Tree type
    # guaranteed that there is at least one parse tree
    def get_trees(self):
        self.passive_edges = self.__extract_passive_edges(self.chart)
        top_arc = self.__get_top_level_arc(self.passive_edges)
        if top_arc is None:
            print("FAILURE: no successful parse found")
            return None
        
        possible_parse_trees = [] # store all possible parse trees
        self.tmp_storage = [] # working list to store state info

        parse_tree = self.__build_parse_tree(top_arc)
        possible_parse_trees.append(parse_tree)

        #print("==========================")
        while self.tmp_storage:
            tmp_state = self.tmp_storage.pop(0)
            another_parse_tree = tmp_state[0]
            another_arc = tmp_state[1]
            init_nth = tmp_state[2]
            another_tree = self.__build_parse_tree(another_arc, another_parse_tree, init_nth)
            possible_parse_trees.append(another_tree)

        print("==========================")
        for i, possibillity in enumerate(possible_parse_trees):
            print("tree #0%d:" % (i+1))
            print(possibillity)
        print("==========================")

        formatted_possible_parse_trees = []
        for possibillity in possible_parse_trees:
            formatted_parse_tree = self.__format_parse_tree(possibillity)
            formatted_possible_parse_trees.append(formatted_parse_tree)
        
        return formatted_possible_parse_trees


    # return "list of parse-tree-lists"
    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # start: __find_parse_tree(passive_edges, [], top_arc)
    def __build_parse_tree(self, arc, init_parse_tree=None, init_nth=None):
        if self.__is_terminant(arc):
            return [arc[0]]

        if init_parse_tree is None:
            parse_tree = list([arc[0].lhs()])
            # parse_tree = list([arc[0]])
        else:
            parse_tree = list(init_parse_tree)
        
        progress = arc[2]
        for nth_rhs, each_rhs in enumerate(arc[0].rhs()):
        
            alt_arcs = []

            lock = False
            if (init_nth is None):
                pass
            elif (nth_rhs < init_nth):
                continue
            elif (init_nth == nth_rhs):
                alt_arcs.append(list(arc))
                lock = True
            else:
                pass

            if lock is False:
                for cand_edge in self.passive_edges:
                    symb_match = (cand_edge[0].lhs() == each_rhs)
                    prog_match = (cand_edge[2] == progress)
                    end_match = (cand_edge[3] != len(self.tokens))  \
                                if (nth_rhs < len(arc[0].rhs()) - 1) \
                                else (cand_edge[3] == arc[3])
                    if (symb_match and prog_match and end_match):
                        alt_arcs.append(list(cand_edge))

            while alt_arcs:
                tmp_arc = list(alt_arcs.pop()) # remove the last item in list
                tmp_state = (list(parse_tree), tmp_arc, nth_rhs)
                self.tmp_storage.insert(0, tmp_state)
            
            alt_arc = list((self.tmp_storage.pop(0))[1])
            parse_tree.append(list(self.__build_parse_tree(alt_arc)))
            progress = alt_arc[3]
        
        return list(parse_tree)


    # arc = (rule, dot_progress, begin_idx, dot_idx)
    def __is_terminant(self, arc):
        return (arc[3] - arc[2] == 1)

    
    # format list to type 'nltk.tree.Tree'
    def __format_parse_tree(self, parse_list):
        tmp_str_a = str(parse_list)
        tmp_str_b = tmp_str_a.replace("[", "(")
        tmp_str_c = tmp_str_b.replace("]", ")")
        tmp_str_d = tmp_str_c.replace(" -> ", " ")
        tmp_str_e = tmp_str_d.replace(",", "")
        tmp_str_f = tmp_str_e.replace("'", "")
        parse_tree = Tree.fromstring(tmp_str_f)
        return parse_tree


    def __get_top_level_arc(self, passive_edges):
        top_arc = None
        for edge in passive_edges:
            check_symbol = (str(edge[0].lhs()) == str(self.start_symbol))
            check_bidx = (edge[2] == 0)
            check_didx = (edge[3] == len(self.tokens))
            s_check = check_symbol and check_bidx and check_didx
            if s_check is True:
                top_arc = edge
                break
        return top_arc


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    def __extract_passive_edges(self, chart):
        passive_edges = []
        for edge in chart:
            if (self.__is_complete(edge)):
                passive_edges.append(edge)
        return passive_edges


    # HACK: want to share this function with Parser class
    # returns True if edge is passive, False if active
    def __is_complete(self, edge):
        rhs_length = len(edge[0].rhs())
        dot_progress = edge[1]
        return (rhs_length == dot_progress)
