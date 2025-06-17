from z3 import *
import json
import mitmFactory
import time
import json
from datetime import datetime
import re
from mitmFactory import addfivexor_red, addtwoxor_red, addTheta_red, addSbox_nc, addDoMnew, beta_constraints, \
    determine_exist_one
import cProfile
import pstats


# # 创建一个性能分析对象
# profiler = cProfile.Profile()
# # 开始监控
# profiler.enable()
class Mitm:
    def bitvec_to_int(self, bitvec):
        return If(bitvec == 1, 1, 0)

    def __init__(self, rounds, filepath, z_size=32, obj_value=1, rho_values=None):
        self.rounds = rounds
        self.z_size = z_size
        self.obj_value = obj_value  # 将目标值 obj_value 作为参数传入
        self.solver = Optimize()
        self.variables = mitmFactory.variables
        # 设置线程数
        set_param('parallel.enable', True)
        set_param('parallel.threads.max', 4)
        with open(filepath, 'r') as file:
            self.mitm_solution = json.load(file)
        self.rho = rho_values if rho_values is not None else [
            [0, 36, 3, 41, 18],
            [1, 44, 10, 45, 2],
            [62, 6, 43, 15, 61],
            [28, 55, 25, 21, 56],
            [27, 20, 39, 8, 14]
        ]

        # 颜色定义
        self.WhiteColor = "white"
        self.GrayColor = "lightgray"
        self.BlueColor = "blue"
        self.RedColor = "red"
        self.PurpleColor = "green!60"
        # 初始化模型中使用的变量数组
        self.DA = [
            [
                [
                    [
                        [
                            # BitVec(f"DA_{round}_{x}_{y}_{z}_{v}", 1)
                            mitmFactory.add_variable(BitVec(f"DA_{round}_{x}_{y}_{z}_{v}", 1))
                            for v in range(3)
                        ]
                        for z in range(z_size)
                    ]
                    for y in range(5)
                ]
                for x in range(5)
            ]
            for round in range(rounds + 1)
        ]

        self.DP = [
            [
                [
                    [
                        # BitVec(f"DP_{round}_{x}_{z}_{v}", 1)
                        mitmFactory.add_variable(BitVec(f"DP_{round}_{x}_{z}_{v}", 1))

                        for v in range(3)
                    ]
                    for z in range(z_size)
                ]
                for x in range(5)
            ]
            for round in range(rounds)
        ]

        self.DP2 = [
            [
                [
                    [
                        # BitVec(f"DP2_{round}_{x}_{z}_{v}", 1)
                        mitmFactory.add_variable(BitVec(f"DP2_{round}_{x}_{z}_{v}", 1))
                        for v in range(3)
                    ]
                    for z in range(z_size)
                ]
                for x in range(5)
            ]
            for round in range(rounds)
        ]

        self.DC1 = [
            [
                [
                    # BitVec(f"DC1_{round}_{x}_{z}", 1)
                    mitmFactory.add_variable(BitVec(f"DC1_{round}_{x}_{z}", 1))

                    for z in range(z_size)
                ]
                for x in range(5)
            ]
            for round in range(rounds)
        ]

        self.DC12 = [
            [
                [
                    # BitVec(f"DC12_{round}_{x}_{z}", 1)
                    mitmFactory.add_variable(BitVec(f"DC12_{round}_{x}_{z}", 1))
                    for z in range(z_size)
                ]
                for x in range(5)
            ]
            for round in range(rounds)
        ]

        self.DB = [
            [
                [
                    [
                        [
                            # BitVec(f"DB_{round}_{x}_{y}_{z}_{v}", 1)
                            mitmFactory.add_variable(BitVec(f"DB_{round}_{x}_{y}_{z}_{v}", 1))
                            for v in range(3)
                        ]
                        for z in range(z_size)
                    ]
                    for y in range(5)
                ]
                for x in range(5)
            ]
            for round in range(rounds)
        ]

        self.DC2 = [
            [
                [
                    [
                        # BitVec(f"DC2_{round}_{x}_{y}_{z}", 1)
                        mitmFactory.add_variable(BitVec(f"DC2_{round}_{x}_{y}_{z}", 1))
                        for z in range(z_size)
                    ]
                    for y in range(5)
                ]
                for x in range(5)
            ]
            for round in range(rounds)
        ]

        self.dom = [
            [
                # BitVec(f"dom_{i}_{k}", 1)
                mitmFactory.add_variable(BitVec(f"dom_{i}_{k}", 1))
                for k in range(z_size)
            ]
            for i in range(2)
        ]
        # Fixed input
        indices_to_set = [
            (0, 0),
            (1, 3),
            (0, 4),
            (1, 2),
            (1, 0),
            (0, 2),
            (0, 1),
            (1, 4)
        ]
        t1 = [1.0, -1.0, 1.0, -1.0]
        for x in range(5):
            for y in range(5):
                for z in range(z_size):
                    self.solver.add(self.DA[0][x][y][z][1] == 1)
                    for v in range(3):
                        if (v != 1):
                            self.solver.add(
                                self.DA[0][0][0][z][v] == self.DA[0][1][3][(z + self.rho[0][1]) % z_size][v])
                            self.solver.add(self.DA[0][1][0][(z + self.rho[1][1]) % z_size][v] ==
                                            self.DA[0][0][2][(z + self.rho[1][0]) % z_size][v])
                            # self.solver.add(self.DA[0][0][0][z][v] == self.DA[0][1][0][(z + 44) % 64][v])
                            self.solver.add(self.DA[0][0][4][(z + self.rho[2][0]) % z_size][v] ==
                                            self.DA[0][1][2][(z + self.rho[2][1]) % z_size][v])
                            self.solver.add(self.DA[0][0][1][(z + self.rho[3][0]) % z_size][v] ==
                                            self.DA[0][1][4][(z + self.rho[3][1]) % z_size][v])
                            # self.solver.add(self.DA[0][0][4][(z + 62) % 64][v] == self.DA[0][0][1][(z + 28) % 64][v])
                        if (x, y) in indices_to_set:
                            self.solver.add(Or(self.DA[0][x][y][z][0] == 1, self.DA[0][x][y][z][2] == 1))
                        elif (x == 4 and y == 0):
                            term1 = If(self.DA[0][0][0][z][0] == 1, 1, 0)
                            term2 = If(self.DA[0][1][0][z][0] == 1, 1, 0)
                            term3 = If(self.DA[0][1][0][z][2] == 1, 1, 0)
                            term4 = If(self.DA[0][0][0][z][2] == 1, 1, 0)
                            expr = t1[0] * term1 + t1[1] * term2 + t1[2] * term3 + t1[3] * term4
                            self.solver.add(expr <= 1)
                            self.solver.add(expr >= -1)
                            determine_exist_one(self.solver, self.DA[0][x][y][z][0], self.DA[0][0][0][z][0],
                                                self.DA[0][1][0][z][0])
                            determine_exist_one(self.solver, self.DA[0][x][y][z][2], self.DA[0][0][0][z][2],
                                                self.DA[0][1][0][z][2])
                        elif (x == 4 and y == 2):
                            term1 = If(self.DA[0][0][2][z][0] == 1, 1, 0)
                            term2 = If(self.DA[0][1][2][z][0] == 1, 1, 0)
                            term3 = If(self.DA[0][1][2][z][2] == 1, 1, 0)
                            term4 = If(self.DA[0][0][2][z][2] == 1, 1, 0)

                            # 使用 t1 向量进行线性计算
                            expr = t1[0] * term1 + t1[1] * term2 + t1[2] * term3 + t1[3] * term4
                            self.solver.add(expr <= 1)
                            self.solver.add(expr >= -1)

                            # 添加 Determine_ExistOne 约束
                            determine_exist_one(self.solver, self.DA[0][x][y][z][0], self.DA[0][0][2][z][0],
                                                self.DA[0][1][2][z][0])
                            determine_exist_one(self.solver, self.DA[0][x][y][z][2], self.DA[0][0][2][z][2],
                                                self.DA[0][1][2][z][2])

                        # x == 4 且 y == 4 的条件下
                        elif x == 4 and y == 4:
                            term1 = If(self.DA[0][0][4][z][0] == 1, 1, 0)
                            term2 = If(self.DA[0][1][4][z][0] == 1, 1, 0)
                            term3 = If(self.DA[0][1][4][z][2] == 1, 1, 0)
                            term4 = If(self.DA[0][0][4][z][2] == 1, 1, 0)

                            # 使用 t1 向量进行线性计算
                            expr = t1[0] * term1 + t1[1] * term2 + t1[2] * term3 + t1[3] * term4
                            self.solver.add(expr <= 1)
                            self.solver.add(expr >= -1)

                            # 添加 Determine_ExistOne 约束
                            determine_exist_one(self.solver, self.DA[0][x][y][z][0], self.DA[0][0][4][z][0],
                                                self.DA[0][1][4][z][0])
                            determine_exist_one(self.solver, self.DA[0][x][y][z][2], self.DA[0][0][4][z][2],
                                                self.DA[0][1][4][z][2])

                        # 其他条件下的默认约束
                        else:
                            self.solver.add(self.DA[0][x][y][z][0] == 1)
                            self.solver.add(self.DA[0][x][y][z][2] == 1)

                            # # 在DA^1上加条件
        # DA_init = [
        #   [[[0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]],
        # [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
        # [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
        # [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
        # [[0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]]],
        # [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [[0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1]], [[0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]]]

        # for i in range(2):
        #     for j in range(5):
        #         for k in range(64):
        #             for l in range(3):
        #                 self.solver.add(self.DA[0][i][j][k][l] == DA_init[i][j][k][l])
        # #在DP2上添加条件
        # # 存储所有的约束条件
        # constraints = []
        # # 读取文件并解析值
        # with open('MITM-Preimage-Attack-main/Keccak-mitm-search/output.sol', 'r', encoding='utf-8') as file:
        #     for line in file:
        #         # match = re.match(r'(\w+)_(\d+)_(\d+)_(\d+)_(\d+) = (\d+)', line.strip())
        #         match = re.match(r'(\w+)_(\d+)_(\d+)_(\d+)_(\d+) (\d+)', line.strip())
        #         if match:
        #             var_name, round, x, z, v, value = match.groups()
        #             round, x, z, v, value = int(round), int(x), int(z), int(v), int(value)

        #             if var_name == 'DP2' and round < rounds and x < 5 and z < 64 and v < 3:
        #                 constraints.append(self.DP2[round][x][z][v] == BitVecVal(value, 1))
        # constraints.append(self.DP2[0][0][0][0] == BitVecVal(1,1))
        # 根据 var_name 处理其他变量，如 DA, DB 等
        # if var_name == 'DA':
        #     constraints.append(DA[round][x][z][v] == BitVecVal(value, 1))
        # if var_name == 'DB':
        #     constraints.append(DB[round][x][z][v] == BitVecVal(value, 1))
        # 打印所有约束条件
        # print("Constraints:")
        # for c in constraints:
        #     print(c)
        # 将所有约束条件一次性添加到 solver
        # self.solver.add(constraints)
        print("Constraints after Fixed input:", len(self.solver.assertions()))

        addfivexor_red(self.solver, self.DA, self.DP, self.DC1, self.z_size)
        print("Constraints after addtwoxor_red:", len(self.solver.assertions()))
        addtwoxor_red(self.solver, self.DP2, self.DP, self.DC12, self.z_size)
        print("Constraints after addtwoxor_red:", len(self.solver.assertions()))

        addTheta_red(self.solver, self.DA, self.DP2, self.DB, self.DC2, self.z_size, self.rho)
        print("Constraints after addTheta_red:", len(self.solver.assertions()))

        addSbox_nc(self.solver, self.DB, self.DA, self.z_size)
        print("Constraints after addSbox_nc:", len(self.solver.assertions()))

        addDoMnew(self.solver, self.DA, self.dom, self.z_size, self.rho)
        print("Constraints after addDoMnew:", len(self.solver.assertions()))

        self.beta = [[mitmFactory.add_variable(BitVec(f'beta_{x}_{z}', 1)) for z in range(z_size)] for x in range(4)]
        beta_constraints(self.solver, self.DA, self.beta, self.z_size)
        print("Constraints after beta_constraints:", len(self.solver.assertions()))

        self.Obj = mitmFactory.add_variable(Int('Obj'))
        obj1 = mitmFactory.add_variable(Int('Obj1'))
        obj2 = mitmFactory.add_variable(Int('Obj2'))
        obj3 = mitmFactory.add_variable(Int('Obj3'))
        # 将这些变量存储在 self.obj 列表中
        self.obj = [obj1, obj2, obj3]
        self.DoF_red = mitmFactory.add_variable(Int('DoF_red'))
        self.DoF_blue = mitmFactory.add_variable(Int('DoF_blue'))
        self.DoM = mitmFactory.add_variable(Int('DoM'))
        # If(condition, then, else) BitVec转为Int
        self.DoM_expr = Sum([If(self.dom[x][z] == 1, 1, 0) for x in range(2) for z in range(z_size)])

        self.DoF_red_expr = Sum([If(self.DA[0][0][0][z][2] == 1, 1, 0) -
                                 If(self.beta[0][z] == 1, 1, 0) +
                                 If(self.DA[0][0][1][z][2] == 1, 1, 0) -
                                 If(self.beta[1][z] == 1, 1, 0) +
                                 If(self.DA[0][0][2][z][2] == 1, 1, 0) -
                                 If(self.beta[2][z] == 1, 1, 0) +
                                 If(self.DA[0][0][4][z][2] == 1, 1, 0) -
                                 If(self.beta[3][z] == 1, 1, 0) for z in range(z_size)])
        self.DoF_blue_expr = Sum([If(self.DA[0][0][0][z][0] == 1, 1, 0) -
                                  If(self.beta[0][z] == 1, 1, 0) +
                                  If(self.DA[0][0][1][z][0] == 1, 1, 0) -
                                  If(self.beta[1][z] == 1, 1, 0) +
                                  If(self.DA[0][0][2][z][0] == 1, 1, 0) -
                                  If(self.beta[2][z] == 1, 1, 0) +
                                  If(self.DA[0][0][4][z][0] == 1, 1, 0) -
                                  If(self.beta[3][z] == 1, 1, 0) for z in range(z_size)])
        for round in range(rounds):
            for x in range(5):
                for z in range(z_size):
                    self.DoF_red_expr -= If(self.DC1[round][x][z] == 1, 1, 0)
                    self.DoF_red_expr -= If(self.DC12[round][x][z] == 1, 1, 0)
                    for y in range(5):
                        self.DoF_red_expr -= If(self.DC2[round][x][y][z] == 1, 1, 0)
        # 添加约束
        print("Adding constraints:")
        self.solver.add(self.DoF_red == self.DoF_red_expr)
        self.solver.add(self.DoF_blue == self.DoF_blue_expr)
        self.solver.add(self.DoM == self.DoM_expr)
        self.solver.add(self.DoF_red >= 1)
        self.solver.add(self.DoF_blue >= 1)
        self.solver.add(self.DoM >= 1)
        self.solver.add(self.DoF_red == self.obj[0])
        self.solver.add(self.DoF_blue == self.obj[1])
        self.solver.add(self.DoM == self.obj[2])

        # 目标函数

        self.solver.add(self.Obj <= self.DoF_blue)
        self.solver.add(self.Obj <= self.DoF_red)
        self.solver.add(self.Obj <= self.DoM)
        self.solver.add(self.Obj == self.obj_value)

        # 设置目标
        self.solver.maximize(self.Obj)
        print("Constraints after all:", len(self.solver.assertions()))
        print("Objective set to maximize:", self.Obj)

    def generate_smt2_file(self):
        smt2_content = self.solver.sexpr()
        with open("solver_constraints.smt2", "w") as f:
            f.write(smt2_content)

    def solve(self):
        start_time = datetime.now()
        print("Start time2: {}".format(start_time.strftime("%m-%d-%H:%M:%S")))
        result = self.solver.check()
        if result == sat:
            m = self.solver.model()
            solution = {
                "Rounds": self.rounds,
                "objective": m[self.Obj].as_long(),
                "DA": [[[
                    [[m[self.DA[round][x][y][z][v]].as_long() for v in range(3)] for z in range(self.z_size)]
                    for y in range(5)]
                    for x in range(5)]
                    for round in range(self.rounds + 1)],
                "DP": [[[
                    [m[self.DP[round][x][z][v]].as_long() for v in range(3)] for z in range(self.z_size)]
                    for x in range(5)]
                    for round in range(self.rounds)],
                "DP2": [[[
                    [m[self.DP2[round][x][z][v]].as_long() for v in range(3)] for z in range(self.z_size)]
                    for x in range(5)]
                    for round in range(self.rounds)],
                "DC1": [[[
                    m[self.DC1[round][x][z]].as_long() for z in range(self.z_size)]
                    for x in range(5)]
                    for round in range(self.rounds)],
                "DC12": [[[
                    m[self.DC12[round][x][z]].as_long() for z in range(self.z_size)]
                    for x in range(5)]
                    for round in range(self.rounds)],
                "DB": [[[
                    [[m[self.DB[round][x][y][z][v]].as_long() for v in range(3)] for z in range(self.z_size)]
                    for y in range(5)]
                    for x in range(5)]
                    for round in range(self.rounds)],
                "DC2": [[[[
                    m[self.DC2[round][x][y][z]].as_long() for z in range(self.z_size)]
                    for y in range(5)]
                    for x in range(5)]
                    for round in range(self.rounds)],
                "dom": [[m[self.dom[x][z]].as_long() for z in range(self.z_size)] for x in range(2)],
                "obj": [m[self.obj[i]].as_long() for i in range(3)],

            }
            print("DoM:", m[self.DoM].as_long())
            print("DoF_red:", m[self.DoF_red].as_long())
            print("DoF_blue:", m[self.DoF_blue].as_long())
        #     with open('mitm_solution.json', 'w') as file:
        #         json.dump(solution, file, indent=4)
        #         file.flush()  # 强制写入缓存
        # else:
        #     print("No solution found")
        # print(self.solver.statistics())
            solution_file = os.path.join(os.path.dirname(__file__),
                                         f'mitm_solution_{start_time.strftime("%Y%m%d_%H%M%S")}.json')
            with open(solution_file, 'w') as file:
                json.dump(solution, file, indent=4)
                file.flush()  # 强制写入缓存
            print(f"Solution saved to {solution_file}")
            # 重新加载文件，确保最新数据可用
            with open(solution_file, 'r') as file:
                self.mitm_solution = json.load(file)
            print("Reloaded solution data successfully.")
        else:
            print("No solution found")
        print(self.solver.statistics())

    def generate(self):
        print("进入generate函数")
        output = ""
        output += "\\documentclass{standalone}\n"
        output += "\\usepackage{tikz}\n"
        output += "\\usepackage{calc}\n"
        output += "\\usepackage{pgffor}\n"
        output += "\\usetikzlibrary{patterns}\n"
        output += "\\tikzset{base/.style = {draw=black, minimum width=0.02cm, minimum height=0.02cm, align=center, on chain},}\n"
        output += "\\begin{document}\n"
        output += "\\begin{tikzpicture}[scale = 0.45,every node/.style={scale=0.5}]\n"
        output += "\\makeatletter\n"

        rounds = self.mitm_solution["Rounds"]
        for round in range(rounds + 1):
            print(f"Starting Round {round + 1}")  # 打印当前轮次
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 20.5}) [scale=1.5]{{\\textbf{{\\huge $A^{{({round + 1})}}$}}}};\n"
            for k in range(self.z_size):
                for i in range(5):
                    for j in range(5):
                        da_values = self.mitm_solution["DA"][round][i][j][k]
                        if da_values == [0, 0, 0]:
                            color = self.WhiteColor
                        elif da_values == [0, 1, 1]:
                            color = self.RedColor
                        elif da_values == [1, 1, 0]:
                            color = self.BlueColor
                        elif da_values == [0, 1, 0]:
                            color = self.PurpleColor
                        elif da_values == [1, 1, 1]:
                            color = self.GrayColor
                        output += f"\\fill[color={color}] ({6 * k + i},{25 * (rounds - round) + (4 - j) + 18}) rectangle ++(1,1);\n"
                output += f"\\draw({6 * k},{25 * (rounds - round) + 18}) grid ++(5,5);\n"
                output += f" \\node[align=center] at ({6 * k + 2},{25 * (rounds - round) + 17})[scale=2] {{\\Large z={k}}};\n"

            if round != rounds:
                # DP
                print(f"Drawing C for Round {round + 1}")
                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 15.5}) [scale=1.5]{{\\textbf{{\\huge $C^{{({round + 1})}}$}}}};\n"
                consumered = 0
                for k in range(self.z_size):
                    for i in range(5):
                        dp_values = self.mitm_solution["DP"][round][i][k]
                        if dp_values == [0, 0, 0]:
                            color = self.WhiteColor
                        elif dp_values == [0, 1, 1]:
                            color = self.RedColor
                        elif dp_values == [1, 1, 0]:
                            color = self.BlueColor
                        elif dp_values == [0, 1, 0]:
                            color = self.PurpleColor
                        elif dp_values == [1, 1, 1]:
                            color = self.GrayColor
                        output += f"\\fill[color={color}] ({6 * k + i},{25 * (rounds - round) + 15}) rectangle ++(1,1);\n"
                    output += f"\\draw({6 * k},{25 * (rounds - round) + 15}) grid ++(5,1);\n"
                    for i in range(5):
                        if self.mitm_solution["DC1"][round][i][k] == 1:
                            consumered += 1
                            output += f"\\draw[line width=2pt, color=yellow] ({6 * k + i},{25 * (rounds - round) + 15}) grid ++(1,1);\n"

                output += f"\\fill[color={self.RedColor}] ({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 15})  rectangle ++(1,1);\n"
                output += f"\\draw({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                output += f"\\node[align=center] at ({6 * (self.z_size - 1) + 4 + 2.5},{25 * (rounds - round) + 15.4}) {{\\textbf{{\\huge - {consumered}}}}};\n"

                # DP2
                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 13.5})[scale=1.5]{{\\textbf{{\\huge $D^{{({round + 1})}}$}}}};\n"
                print(f"Drawing D for Round {round + 1}")
                consumered = 0
                for k in range(self.z_size):
                    for i in range(5):
                        dp2_values = self.mitm_solution["DP2"][round][i][k]
                        if dp2_values == [0, 0, 0]:
                            color = self.WhiteColor
                        elif dp2_values == [0, 1, 1]:
                            color = self.RedColor
                        elif dp2_values == [1, 1, 0]:
                            color = self.BlueColor
                        elif dp2_values == [0, 1, 0]:
                            color = self.PurpleColor
                        elif dp2_values == [1, 1, 1]:
                            color = self.GrayColor
                        output += f"\\fill[color={color}] ({6 * k + i},{25 * (rounds - round) + 13}) rectangle ++(1,1);\n"
                    output += f"\\draw({6 * k},{25 * (rounds - round) + 13}) grid ++(5,1);\n"
                    for i in range(5):
                        if self.mitm_solution["DC12"][round][i][k] == 1:
                            consumered += 1
                            output += f"\\draw[line width=2pt, color=yellow] ({6 * k + i},{25 * (rounds - round) + 13}) grid ++(1,1);\n"
                output += f"\\fill[color={self.RedColor}] ({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 13})  rectangle ++(1,1);\n"
                output += f"\\draw({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 13})  grid ++(1,1);\n"
                output += f" \\node[align=center] at ({6 * (self.z_size - 1) + 4 + 2.5},{25 * (rounds - round) + 13.4}) {{\\textbf{{\\huge - {consumered}}}}};\n"

                # DB after theta

                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 9.5})[scale=1.5]{{\\textbf{{\\huge $\\theta^{{({round + 1})}}$}}}};\n"
                print(f"Drawing theta for Round {round + 1}")
                for k in range(self.z_size):
                    for i in range(5):
                        for j in range(5):
                            db_values = self.mitm_solution["DB"][round][i][j][k]
                            if db_values == [0, 0, 0]:
                                color = self.WhiteColor
                            elif db_values == [0, 1, 1]:
                                color = self.RedColor
                            elif db_values == [1, 1, 0]:
                                color = self.BlueColor
                            elif db_values == [0, 1, 0]:
                                color = self.PurpleColor
                            elif db_values == [1, 1, 1]:
                                color = self.GrayColor
                            output += f"\\fill[color={color}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + self.z_size) % self.z_size) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 7}) rectangle ++(1,1);\n"
                for k in range(self.z_size):
                    output += f"\\draw({6 * k},{25 * (rounds - round) + 7}) grid ++(5,5);\n"

                consumered = 0
                for k in range(self.z_size):
                    for i in range(5):
                        for j in range(5):
                            if self.mitm_solution["DC2"][round][i][j][k] == 1:
                                consumered += 1
                                output += f"\\draw[line width=2pt, color=yellow] ({6 * k + i},{25 * (rounds - round) + (4 - j) + 7}) grid ++(1,1);\n"
                output += f"\\fill[color={self.RedColor}] ({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 9})  rectangle ++(1,1);\n"
                output += f"\\draw({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 9})  grid ++(1,1);\n"
                output += f" \\node[align=center] at ({6 * (self.z_size - 1) + 4 + 2.5},{25 * (rounds - round) + 9.4}) {{\\textbf{{\\huge - {consumered}}}}};\n"

                # DB
                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 2.5})[scale=1.5]{{\\textbf{{\\huge $\\pi^{{({round + 1})}}$}}}};\n"
                print(f"Drawing pai for Round {round + 1}")
                for k in range(self.z_size):
                    for i in range(5):
                        for j in range(5):
                            db_values = self.mitm_solution["DB"][round][i][j][k]
                            if db_values == [0, 0, 0]:
                                color = self.WhiteColor
                            elif db_values == [0, 1, 1]:
                                color = self.RedColor
                            elif db_values == [1, 1, 0]:
                                color = self.BlueColor
                            elif db_values == [0, 1, 0]:
                                color = self.PurpleColor
                            elif db_values == [1, 1, 1]:
                                color = self.GrayColor
                            output += f"\\fill[color={color}] ({6 * k + i},{25 * (rounds - round) + (4 - j)}) rectangle ++(1,1);\n"
                    output += f"\\draw({6 * k},{25 * (rounds - round)}) grid ++(5,5);\n"
            # 添加新的节点
            for k in range(self.z_size):
                if self.mitm_solution["dom"][0][k] == 1:
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[3][0] + self.z_size) % self.z_size) + 3 + 0.5},{18 + 4 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[3][0] + self.z_size) % self.z_size) + 3 + 0.5},{18 + 1 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[0][2] + self.z_size) % self.z_size) + 0 + 0.5},{18 + 2 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[0][2] + self.z_size) % self.z_size) + 0 + 0.5},{18 + 4 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                if self.mitm_solution["dom"][1][k] == 1:
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[4][1] + self.z_size) % self.z_size) + 4 + 0.5},{18 + 3 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[4][1] + self.z_size) % self.z_size) + 4 + 0.5},{18 + 0 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[1][3] + self.z_size) % self.z_size) + 1 + 0.5},{18 + 1 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[1][3] + self.z_size) % self.z_size) + 1 + 0.5},{18 + 3 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
            output += "\n"
            # 处理 round == -1 的情况
        round = -1
        if round == -1:
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 20.5}) [scale=1.5]{{\\textbf{{\\huge $A^{{({round + 1})}}$}}}};\n"
            for k in range(self.z_size):
                for i in range(5):
                    for j in range(5):
                        if (i == 0 or i == 1):
                            da_values = self.mitm_solution["DA"][round + 1][i][j][k]
                            if da_values == [0, 0, 0]:
                                color = self.WhiteColor
                            elif da_values == [0, 1, 1]:
                                color = self.RedColor
                            elif da_values == [1, 1, 0]:
                                color = self.BlueColor
                            elif da_values == [0, 1, 0]:
                                color = self.PurpleColor
                            elif da_values == [1, 1, 1]:
                                color = self.GrayColor
                            output += f"\\fill[color={color}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + self.z_size) % self.z_size) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 18}) rectangle ++(1,1);\n"
                        else:
                            output += f"\\fill[color={self.GrayColor}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + self.z_size) % self.z_size) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 18}) rectangle ++(1,1);\n"
            for k in range(self.z_size):
                output += f"\\draw({6 * k},{25 * (rounds - round) + 18}) grid ++(5,5);\n"
                output += f" \\node[align=center] at ({6 * k + 2},{25 * (rounds - round) + 17})[scale=2] {{\\Large z={k}}};\n"

            allred = 0
            allblue = 0
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 15.5})[scale=1.5]{{\\textbf{{\\huge $C^{{({round + 1})}}$}}}};\n"
            for k in range(self.z_size):
                for i in range(5):
                    output += f"\\fill[color={self.GrayColor}] ({6 * k + i},{25 * (rounds - round) + 15}) rectangle ++(1,1);\n"
                output += f"\\draw({6 * k},{25 * (rounds - round) + 15}) grid ++(5,1);\n"
            for k in range(self.z_size):
                if self.mitm_solution["DA"][round + 1][0][0][k] == [0, 1, 1]:
                    allred += 1
                    output += f"\\draw[line width=2pt, color=yellow]({6 * k},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                if self.mitm_solution["DA"][round + 1][0][0][k] == [1, 1, 0]:
                    allblue += 1
                    output += f"\\draw[line width=2pt, color=black]({6 * k},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                if self.mitm_solution["DA"][round + 1][1][0][k] == [0, 1, 1]:
                    allred += 1
                    output += "\\draw[line width=2pt, color=yellow](" + str(
                        6 * ((k - self.rho[1][1] + self.z_size) % self.z_size) + 1) + "," + str(
                        25 * (rounds - round) + 15) + ") grid ++(1,1);\n"
                if self.mitm_solution["DA"][round + 1][1][0][k] == [1, 1, 0]:
                    allblue += 1
                    output += "\\draw[line width=2pt, color=black](" + str(
                        6 * ((k - self.rho[1][1] + self.z_size) % self.z_size) + 1) + "," + str(
                        25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][1][2][k] == [0, 1, 1]:
                    allred += 1
                    output += "\\draw[line width=2pt, color=yellow](" + str(
                        6 * ((k - self.rho[2][1] + self.z_size) % self.z_size) + 2) + "," + str(
                        25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][1][2][k] == [1, 1, 0]:
                    allblue += 1
                    output += "\\draw[line width=2pt, color=black](" + str(
                        6 * ((k - self.rho[2][1] + self.z_size) % self.z_size) + 2) + "," + str(
                        25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][0][1][k] == [0, 1, 1]:
                    allred += 1
                    output += "\\draw[line width=2pt, color=yellow](" + str(
                        6 * ((k - self.rho[3][0] + self.z_size) % self.z_size) + 3) + "," + str(
                        25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][0][1][k] == [1, 1, 0]:
                    allblue += 1
                    output += "\\draw[line width=2pt, color=black](" + str(
                        6 * ((k - self.rho[3][0] + self.z_size) % self.z_size) + 3) + "," + str(
                        25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

            output += f"\\fill[color={self.RedColor}] ({6 * (self.z_size - 1) + 4 + 2},{25 * (rounds - round) + 21})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * (self.z_size - 1) + 4 + 2},{25 * (rounds - round) + 21})  grid ++(1,1);\n"

            output += f" \\node[align=center] at ({6 * (self.z_size - 1) + 4 + 4.2},{25 * (rounds - round) + 21.4}){{\\textbf{{\\huge = {allred * 2}}}}};\n"
            output += f"\\fill[color={self.BlueColor}] ({6 * (self.z_size - 1) + 4 + 2},{25 * (rounds - round) + 19})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * (self.z_size - 1) + 4 + 2},{25 * (rounds - round) + 19}) grid ++(1,1);\n"
            output += f" \\node[align=center] at ({6 * (self.z_size - 1) + 4 + 4.1},{25 * (rounds - round) + 19.4}){{\\textbf{{\\huge = {allblue * 2}}}}};\n"

            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 13.5}) [scale=1.5]{{\\textbf{{\\huge $D^{{({round + 1})}}$}}}};\n"
            for k in range(self.z_size):
                for i in range(5):
                    output += f"\\fill[color={self.GrayColor}] ({6 * k + i},{25 * (rounds - round) + 13}) rectangle ++(1,1);\n"
                output += f"\\draw({6 * k},{25 * (rounds - round) + 13}) grid ++(5,1);\n"
            output += f"\\fill[color={self.RedColor}] ({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 16})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 16})  grid ++(1,1);\n"
            output += f" \\node[align=center] at ({6 * (self.z_size - 1) + 4 + 2.5},{25 * (rounds - round) + 16.4}){{\\textbf{{\\huge - {allred}}}}};\n"
            output += f"\\fill[color={self.BlueColor}] ({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 14.5})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * (self.z_size - 1) + 4 + 4},{25 * (rounds - round) + 14.5}) grid ++(1,1);\n"
            output += f" \\node[align=center] at ({6 * (self.z_size - 1) + 4 + 2.7},{25 * (rounds - round) + 14.9}){{\\textbf{{\\huge - {allblue}}}}};\n"

            # DB after theta
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 9.5})[scale=1.5]{{\\huge $\\theta^{{({round + 1})}}$}};\n"
            for k in range(self.z_size):
                for i in range(5):
                    for j in range(5):
                        if (i == 0 or i == 1):
                            da_values = self.mitm_solution["DA"][round + 1][i][j][k]
                            if da_values == [0, 0, 0]:
                                color = self.WhiteColor
                            elif da_values == [0, 1, 1]:
                                color = self.RedColor
                            elif da_values == [1, 1, 0]:
                                color = self.BlueColor
                            elif da_values == [0, 1, 0]:
                                color = self.PurpleColor
                            elif da_values == [1, 1, 1]:
                                color = self.GrayColor
                            output += f"\\fill[color={color}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + self.z_size) % self.z_size) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 7}) rectangle ++(1,1);\n"
                        else:
                            output += f"\\fill[color={self.GrayColor}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + self.z_size) % self.z_size) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 7}) rectangle ++(1,1);\n"
                if (i == 0 and j == 0):
                    if (self.DA[round + 1][0][0][k][0] == 0 and self.DA[round + 1][0][0][k][1] == 1 and
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";
                    if (self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and
                            self.DA[round + 1][0][0][k][2] == 0 and self.DA[round + 1][1][0][k][0] == 1 and
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 0):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";
                    if (self.DA[round + 1][0][0][k][0] == 0 and self.DA[round + 1][0][0][k][1] == 1 and
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 1 and
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";
                    if (self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";
                    if (self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and
                            self.DA[round + 1][0][0][k][2] == 0 and self.DA[round + 1][1][0][k][0] == 1 and
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";
                    if (self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 0):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";
                if i == 0 and j == 1:
                    if self.DA[round + 1][0][1][k][0] == 0 and self.DA[round + 1][0][1][k][1] == 1 and \
                            self.DA[round + 1][0][1][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][1][k][0] == 1 and self.DA[round + 1][0][1][k][1] == 1 and \
                            self.DA[round + 1][0][1][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                if i == 0 and j == 2:
                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                    if i == 0 and j == 3:
                        if self.DA[round + 1][1][3][k][0] == 0 and self.DA[round + 1][1][3][k][1] == 1 and \
                                self.DA[round + 1][1][3][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][1][3][k][0] == 1 and self.DA[round + 1][1][3][k][1] == 1 and \
                                self.DA[round + 1][1][3][k][2] == 0:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if i == 0 and j == 4:
                        if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and \
                                self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and \
                                self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and \
                                self.DA[round + 1][0][4][k][2] == 0 and self.DA[round + 1][1][4][k][0] == 1 and \
                                self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 0:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and \
                                self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 1 and \
                                self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and \
                                self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and \
                                self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and \
                                self.DA[round + 1][0][4][k][2] == 0 and self.DA[round + 1][1][4][k][0] == 1 and \
                                self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + self.z_size) % self.z_size) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + self.z_size) % self.z_size) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and \
                                self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 1 and \
                                self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 0:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + self.z_size) % self.z_size) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + self.z_size) % self.z_size) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                # for i in range(5):
                #     for j in range(5):
                #         if self.mitm_solution["DA"][round + 1][i][j][k] == [0, 1, 1]:
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n"
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n"
                #         if self.mitm_solution["DA"][round + 1][i][j][k] == [1, 1, 0]:
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n"
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n"
            for k in range(self.z_size):
                output += f"\\draw({6 * k},{25 * (rounds - round) + 7}) grid ++(5,5);\n"

            # DB
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 2.5}) [scale=1.5]{{\\textbf{{\\huge $\\pi^{{({round + 1})}}$}}}};\n"
            for k in range(self.z_size):
                for i in range(5):
                    for j in range(5):
                        if i == 0 or i == 1:
                            da_values = self.mitm_solution["DA"][round + 1][i][j][k]
                            if da_values == [0, 0, 0]:
                                color = self.WhiteColor
                            elif da_values == [0, 1, 1]:
                                color = self.RedColor
                            elif da_values == [1, 1, 0]:
                                color = self.BlueColor
                            elif da_values == [0, 1, 0]:
                                color = self.PurpleColor
                            elif da_values == [1, 1, 1]:
                                color = self.GrayColor
                            output += f"\\fill[color={color}] ({6 * k + i},{25 * (rounds - round) + (4 - j)}) rectangle ++(1,1);\n"
                        else:
                            output += f"\\fill[color={self.GrayColor}] ({6 * k + i},{25 * (rounds - round) + (4 - j)}) rectangle ++(1,1);\n"

                output += f"\\draw({6 * k},{25 * (rounds - round)}) grid ++(5,5);\n"
                if i == 0 and j == 0:
                    if self.DA[round + 1][0][0][k][0] == 0 and self.DA[round + 1][0][0][k][1] == 1 and \
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and \
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and \
                            self.DA[round + 1][0][0][k][2] == 0 and self.DA[round + 1][1][0][k][0] == 1 and \
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 0 and self.DA[round + 1][0][0][k][1] == 1 and \
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 1 and \
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and \
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and \
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and \
                            self.DA[round + 1][0][0][k][2] == 0 and self.DA[round + 1][1][0][k][0] == 1 and \
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and \
                            self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 1 and \
                            self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                if i == 0 and j == 1:
                    if self.DA[round + 1][0][1][k][0] == 0 and self.DA[round + 1][0][1][k][1] == 1 and \
                            self.DA[round + 1][0][1][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][1][k][0] == 1 and self.DA[round + 1][0][1][k][1] == 1 and \
                            self.DA[round + 1][0][1][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                if i == 0 and j == 2:
                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += "\\node[align=center] at (" + str(6 * k + (i + 1) % 5 + 0.5) + "," + str(
                            25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 0}};\n"
                        output += "\\node[align=center] at (" + str(6 * k + (i + 4) % 5 + 0.5) + "," + str(
                            25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 1}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and \
                            self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and \
                            self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        output += "\\node[align=center] at (" + str(6 * k + i % 5 + 0.5) + "," + str(
                            25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 1}};\n"
                        output += "\\node[align=center] at (" + str(6 * k + (i + 2) % 5 + 0.5) + "," + str(
                            25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 0}};\n"
                if i == 0 and j == 3:
                    if self.DA[round + 1][1][3][k][0] == 0 and self.DA[round + 1][1][3][k][1] == 1 and \
                            self.DA[round + 1][1][3][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                    if self.DA[round + 1][1][3][k][0] == 1 and self.DA[round + 1][1][3][k][1] == 1 and \
                            self.DA[round + 1][1][3][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                    i = 0;
                    j = 4
                    if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and \
                            self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and \
                            self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and \
                            self.DA[round + 1][0][4][k][2] == 0 and self.DA[round + 1][1][4][k][0] == 1 and \
                            self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and \
                            self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 1 and \
                            self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and \
                            self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and \
                            self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                # for i in range(5):
                #     for j in range(5):
                #         if self.mitm_solution["DA"][round + 1][i][j][k] == [0, 1, 1]:
                #             output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}){{\\textbf{{\\Large 0}}}};\n"
                #             output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}){{\\textbf{{\\Large 1}}}};\n"
                #         if self.mitm_solution["DA"][round + 1][i][j][k] == [1, 1, 0]:
                #             output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}){{\\textbf{{\\Large 0}}}};\n"
                #             output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}){{\\textbf{{\\Large 1}}}};\n"

        output += "\\makeatother\n"
        output += "\\end{tikzpicture}\n"
        output += "\\end{document}\n"
        return output


# def main():
#     # 路径和文件设置
#     base_dir = os.path.dirname(__file__)
#     filepath = os.path.join(base_dir, "mitm_solution.json")
#     output_dir = os.path.join(base_dir, "pic")
#     os.makedirs(output_dir, exist_ok=True)
#     output_file = os.path.join(output_dir, f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.tex")
#
#     # 配置参数
#     rounds = 2
#     z_size = 32
#     obj_value = 2
#     rho_values = [
#         [0, 36, 3, 41, 18],
#         [1, 44, 10, 45, 2],
#         [62, 6, 43, 15, 61],
#         [28, 55, 25, 21, 56],
#         [27, 20, 39, 8, 14]
#     ]
#
#     # 记录开始时间
#     start_time = datetime.now()
#     print("Start time: {}".format(start_time.strftime("%m-%d-%H:%M:%S")))
#
#     # 初始化 Mitm 实例并执行
#     mitm_instance = Mitm(rounds, filepath, z_size=z_size, obj_value=obj_value, rho_values=rho_values)
#     mitm_instance.generate_smt2_file()
#     mitm_instance.solve()
#
#     # 记录结束时间和执行耗时
#     end_time = datetime.now()
#     print("End time: {}".format(end_time.strftime("%m-%d-%H-%M-%S")))
#     elapsed_time = end_time - start_time
#     print("Elapsed time: {} seconds".format(elapsed_time.total_seconds()))
#
#     # 生成 TikZ 代码并保存
#     tikz_code = mitm_instance.generate()
#     with open(output_file, "w") as file:
#         file.write(tikz_code)
#     print(f"TikZ code has been saved to {output_file}")
#
# if __name__ == "__main__":
#     main()
#

