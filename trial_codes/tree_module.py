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
        #####

        # 使うことのできる arc：
        print("==============================")
        print("passive_edges:")
        for edge in self.passive_edges:
            print(edge)
        print("==============================")
        parse_tree = self.__find_parse_tree(top_arc)
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
    def __find_parse_tree(self, top_arc):
        np_rules = self.__get_rule_lhs_of(top_arc[0].rhs()[0], begin_idx=0)
        np_progress = np_rules[0][3]
        # 本当はここでNP_ruleのprogressを返して欲しい、しかし、複数個あった場合はどうする？
        vp_rules = self.__get_rule_lhs_of(top_arc[0].rhs()[1], end_idx=len(self.tokens))
        
        for vp_rule in vp_rules:
            v_rules = self.__get_rule_lhs_of(vp_rule[0].rhs()[0], begin_idx=np_progress)
            np_rules_2 = self.__get_rule_lhs_of(vp_rule[0].rhs()[1], end_idx=len(self.tokens))
            


    def __rhs_is_terminant(self, arc):
        return (arc[3] - arc[2] == 1)

    # returns: (matching_rules, end_idx)
    def __get_rule_lhs_of(self, left_sym, begin_idx=None, end_idx=None):
        matching_rules = []
        for arc in self.passive_edges:
            flg_sym = (arc[0].lhs() == left_sym)
            flg_beg = True if (begin_idx == None) else (arc[2] == begin_idx)
            flg_end = True if (end_idx == None) else (arc[3] == end_idx)
            if (flg_sym and flg_beg and flg_end):
                matching_rules.append(arc)
        return matching_rules



    



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





"""
    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # start: __find_parse_tree(passive_edges, [], top_arc)
    def __find_parse_tree(self, passive_edges, arc):
        parse_tree = [arc[0]]
        # parse_tree = [arc[0].lhs()] # 木を作るときにはこちらを使う
        if (arc[3] - arc[2] == 1): # base case
            return [arc[0]] # terminant
        prog_list = [arc[2]]
        for each_rhs in arc[0].rhs():
            for progress in prog_list:
                cand_list = []
                for edge in passive_edges:
                    if (edge[0].lhs() == each_rhs) and (edge[2] == progress):
                        cand_list.append(edge)
                        prog_list.append(edge[3])
                for cand_edge in cand_list:
                    parse_tree.append(self.__find_parse_tree(passive_edges, cand_edge))
                    # ここまでのparse_treeをまるっとコピーして、完全に新しく続きを作りたい
        return parse_tree


    # edge = (rule, dot_progress, begin_idx, dot_idx)
    # start: __find_parse_tree(passive_edges, [], top_arc)
    def __find_parse_tree(self, passive_edges, arc):
        parse_tree = [arc[0]]
        # parse_tree = [arc[0].lhs()] # 木を作るときにはこちらを使う
        if (arc[3] - arc[2] == 1): # base case
            return [arc[0]] # terminant
        progress = arc[2]
        prog_list = []
        for each_rhs in arc[0].rhs():
            cand_list = []
            for edge in passive_edges:
                if (edge[0].lhs() == each_rhs) and (edge[2] == progress):
                    cand_list.append(edge)
                    prog_list.append(edge[3])
            for cand_edge in cand_list:
                parse_tree.append(self.__find_parse_tree(passive_edges, cand_edge))
                progress = cand_edge[3]
                break
                # ここまでのparse_treeをまるっとコピーして、完全に新しく続きを作りたい
        return parse_tree



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
