#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: common.py
# @time: 2019/4/1 23:01
# @Software: PyCharm


__author__ = 'A.Star'

eps = 1e-6
import numpy as np


def equals_zero(x):
    if isinstance(x, np.ndarray):
        return (-eps < x) * (x < eps)
    if isinstance(x, list):
        return [-eps < each_x < eps for each_x in x]
    raise ValueError('data must be ndarray')
