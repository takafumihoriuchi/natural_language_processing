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
    def get_tree(self):
        self.passive_edges = self.__extract_passive_edges(self.chart)
        top_arc = self.__get_top_level_arc(self.passive_edges)
        if top_arc is None:
            print("FAILURE: no successful parse found")
            return None
        parse_tree = self.__find_parse_tree(top_arc)
        formatted_parse_tree = self.__format_parse_tree(parse_tree)
        # ここでは、'nltk.tree.Tree' の list を返したい
        return formatted_parse_tree


    def __find_parse_tree(self, top_arc):
        self.parse_tree_list = []
        print("==========================")
        parse_tree = self.__build_tree(top_arc)
        print(parse_tree)
        return parse_tree


    # return "list of parse-tree-lists"
    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # start: __find_parse_tree(passive_edges, [], top_arc)
    def __build_tree(self, arc):
        if (arc[3] - arc[2] == 1): # base case
            return [arc[0]] # terminant
        parse_tree = [arc[0].lhs()]
        progress = arc[2]
        for each_rhs in arc[0].rhs():
            for cand_edge in self.passive_edges:
                symb_match = (cand_edge[0].lhs() == each_rhs)
                prog_match = (cand_edge[2] == progress)
                if (symb_match and prog_match):
                    parse_tree.append(self.__build_tree(cand_edge))
                    progress = cand_edge[3]
                    break
        return parse_tree

    
    # format list to type 'nltk.tree.Tree'
    def __format_parse_tree(self, parse_list):
        tmp_str = str(parse_list)
        tmp_str = tmp_str.replace("[", "(")
        tmp_str = tmp_str.replace("]", ")")
        tmp_str = tmp_str.replace(" -> ", " ")
        tmp_str = tmp_str.replace(",", "")
        tmp_str = tmp_str.replace("'", "")
        parse_tree = Tree.fromstring(tmp_str)
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
