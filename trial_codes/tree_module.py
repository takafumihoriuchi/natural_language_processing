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


        ###
        # ここを埋める
        # passive_edgesのedgesからtreeを作る
        ###
        # attempt 1; can find the first tree only (for updating 'progress'), by luck
        tree_candidate = []
        tree_candidate.append(top_arc)
        tmp_queue = []
        tmp_queue.append(top_arc)

        while tmp_queue:
            tmp_edge = tmp_queue.pop(0)
            progress = tmp_edge[2]
            if (tmp_edge[3] - tmp_edge[2] <= 1):
                continue
            for tmp_rhs in tmp_edge[0].rhs():
                for edge in passive_edges:
                    if (edge[0].lhs() == tmp_rhs) and (edge[2] == progress):
                        tmp_queue.append(edge)
                        tree_candidate.append(edge)
                        progress = edge[3] # ここで進めてしまう前に、ほかの候補も欲しい
        
        print(tree_candidate)

        print("==============================")
        parse_tree = self.__find_parse_tree(passive_edges, [], top_arc)
        print("parse_tree:")
        print(parse_tree)
        print("==============================")
        ###

        # treeを返す
        return []
        #####


    def __find_parse_tree(self, passive_edges, parse_tree, arc):
        pass



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
