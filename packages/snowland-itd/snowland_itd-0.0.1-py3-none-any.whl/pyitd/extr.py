#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: extr.py
# @time: 2019/4/1 21:42
# @Software: PyCharm


__author__ = 'A.Star'

import numpy as np

npa = np.array
from pyitd.common import equals_zero
from abc import ABCMeta,abstractmethod


class BaseExtr(metaclass=ABCMeta):
    @abstractmethod
    def extrema(self, *args, **kwargs):
        pass


class Extr(BaseExtr):
    def __init__(self, *args, **kwargs):
        pass

    def extrema(self, x, t=None, *args, **kwargs):
        d1 = x[1:] - x[:-1]
        up = d1 >= 0
        down = d1 <= 0
        max_index = np.where(up[:-1] * down[1:])[0] + 1
        min_index = np.where(up[1:] * down[:-1])[0] + 1
        return min_index, max_index
