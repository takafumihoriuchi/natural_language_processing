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


    def get_tree(self):
        passive_edges = self.__extract_passive_edges(self.chart)
        top_arc = self.__get_top_level_arc(passive_edges)
        if top_arc is None:
            print("FAILURE: no successful parse was found")
            return None
        #####

        # 使うことのできる arc：
        print("==============================")
        for edge in passive_edges:
            print(edge)
        print("==============================")

        # ここを埋める
        ###

        # treeを返す
        return []
        #####


    def __get_top_level_arc(self, passive_edges):
        top_arc = None
        for edge in passive_edges:
            check_symbol = (str(edge[0].lhs()) == str(self.start_symbol))
            check_bidx = (edge[2] == 0)
            check_didx = (edge[3] == len(self.tokens))
            s_check = check_symbol and check_bidx and check_didx
            if s_check is True:
                top_arc = edge
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
