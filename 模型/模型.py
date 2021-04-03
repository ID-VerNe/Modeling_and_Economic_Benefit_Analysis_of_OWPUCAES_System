# -*- coding: utf-8 -*-
# @Time    : 1月 2021/1/19 18:58
# @Author  : VerNe
# @Email   : 1716200584@qq.com
# @File    : 模型.py
# @Software: PyCharm

import numpy as np
import 模型.基本公式 as 基本公式


class 大气参数(object):
    空气温度 = 298.15
    空气压强 = 101.325 * 1000
    名字 = '大气参数'

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '空气压强': self.空气压强,
            '空气温度': self.空气温度
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 风电站(object):
    def __init__(self, 容量, 发电阈值, 上一轮发电量, 轮次=2):
        self.容量 = 容量
        self.发电阈值 = 发电阈值
        self.上一轮发电量 = 上一轮发电量
        self.轮次 = 轮次
        self.名字 = '风电站'

    def 发电量(self, 随机等级=3, 输出方法=1):  # 输出方法=1：不含阈值  ；  输出方法=2：含有阈值
        def 含有阈值的输出(发电量, 发电阈值):
            if 发电量 < 发电阈值:
                return 0
            else:
                return 发电量 - 发电阈值

        def 不含阈值的输出(发电量):
            return 发电量

        rate = self.容量 / 49.5
        wind_power_base_level = np.array([0, 0, 0, 9.8, 12.6, 15.4, 18.2, 21, 23.8, 26.6, 29.4, 32.2, 35, 0, 0, 0])
        wind_power_real_level = wind_power_base_level * rate
        wind_power_probability = np.array(
            [0, 0, 0, 0.06, 0.11, 0.13, 0.11, 0.07, 0.15, 0.15, 0.06, 0.11, 0.05, 0, 0, 0])
        '''
        数据来源：
        考虑风电不确定性的分时电价研究_闫晔
        '''
        if self.轮次 == 1:  # 第一次用Time=1，第二次之后用默认值就好
            发电量数值 = 基本公式.指定概率随机数(wind_power_real_level, wind_power_probability)
        else:
            index = np.argwhere(wind_power_real_level == self.上一轮发电量)[0][0]
            usable_wind_power_level = []
            usable_wind_power_level_probability = []
            jump_index = []
            for i in range(2 * 随机等级 + 1):
                jump_index.append(index + i - 随机等级)
            for i in jump_index:
                usable_wind_power_level.append(wind_power_real_level[i])
                usable_wind_power_level_probability.append(wind_power_probability[i])
            sum = np.sum(usable_wind_power_level_probability)
            usable_wind_power_level_probability = usable_wind_power_level_probability / sum
            发电量数值 = np.random.choice(usable_wind_power_level, p=usable_wind_power_level_probability)

        # 输出
        if 输出方法 == 1:
            带阈值的发电量数值 = 不含阈值的输出(发电量=发电量数值)
        else:
            带阈值的发电量数值 = 含有阈值的输出(发电量=发电量数值, 发电阈值=self.发电阈值)
        返回参数 = {
            '本轮发电量': 发电量数值,
            '带阈值的发电量数值': 带阈值的发电量数值
        }
        return 返回参数

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '轮次': self.轮次,
            '发电量': self.发电量()
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 电动机(object):

    def __init__(self, 转速, 输入电量, 效率, 序列号):
        self.转速 = 转速
        self.输入电量 = 输入电量
        self.效率 = 效率
        self.名字 = '电动机 #' + str(序列号)

    def 做功(self):
        return self.输入电量 * self.效率

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '做功': self.做功()
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 空气压缩机(object):
    热交换系数r = 1.41

    def __init__(self, 入口温度, 入口压强, 空气流速, 压比, 压缩效率, 序列号):
        self.入口温度 = 入口温度
        self.入口压强 = 入口压强
        self.空气流速 = 空气流速
        self.压比 = 压比
        self.压缩效率 = 压缩效率
        self.名字 = '空气压缩机 #' + str(序列号)

    def 出口温度(self):
        出口温度数值 = self.入口温度 + self.入口温度 * (1 / self.压缩效率) * (self.压比 ** ((self.热交换系数r - 1) / self.热交换系数r) - 1)
        return 出口温度数值

    def 出口压强(self):
        出口压强数值 = self.入口压强 * self.压比
        return 出口压强数值

    def 压缩机气体能量变化量(self):
        能量能量变化量 = self.空气流速 * (基本公式.空气比焓(空气温度=self.入口温度) - 基本公式.空气比焓(空气温度=self.出口温度()))
        return 能量能量变化量

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '空气流速': self.空气流速,
            '压比': self.压比,
            '入口温度': self.入口温度,
            '出口温度': self.出口温度(),
            '入口压强': self.入口压强,
            '出口压强': self.出口压强(),
            '气体能量变化量': self.压缩机气体能量变化量(),
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 压缩机热交换器(object):
    热交换有效度epsilon = 0.9

    def __init__(self, 入口温度, 空气流速, 冷却液温度, 冷却液流速, 序列号, 压缩机输入热量):
        self.入口温度 = 入口温度
        self.空气流速 = 空气流速
        self.冷却液温度 = 冷却液温度
        self.冷却液流速 = 冷却液流速
        self.压缩机输入热量 = 压缩机输入热量
        self.名字 = '压缩机热交换器 #' + str(序列号)

    def 出口温度(self):  # 这条式用不得
        def min(m1, m2, c1, c2):
            # print(m1 * c1)
            # print(m2 * c2)
            if m1 * c1 < m2 * c2:
                return m1 * c1
            else:
                return m2 * c2

        换热器内空气比热 = 基本公式.空气比热(空气温度=self.入口温度)  # 用入口温度计算
        换热器内冷却液比热 = 基本公式.导热油比热(导热油温度=self.冷却液温度)

        换热器出口温度 = self.入口温度 - self.热交换有效度epsilon * (
                min(self.空气流速, self.冷却液流速, 换热器内空气比热, 换热器内冷却液比热) / (self.空气流速 * 换热器内空气比热)) * (
                          self.入口温度 - self.冷却液温度)
        return 换热器出口温度

    def 出口温度_新(self):
        换热器出口温度 = self.入口温度 + self.热交换有效度epsilon * self.压缩机输入热量 / (基本公式.空气比热(self.入口温度) * self.空气流速)
        return 换热器出口温度

    def 换热器气体能量变化量(self):
        能量能量变化量 = self.空气流速 * (基本公式.空气比焓(空气温度=self.入口温度) - 基本公式.空气比焓(空气温度=self.出口温度_新()))
        return 能量能量变化量

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '空气流速': self.空气流速,
            '入口温度': self.入口温度,
            '出口温度': self.出口温度_新(),
            '气体能量变化量': self.换热器气体能量变化量(),
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 储气包(object):
    储气包深度 = 100
    温度 = 290

    def __init__(self, 上一轮容量, 入口空气流速, 出口空气流速, 压缩比):
        self.上一轮容量 = 上一轮容量
        self.入口空气流速 = 入口空气流速
        self.出口空气流速 = 出口空气流速
        self.名字 = '储气包'
        self.压强 = 压缩比 ** 3 * 大气参数.空气压强

    def 当前容量(self, 时间间隔=1):
        容量数值 = self.上一轮容量 + self.入口空气流速 * 时间间隔 - self.出口空气流速 * 时间间隔
        return 容量数值

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '储气包深度': self.储气包深度,
            '入口空气流速': self.入口空气流速,
            '出口空气流速': self.出口空气流速,
            '储气包气体温度': self.温度,
            '储气包气体压强': self.压强,
            '当前储气包容量': self.当前容量(),
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 空气膨胀机(object):
    热交换系数r = 1.41

    def __init__(self, 入口温度, 入口压强, 空气流速, 膨胀比, 膨胀效率, 序列号):
        self.入口温度 = 入口温度
        self.入口压强 = 入口压强
        self.空气流速 = 空气流速
        self.膨胀比 = 膨胀比
        self.膨胀效率 = 膨胀效率
        self.名字 = '空气膨胀机 #' + str(序列号)

    def 出口温度(self):
        出口温度数值 = self.入口温度 * (1 - self.膨胀效率 * (1 - (1 / self.膨胀比) ** ((self.热交换系数r - 1) / (self.热交换系数r))))
        return 出口温度数值

    def 出口压强(self):
        出口压强数值 = self.入口压强 / self.膨胀比
        return 出口压强数值

    def 膨胀机气体能量变化量(self):
        能量能量变化量 = self.空气流速 * (基本公式.空气比焓(空气温度=self.入口温度) - 基本公式.空气比焓(空气温度=self.出口温度()))
        return 能量能量变化量

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '空气流速': self.空气流速,
            '膨胀比': self.膨胀比,
            '入口温度': self.入口温度,
            '出口温度': self.出口温度(),
            '入口压强': self.入口压强,
            '出口压强': self.出口压强(),
            '气体能量变化量': self.膨胀机气体能量变化量(),
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 膨胀机热交换器(object):
    热交换有效度epsilon = 0.9

    def __init__(self, 入口温度, 空气流速, 冷却液温度, 冷却液流速, 序列号, 压缩机热交换器输入热量):
        self.入口温度 = 入口温度
        self.空气流速 = 空气流速
        self.冷却液温度 = 冷却液温度
        self.冷却液流速 = 冷却液流速
        self.压缩机热交换器输入热量 = 压缩机热交换器输入热量
        self.名字 = '膨胀机热交换器 #' + str(序列号)

    def 出口温度(self):
        def min(m1, m2, c1, c2):
            # print(m1 * c1)
            # print(m2 * c2)
            if m1 * c1 < m2 * c2:
                return m1 * c1
            else:
                return m2 * c2

        换热器内空气比热 = 基本公式.空气比热(空气温度=self.入口温度)  # 用入口温度计算
        换热器内冷却液比热 = 基本公式.导热油比热(导热油温度=self.冷却液温度)
        换热器出口温度 = self.入口温度 + self.热交换有效度epsilon * (self.冷却液温度 - self.入口温度) * (
                min(self.空气流速, self.冷却液流速, 换热器内空气比热, 换热器内冷却液比热) / (self.空气流速 * 换热器内空气比热))
        return 换热器出口温度

    # def 出口温度_新(self):
    #     换热器出口温度 = self.入口温度 + self.热交换有效度epsilon * self.压缩机热交换器输入热量 / 3 / (基本公式.空气比热(self.入口温度) * self.空气流速)
    #     return 换热器出口温度

    def 换热器气体能量变化量(self):
        能量能量变化量 = self.空气流速 * (基本公式.空气比焓(空气温度=self.入口温度) - 基本公式.空气比焓(空气温度=self.出口温度()))
        return 能量能量变化量

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '空气流速': self.空气流速,
            '入口温度': self.入口温度,
            '出口温度': self.出口温度(),
            '气体能量变化量': self.换热器气体能量变化量(),
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 发电机(object):

    def __init__(self, 输入电量, 效率, 序列号):
        self.输入电量 = 输入电量
        self.效率 = 效率
        self.名字 = '发电机 #' + str(序列号)

    def 发电量(self):
        return self.输入电量 * self.效率

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '发电量': self.发电量()
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 储热罐(object):

    def __init__(self, 上一轮温度, 导热油流速, 压缩机换热器输出的热量):
        self.名字 = '储热罐'
        self.上一轮温度 = 上一轮温度
        self.导热油流速 = 导热油流速
        self.压缩机换热器输出的热量 = 压缩机换热器输出的热量

    def 本轮导热油温度(self):
        导热油比热 = 基本公式.导热油比热(self.上一轮温度)
        温度变化量 = self.压缩机换热器输出的热量 * 0.9 / (导热油比热 * self.导热油流速)
        return self.上一轮温度 + 温度变化量

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '上一轮温度': self.上一轮温度,
            '本轮导热油温度': self.本轮导热油温度()
        }
        基本公式.表格输出(参数集合)
        return 参数集合


class 储冷罐(object):
    def __init__(self, 上一轮温度, 导热油流速, 膨胀机换热器输出的热量):
        self.名字 = '储冷罐'
        self.上一轮温度 = 上一轮温度
        self.导热油流速 = 导热油流速
        self.膨胀机换热器输出的热量 = 膨胀机换热器输出的热量

    def 本轮导热油温度(self):
        导热油比热 = 基本公式.导热油比热(self.上一轮温度)
        温度变化量 = self.膨胀机换热器输出的热量 / (导热油比热 * self.导热油流速)
        return self.上一轮温度 - 温度变化量

    def 输出并返回总参数(self):
        参数集合 = {
            '名字': self.名字,
            '上一轮温度': self.上一轮温度,
            '本轮导热油温度': self.本轮导热油温度()
        }
        基本公式.表格输出(参数集合)
        return 参数集合


if __name__ == '__main__':
    # c = 空气压缩机(100,10000,0.004,2.31,0.9,1)
    # c = 风电站(容量=100, 发电阈值=0, 上一轮发电量=0, 轮次=1)
    # print(c.发电量())
    c = 大气参数()
    c.输出并返回总参数()
