"""
author : takafumihoriuchi
created in July of 2018
"""
import os
import signal
from nltk import Tree


class TreeGenerator(object):
    
    def __init__(self, chart, tokens, start_symbol='S'):
        self.chart = chart
        self.tokens = tokens
        self.start_symbol = start_symbol


    # returns a list of trees, each in nltk.tree.Tree type
    # guaranteed that there is at least one parse tree
    def get_tree(self):
        passive_edges = self.__extract_passive_edges(self.chart)
        top_arc = self.__get_top_level_arc(passive_edges)
        if top_arc is None:
            print("FAILURE: no successful parse was found")
            return None
        #####

        # 使うことのできる arc：
        print("==============================")
        print("passive_edges:")
        for edge in passive_edges:
            print(edge)
        print("==============================")
        parse_tree = self.__find_parse_tree(passive_edges, top_arc)
        print("parse_tree:")
        print(parse_tree)
        print("==============================")

        # treeを返す
        # 最終的には、ファイルに書き出して、string型で読みだして、それをTreeの形式に変更する？
        # 一次生成したファイルは、削除するのも忘れずに
        return parse_tree
        #####


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # start: __find_parse_tree(passive_edges, [], top_arc)
    def __find_parse_tree(self, passive_edges, arc):
        parse_tree = [arc[0]]
        # parse_tree = [arc[0].lhs()] # 木を作るときにはこちらを使う
        if (arc[3] - arc[2] == 1): # base case
            return [arc[0]] # terminant
        progress = arc[2]
        for each_rhs in arc[0].rhs():
            cand_list = []
            for edge in passive_edges:
                if (edge[0].lhs() == each_rhs) and (edge[2] == progress):
                    cand_list.append(edge)
            for cand_edge in cand_list:
                parse_tree.append(self.__find_parse_tree(passive_edges, cand_edge))
                progress = cand_edge[3]
                break
                # ここまでのparse_treeをまるっとコピーして、完全に新しく続きを作りたい
        return parse_tree


    """
    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # start: __find_parse_tree(passive_edges, [], top_arc)
    def __find_parse_tree(self, passive_edges, arc):
        parse_tree = [arc[0]]
        # parse_tree = [arc[0].lhs()] # 木を作るときにはこちらを使う
        if (arc[3] - arc[2] == 1): # base case
            return [arc[0]] # terminant
        progress = arc[2]
        for each_rhs in arc[0].rhs():
            for cand_edge in passive_edges:
                if (cand_edge[0].lhs() == each_rhs) and (cand_edge[2] == progress):
                    parse_tree.append(self.__find_parse_tree(passive_edges, cand_edge))
                    progress = cand_edge[3]
                    break
        return parse_tree
    """



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
