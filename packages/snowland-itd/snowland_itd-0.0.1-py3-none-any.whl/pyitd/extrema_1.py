#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: extrema_1.py
# @time: 2019/4/1 21:42
# @Software: PyCharm


__author__ = 'A.Star'

import numpy as np


class Extrema(object):
    def extrema(self, x):
        d1 = x[1:] - x[:-1]
        up = d1 >= 0
        down = d1 <= 0
        max_index = np.where(up[:-1] and down[1:]) + 1
        min_index = np.where(up[1:] and down[:-1]) + 1
        T = np.hstack((max_index, min_index, 0, len(x) - 1))
        np.sort(T)
        k = len(T)
        return k, T
