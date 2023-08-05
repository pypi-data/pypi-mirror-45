#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: itd.py
# @time: 2019/4/1 21:39
# @Software: PyCharm


__author__ = 'A.Star'

import numpy as np
import scipy
from pyitd.extr import Extr, BaseExtr
from pyitd.boundary_conditions import BoundaryConditions, BaseBoundaryConditions

npa = np.array
from matplotlib import pyplot as plt
from pyitd.common import equals_zero


class ITD():
    def __init__(self,
                 extr=Extr,
                 boundary_conditions=BoundaryConditions,
                 *args,
                 **kwargs
                 ):
        """
        :param x: Vector 信号
        :param n:
        :param err:
        :param extr:
        :param boundary_conditions:
        """

        if issubclass(extr, BaseExtr):
            self.extr = extr(*args, **kwargs)
        else:
            raise ValueError('value error')

        if issubclass(boundary_conditions, BaseBoundaryConditions):
            self.boundary_conditions = boundary_conditions(*args, **kwargs)
        else:
            raise ValueError('value error')

    def itd_base_decomp(self, x, err=1e-5, t=None, nbsym=1):
        """
        将信号x进行分解一层ITD分解
        H表示固有旋转分量
        LL表示基信号
        :return:
        """
        length = len(x)
        t = t if t is not None else np.arange(length)
        indmin, indmax = self.extr.extrema(x)  # 提取极值点，不区分极大值极小值
        index = sorted(np.hstack((0, indmin, indmax, length)))
        # plt.plot(x)
        # plt.plot(indmin, x, 'r+')
        # plt.plot(indmin, x[indmin], 'r+')
        # plt.plot(indmax, x[indmax], 'g+')
        # plt.show()

        # indmin, indmax = self.extr()  # 区分极值大值和极小值
        # 衍生虚极值点，抑制端点效应
        # 信号的左右两端分别添加一个极小值和极大值，1 表示数量
        tlmin, tlmax, zlmin, zlmax, trmin, trmax, zrmin, zrmax = \
            self.boundary_conditions.boundary_conditions(indmin, indmax, t, x, x, nbsym)

        if np.all(tlmin < tlmax):
            if np.all(trmin < trmax):
                newT = np.arange(tlmin, trmax + 1)  # 新的数据点区间，左右都增加了一个极小值和极大值
                # 之所以从第2个极点开始，那是因为虚构点的时候把第一个点当做虚构极值点了
                # 最后一个点也当做虚构极值点了，所以最后一个极值点也不取
                newExtr = np.hstack((tlmin, tlmax, t[index[1:- 1]], trmin, trmax))  # 左右两端的衍生极值点和原来极值点
                newX = np.hstack((zlmin, zlmax, x[index[1:-1]], zrmin, zrmax))  # 左右两端的衍生极值点和原来极值点对应的极值
            else:  # if trmin > trmax:
                newT = np.arange(tlmin, trmin + 1)
                newExtr = np.hstack((tlmin, tlmax, t[index[1:-1]], trmax, trmin))
                newX = np.hstack((zlmin, zlmax, x[index[1:-1]], zrmax, zrmin))

        else:  # tlmin < tlmax
            if trmin <= trmax:
                newT = np.arange(tlmax, trmax + 1)
                newExtr = np.hstack((tlmax, tlmin, x[index[1:- 1]], trmin, trmax))
                newX = np.hstack((zlmax, zlmin, x[index[1: - 1]], zrmin, zrmax))
            elif trmin > trmax:
                newT = np.hstack((tlmax, trmin))
                newExtr = np.hstack((tlmax, tlmin, t[index[1: - 1]], trmax, trmin))
                newX = np.hstack((zlmax, zlmin, x[index[1: - 1]], zrmax, zrmin))
        a = 0.5
        L = self.interp(newX, newExtr, a=a)
        LL = np.zeros(length)
        ind = 0
        diff_newX = newX[2 * nbsym:] - newX[2 * nbsym - 1:-2 * nbsym + 1]
        diff_L = L[1:] - L[:-1]
        for k, diff_Lk in enumerate(diff_L):
            p = np.arange(index[k], index[k + 1], dtype=np.int64)  # 原极值点之间的序号, 映射到原区间上
            # if not equals_zero((newX[k + 1] - newX[k]) * (x[p] - newX[k])).any():
            temp = L[k] + diff_Lk / diff_newX[k] * (x[p] - newX[k + 1])
            LL[ind: ind + len(temp)] = npa(temp)  # 基线信号
            ind += len(temp)
        H = x - LL
        return H, LL

    def interp(self, newX, newIndex, a=0.5, nbsym=1, *args, **kwargs):
        """
        :param newX: 新的极值点值
        :param newIndex: 新的极值点索引
        :param a: 一个变量
        :return:
        """
        L = a * (newX[:-2 * nbsym] + ((newIndex[nbsym:-nbsym] - newIndex[:-2 * nbsym]) / (
                newIndex[2 * nbsym:] - newIndex[:-2 * nbsym])) * (newX[2 * nbsym:] - newX[:-2 * nbsym])) + (
                    1 - a) * newX[nbsym:-nbsym]
        return L

    def run(self, x, n, err=1e-5, t=None):
        """
        将信号x进行ITD分解
        n分解最大层数
        err
        :return:
        """
        t = t if t is not None else np.arange(len(x))
        tempH1, tempL = self.itd_base_decomp(x, t=t)
        H = [tempH1]
        for i in range(n):
            tempH, tempL = self.itd_base_decomp(tempL, t=t)
            H.append(tempH)
            # ----终止条件
            if self.stop(tempL, err=err):
                break
        L = tempL
        return H, L

    def stop(self, x, err=1e-5, *args, **kwargs):
        return self.monotone(x) or (np.all(x < err) and np.all(x > err))

    def monotone(self, xx):
        # 求是否单调函数
        x1 = np.diff(xx)
        return np.all(x1 >= 0) or np.all(x1 <= 0)
