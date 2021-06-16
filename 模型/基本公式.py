# -*- coding: utf-8 -*-
# @Time    : 1月 2021/1/19 19:16
# @Author  : VerNe
# @Email   : 1716200584@qq.com
# @File    : 基本公式.py
# @Software: PyCharm

import numpy as np
import math
import random
import prettytable as pt
from decimal import Decimal
import matplotlib.pyplot as plt
# from scipy.interpolate import spline
import spline
import scipy.interpolate as si

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def 指定概率随机数(num, probability):
    assert len(num) == len(probability), "Length does not match."
    assert sum(probability) == 1, "Total rate is not 1."

    sup_list = [len(str(i).split(".")[-1]) for i in probability]
    top = 10 ** max(sup_list)
    new_rate = [int(i * top) for i in probability]
    rate_arr = []
    for i in range(1, len(new_rate) + 1):
        rate_arr.append(sum(new_rate[:i]))
    rand = random.randint(1, top)
    data = None
    for i in range(len(rate_arr)):
        if rand <= rate_arr[i]:
            data = num[i]
            break
    return data


def 空气比焓(空气温度):
    比焓数值 = 4.6020 + 0.9705 * 空气温度 + 3.3955e-5 * 空气温度 ** 2 + 5.5267e-8 * 空气温度 ** 3 - 1.697e-11 * 空气温度 ** 4
    return 比焓数值


def 水比热(水温度):
    比热数值 = 0.00000000000001281201 * 水温度 ** 5 + 0.00000000049564489549 * 水温度 ** 4 - 0.00000076534745908593 * 水温度 ** 3 + 0.00044437700352624400 * 水温度 ** 2 - 0.11483332074518400000 * 水温度 ** 1 + 15.25746646735990000000
    return 比热数值


def 空气比热(空气温度):
    比热数值 = 0.9705 + 6.791e-5 * 空气温度 + 1.658e-7 * 空气温度 ** 2 - 6.788e-11 * 空气温度 ** 3
    return 比热数值


def 导热油比热(导热油温度):
    temp = 导热油温度 - 273.15
    比热数值 = 1.2266 + 0.0014 * temp
    return 比热数值


def 表格输出(dict):
    tb = pt.PrettyTable()
    tb.field_names = [dict['名字'], '', '单位']
    tb.align[dict['名字']] = 'l'
    tb.align['单位'] = 'l'
    tb.align[''] = 'r'
    tb.reversesort = True
    dict_temp = {}
    for k in list(dict.keys()):
        if dict[k] == 0:
            dict_temp[k] = dict[k]
            del dict[k]
    temp = dict['名字']
    # print(dict['name'] + ':')
    dict.pop('名字')

    for key in list(dict.keys()):
        if key.find('压强') != -1:
            tb.add_row([key, round(dict[key], 2), 'Pa'])
        elif key.find('温度') != -1:
            tb.add_row([key, round(dict[key], 2), 'K'])
        elif key.find('流速') != -1:
            tb.add_row([key, round(dict[key] * 1000, 2), 'kg/s'])
        elif key.find('能量') != -1:
            tb.add_row([key, round(dict[key], 2), 'MW'])
        elif key.find('电量') != -1:
            tb.add_row([key, round(dict[key], 2), 'MW'])
        elif key.find('做功') != -1:
            tb.add_row([key, round(dict[key], 2), 'MW'])
        else:
            tb.add_row([key, round(dict[key], 2), ''])
    # print(dict)
    dict['名字'] = temp
    for K in list(dict_temp.keys()):
        dict[K] = dict_temp[K]
    print('*' * 50)
    print(tb)
    print('')
    return 0


