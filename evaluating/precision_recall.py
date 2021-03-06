#!/usr/bin/env python
# coding=utf-8

# 计算推荐系统的precision和recall指标

import os
import numpy as np


def precision(rec_list, play_list):
    """
    为某个用户计算准确率
    :param rec_list: 给该用户的推荐列表，  类型 <type 'numpy.ndarray'> or list
    :param play_list: 该用户的真实播放列表， 类型 <type 'numpy.ndarray'> or list
    :return: 准确率
    """
    inter = set(rec_list).intersection(set(play_list))
    return float(len(inter))/len(rec_list)


def recall(rec_list, play_list):
    """
    为某个用户计算召回率
    :param rec_list: 给该用户的推荐列表，  类型 <type 'numpy.ndarray'>
    :param play_list: 该用户的真实播放列表， 类型 <type 'numpy.ndarray'>
    :return: 召回率
    """
    inter = set(rec_list).intersection(set(play_list))
    return float(len(inter))/len(play_list)


cwd = os.getcwd()  # 获取当前工作目录
f_path = os.path.abspath(os.path.join(cwd, ".."))  # 获取上一级目录

test_play_action_f = f_path + "/output/test_play_action.npy"
item_based_rec_f = f_path + "/output/item_based_rec.npy"

play_map = np.load(test_play_action_f, allow_pickle=True).item()
rec_map = np.load(item_based_rec_f, allow_pickle=True).item()

recall_accumulate = 0
precision_accumulate = 0
rec_u_set = set()

print("===================开始为计算总体召回&排序==================")
# item-based推荐的数据结构如下：
# {u1: [(1905, 0.5), (2452, 0.3), (3938, 0.1)]}
# play_map数据结构如下：
# {2097129: set([(3049, 2), (3701, 4), (3756, 3)]), 1048551: set([(3610, 4), (571, 3)])}
i = 0
for u, rec_u_with_score in rec_map.items():
    if i % 100 == 0:
        print(i)
        i = i + 1
    rec_u_set.add(u)
    if u in play_map:
        play_u_with_score = play_map[u]
        rec_u = [u for (u, _) in rec_u_with_score]
        play_u = [u for (u, _) in play_u_with_score]
        precision_u = precision(rec_u, play_u)
        recall_u = recall(rec_u, play_u)
        precision_accumulate = precision_accumulate + precision_u
        recall_accumulate = recall_accumulate + recall_u

print("===================计算完总体召回&排序==================")


user_num = len(rec_u_set.intersection((set(play_map.keys()))))

precision = precision_accumulate/user_num
recall = recall_accumulate/user_num

print("precision=" + str(precision))
print("recall=" + str(recall))

