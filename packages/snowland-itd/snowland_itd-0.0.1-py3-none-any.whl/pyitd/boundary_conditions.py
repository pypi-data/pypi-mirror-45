#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: boundary_conditions.py
# @time: 2019/4/1 21:43
# @Software: PyCharm


__author__ = 'A.Star'

from abc import ABCMeta, abstractmethod
import numpy as np


class BaseBoundaryConditions(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def boundary_conditions(self, x, *args, **kwargs):
        pass


class BoundaryConditions(BaseBoundaryConditions):
    name = 'default_boundary_conditions'

    def __init__(self, *args, **kwargs):
        pass

    def boundary_conditions(self, indmin, indmax, t, x, z, nbsym):

        lx = len(x)
        t = np.arange(lx) if t is None else t
        if len(indmin) + len(indmax) < 3:
            raise ValueError('not enough extrema')

        if indmax[0] < indmin[0]:
            if x[0] > x[indmin[0]]:
                lmax = indmax[nbsym:0:-1]  # pass
                lmin = indmin[nbsym:0:-1]  # pass
                lsym = indmax[0]
            else:
                lmax = indmax[nbsym:0:-1]
                lmin = np.hstack((indmin[nbsym - 1:0:-1], 0))
                lsym = 0
        else:
            if x[0] < x[indmax[0]]:
                lmax = indmax[min(lx, nbsym) - 1::-1]  # pass
                lmin = indmin[min(lx, nbsym):0:-1]  # pass
                lsym = indmin[0]
            else:
                lmax = np.hstack((indmax[nbsym - 1:0:-1], 0))
                lmin = indmin[nbsym - 1::-1]
                lsym = 0

        if indmax[-1] < indmin[-1]:
            if x[-1] <= x[indmax[-1]]:
                rmax = (indmax[-1:-nbsym - 1:-1])
                rmin = (indmin[-1:-nbsym - 1:-1])
                rsym = indmin[-1]
            else:
                rmax = np.hstack((lx - 1, (indmax[-1:-nbsym:-1])))
                rmin = indmin[-1:-nbsym - 1:-1]
                rsym = lx - 1
        else:
            if x[-1] >= x[indmin[-1]]:
                rmax = indmax[-2:-nbsym - 2:-1]  # pass, 去除最后一个点（端点），所以-2
                rmin = indmin[-1:-nbsym - 1:-1]
                rsym = indmax[-1]
            else:
                rmax = indmax[-1:-nbsym - 1:-1]
                rmin = np.hstack((lx - 1, indmin[-1:- nbsym:-1]))
                rsym = lx - 1
        try:
            tlmin = 2 * t[lsym] - t[lmin]
            tlmax = 2 * t[lsym] - t[lmax]
            trmin = 2 * t[rsym] - t[rmin]
            trmax = 2 * t[rsym] - t[rmax]
        except:
            aaa = 1
        # in case symmetrized parts do not extend enough
        if tlmin[0] > t[0] or tlmax[0] > t[0]:
            if lsym == indmax[0]:
                lmax = indmax[nbsym - 1::-1]
            else:
                lmin = indmin[nbsym - 1::-1]
            if lsym == 0:
                raise ValueError('bug')
            tlmin = 2 * t[0] - t[lmin]
            tlmax = 2 * t[0] - t[lmax]

        if trmin[-1] < t[-1] or trmax[-1] < t[-1]:
            if rsym == indmax[-1]:
                rmax = indmax[-1:-nbsym - 1:-1]
            else:
                rmin = indmin[-1:-nbsym - 1:-1]  # TODO  check

            if rsym == lx:
                raise ValueError('bug')
            trmin = 2 * t[-1] - t[rmin]
            trmax = 2 * t[-1] - t[rmax]

        zlmax = z[lmax]
        zlmin = z[lmin]
        zrmax = z[rmax]
        zrmin = z[rmin]

        # tmin = np.hstack((tlmin, t[indmin], trmin))
        # tmax = np.hstack((tlmax, t[indmax], trmax))
        # zmin = np.hstack((zlmin, z[indmin], zrmin))
        # zmax = np.hstack((zlmax, z[indmax], zrmax))
        return tlmin, tlmax, zlmin, zlmax, trmin, trmax, zrmin, zrmax