def 画图输出(数据, 是否拟合=False, 是否开启网格线=True):  # 是否拟合=True：是 / 是否拟合=False：否
    def 拟合(x, y):
        xnew = np.linspace(x.min(), x.max(),
                           300 * len(x))  # 300 represents number of points to make between T.min and T.max
        power_smooth = spline(x, y, xnew)
        返回参数 = {
            'power_smooth': power_smooth,
            'xnew': xnew
        }
        return 返回参数

    plt.figure(dpi=200,figsize=(4, 2.5))
    if 'y3' in 数据.keys():
        if 是否拟合 == True:
            数组1 = 拟合(x=数据['x1'], y=数据['y1'])
            数据['y1'] = 数组1['power_smooth']
            数据['x1'] = 数组1['xnew']
            数组2 = 拟合(x=数据['x2'], y=数据['y2'])
            数据['y2'] = 数组2['power_smooth']
            数据['x2'] = 数组2['xnew']
            数组3 = 拟合(x=数据['x3'], y=数据['y3'])
            数据['y3'] = 数组3['power_smooth']
            数据['x3'] = 数组3['xnew']
        x1, = plt.plot(数据['x1'], 数据['y1'], color='b', alpha=0.5)
        x2, = plt.plot(数据['x2'], 数据['y2'], color='r', alpha=0.3)
        x3, = plt.plot(数据['x3'], 数据['y3'], color='g', alpha=0.5)
        # plt.title(数据['表题'])
        plt.legend(handles=[x1, x2, x3],
                   labels=[数据['标签1'], 数据['标签2'], 数据['标签3']],fontsize='xx-small',loc='best')
    elif 'y2' in 数据.keys():
        if 是否拟合 == 1:
            数组1 = 拟合(x=数据['x1'], y=数据['y1'])
            数据['y1'] = 数组1['power_smooth']
            数据['x1'] = 数组1['xnew']
            数组2 = 拟合(x=数据['x2'], y=数据['y2'])
            数据['y2'] = 数组2['power_smooth']
            数据['x2'] = 数组2['xnew']
        x1, = plt.plot(数据['x1'], 数据['y1'], color='b', alpha=0.5)
        x2, = plt.plot(数据['x2'], 数据['y2'], color='r', alpha=0.3)
        # plt.title(数据['表题'])
        plt.legend(handles=[x1, x2],
                   labels=[数据['标签1'], 数据['标签2']],fontsize='xx-small',loc='best')
    elif 'y1' in 数据.keys():
        if 是否拟合 == 1:
            数组1 = 拟合(x=数据['x1'], y=数据['y1'])
            数据['y1'] = 数组1['power_smooth']
            数据['x1'] = 数组1['xnew']
        x1, = plt.plot(数据['x1'], 数据['y1'], color='b', alpha=0.5)
        # plt.title(数据['表题'])

    if 是否开启网格线 == True:
        plt.grid()
    plt.xlabel(数据['横坐标'])
    plt.ylabel(数据['纵坐标'])
    plt.tight_layout()
    plt.show()


def 变工况压比(入口空气流速, 入口温度, 入口压强, 标准温度=712.6908917372385, 标准压强=219074.5173990744, 标准空气流速=0.004,
          标准压比=3.5):
    标准温度 = 298.15
    标准压强 = 101.325 * 1000

    '''
    在稳态的时候使用 水底/水面开三次方根
    变工况的时候使用 固定值 3.5最为接近我们所需要的值
    '''

    def c_1(nc):
        return nc / (1.8 * (1 - 1.8 / nc) + nc * (nc - 1.8) ** 2)

    def c_2(nc):
        return (1.8 - 3.6 * nc ** 2) / (1.8 * (1 - 1.8 / nc) + nc * (nc - 1.8) ** 2)

    def c_3(nc):
        return -(3.24 * nc - 3.24 * nc ** 3) / (1.8 * (1 - 1.8 / nc) + nc * (nc - 1.8) ** 2)

    def pai_c(Gc, nc):
        return c_1(nc) * Gc ** 2 + c_2(nc) * Gc + c_3(nc)

    def n_c(T, T0):
        # return (1 / math.sqrt(T)) / (1 / math.sqrt(T0))
        return 1

    '''
    nc*用1的图像是可以看的
    用公式计算的图像则很神奇
    '''

    def G_c(T, T0, P, P0, mass_flow, mass_flow_0):
        return (mass_flow * math.sqrt(T) / P) / (mass_flow_0 * math.sqrt(T0) / P0)

    def pai_real(Gc, nc, compression_ratio):
        return pai_c(Gc, nc) * compression_ratio

    Gc = G_c(T=入口温度, T0=标准温度, P=入口压强, P0=标准压强, mass_flow=入口空气流速, mass_flow_0=标准空气流速)
    nc = n_c(T=入口温度, T0=标准温度)
    return abs(pai_real(Gc=Gc, nc=nc, compression_ratio=标准压比))


def scipy_bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
    """
    cv = np.asarray(cv)
    count = cv.shape[0]

    # Closed curve
    if periodic:
        kv = np.arange(-degree, count + degree + 1)
        factor, fraction = divmod(count + degree + 1, count)
        cv = np.roll(np.concatenate((cv,) * factor + (cv[:fraction],)), -1, axis=0)
        degree = np.clip(degree, 1, degree)

    # Opened curve
    else:
        degree = np.clip(degree, 1, count - 1)
        kv = np.clip(np.arange(count + degree + 1) - degree, 0, count - degree)

    # Return samples
    max_param = count - (degree * (1 - periodic))
    spl = si.BSpline(kv, cv, degree)
    return spl(np.linspace(0, max_param, n))


if __name__ == '__main__':
    print((空气比焓(762) - 空气比焓(298)) * 0.0085)
