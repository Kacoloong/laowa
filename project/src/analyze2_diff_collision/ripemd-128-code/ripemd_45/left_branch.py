# -*- coding: utf-8 -*-
# @Time : 2024/07/09 21:32
# @Author: yxli
# @FileName: left_first.py
# @Software: PyCharm
import subprocess

from constrain_condition import *


class FunctionModel:
    def __init__(self, steps, bounds, num):
        self.__num = num
        self.__bounds_rounds = bounds
        self.__step = steps
        self.__declare = []  # 存储变量
        self.__constraints = []  # 存储约束语句
        self.__assign = []  # 存储赋值约束

    def save_variable(self, s):
        """
        本函数是用来存储变量
        :param s:
        :return:
        """
        temp = s + ": BITVECTOR(1);\n"
        if temp not in self.__declare:
            self.__declare.append(temp)
        return s

    def create_constraints(self, X, propagation_trail):
        fun = []
        for maxterm in propagation_trail:
            temp = []
            for i in range(len(maxterm)):
                if maxterm[i] == '1':
                    temp.append('(' + '~' + X[i] + ')')
                elif maxterm[i] == '0':
                    temp.append(X[i])
            fun.append('(' + "|".join(temp) + ')')
        sbox_main = 'ASSERT ' + '&'.join(fun) + '=0bin1' + ';\n'
        return sbox_main

    def right_shift(self, order, num):
        return order[num:] + order[:num]

    def addexp_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, out_var_v, out_var_d, step):
        """
       本函数表示的是搜索策略2中的一个扩展的模加运算，在算法6中的ADDEXP_MODEL;
       :param step: 步数
       :param in_var_v_0:表示delta-X的v
       :param in_var_d_0:表示delta-X的d
       :param in_var_v_1:表示delta-Y的v
       :param in_var_d_1:表示delta-Y的d
       :param out_var_v:表示delta-Z的v
       :param out_var_d:表示delta-Z的d
       :return:
       声明一个delta-C，其大小为33;
       var_c_v 声明一个delta-C的v,用"cv6" + "_" + step + "_" + str(i)表示;
       var_c_d 声明一个delta-C的d,用"cd6" + "_" + step + "_" + str(i)表示;
       """
        eqn = "% ADDEXP_MODEL\n"
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable("cv6" + "_" + str(step) + "_" + str(0)),
                                                             self.save_variable("cd6" + "_" + str(step) + "_" + str(0)))
        for i in range(32):
            temp = [self.save_variable(in_var_v_0[i]), self.save_variable(in_var_d_0[i]),
                    self.save_variable(in_var_v_1[i]), self.save_variable(in_var_d_1[i]),
                    self.save_variable("cv6" + "_" + str(step) + "_" + str(i)),
                    self.save_variable("cd6" + "_" + str(step) + "_" + str(i)),
                    self.save_variable(out_var_v[i]), self.save_variable(out_var_d[i]),
                    self.save_variable("cv6" + "_" + str(step) + "_" + str(i + 1)),
                    self.save_variable("cd6" + "_" + str(step) + "_" + str(i + 1))]
            eqn += self.create_constraints(temp, addexp_model_constrain)
        self.__constraints.append(eqn)

    def boolfast_model(self, fna, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d):

        # print("60:boolfast_model%s" % fna)
        """
        本模型是布尔函数的快速模型，这个模型中不包括其中隐含条件
        :param fna: 表示步数需要去选择合适的布尔函数
        :param in_var_v_0: 表示布尔函数的输入delta-x的v
        :param in_var_d_0: 表示布尔函数的输入delta-x的d
        :param in_var_v_1: 表示布尔函数的输入delta-y的v
        :param in_var_d_1: 表示布尔函数的输入delta-y的d
        :param in_var_v_2: 表示布尔函数的输入delta-z的v
        :param in_var_d_2: 表示布尔函数的输入delta-z的d
        :param out_var_v: 表示布尔函数的输出delta-w的v
        :param out_var_d: 表示布尔函数的输出delta-w的d
        :return:
        """

        if fna == "XOR":
            eqn = "% boolfast_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i])]
                eqn += self.create_constraints(temp, xor_fast_contsrain)
            self.__constraints.append(eqn)

        elif fna == "IFZ":
            eqn = "% boolfast_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i])]
                eqn += self.create_constraints(temp, ifz_fast_contsrain)
            self.__constraints.append(eqn)
        elif fna == "IFX":
            eqn = "% boolfast_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i])]
                eqn += self.create_constraints(temp, ifz_fast_contsrain)
            self.__constraints.append(eqn)

        elif fna == "ONX":
            eqn = "% boolfast_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i])]
                eqn += self.create_constraints(temp, onx_fast_contsrain)
            self.__constraints.append(eqn)

    def boolfull_model(self, fna, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d, in_var_0, in_var_1, in_var_2):
        # print("175:boolfull_model: %s" % fna)
        if fna == "XOR":
            eqn = "% boolfull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i])]
                eqn += self.create_constraints(temp, xor_full_constrain)
            self.__constraints.append(eqn)

        elif fna == "IFZ":
            eqn = "% boolfull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i])]
                eqn += self.create_constraints(temp, ifz_full_constrain)
            self.__constraints.append(eqn)
        elif fna == "IFX":
            eqn = "% boolfull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i]),
                        self.save_variable(in_var_0[i])]
                eqn += self.create_constraints(temp, ifz_full_constrain)
            self.__constraints.append(eqn)

        elif fna == "ONX":
            eqn = "% boolfull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_2[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i])]
                eqn += self.create_constraints(temp, onx_full_constrain)
            self.__constraints.append(eqn)

    def expand_model(self, in_var_v, in_var_d, in_var_c_v, in_var_c_d, out_var_v, out_var_d, isK):
        # print("202:expand_model")
        """
        本模型输出扩展模型，有时候存在输出的结果可能会出现损失；
        :param in_var_v: 表示输入z的v
        :param in_var_d:表示输入z的d
        :param out_var_v:表示输出sigma的v
        :param out_var_d:表示输出sigma的d
        :param isK: 用于判断模型使用区别；当isK=1是，固定sigma(out_var_v,out_var_d)复制给z(in_var_v, in_var_d);当isK=0时，
        固定z(in_var_v, in_var_d)复制给sigma(out_var_v,out_var_d)
        :param step:表示步数
        :return:
        本模型需要创建一个中间变量delta-c，"cv7" + "_" + str(step) + "_" + str(i)表示的delta-c的v，"cv7" + "_" + str(step) + "_" + str(i)表示的delta-c的d;
        """
        eqn = "% expand_model\n"
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable(in_var_c_v[0]),
                                                             self.save_variable(in_var_c_d[0]))
        if isK == 1:
            for i in range(32):
                temp = [self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_v[i]),
                        self.save_variable(in_var_d[i]),
                        self.save_variable(in_var_c_v[i]),
                        self.save_variable(in_var_c_d[i]),
                        self.save_variable(in_var_c_v[i + 1]),
                        self.save_variable(in_var_c_d[i + 1])]
                eqn += self.create_constraints(temp, expand_model_contsrain_2)
            self.__constraints.append(eqn)
        else:
            for i in range(32):
                temp = [self.save_variable(in_var_v[i]),
                        self.save_variable(in_var_d[i]),
                        self.save_variable(in_var_c_v[i]),
                        self.save_variable(in_var_c_d[i]),

                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_c_v[i + 1]),
                        self.save_variable(in_var_c_d[i + 1])]
                eqn += self.create_constraints(temp, expand_model_contsrain_1)
            self.__constraints.append(eqn)

    def modadd_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_c_v, in_var_c_d, out_var_v,
                     out_var_d):
        # print("245:modadd_model")
        eqn = "% modadd_model\n"
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable(in_var_c_v[0]),
                                                             self.save_variable(in_var_c_d[0]))
        for i in range(32):
            temp = [self.save_variable(in_var_v_0[i]),
                    self.save_variable(in_var_d_0[i]),
                    self.save_variable(in_var_v_1[i]),
                    self.save_variable(in_var_d_1[i]),
                    self.save_variable(in_var_c_v[i]),
                    self.save_variable(in_var_c_d[i]),
                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),
                    self.save_variable(in_var_c_v[i + 1]),
                    self.save_variable(in_var_c_d[i + 1])]
            eqn += self.create_constraints(temp, modadd_model_constrain)
        self.__constraints.append(eqn)

    def left_shift(self, order, num):

        return order[-num:] + order[:-num]

    def derive_cond(self, in_var_x, in_var_v_x, in_var_d_x):
        for i in range(32):
            temp = [self.save_variable(in_var_x[i]),
                    self.save_variable(in_var_v_x[i]),
                    self.save_variable(in_var_d_x[i])]
            eqn = self.create_constraints(temp, derive_cond_constrain)
            self.__constraints.append(eqn)

    def R(self, fNa, in_var_v_m, in_var_d_m, in_var_v_a0, in_var_d_a0, in_var_v_a1, in_var_d_a1,
          in_var_v_a2, in_var_d_a2, in_var_v_a3, in_var_d_a3, in_var_v_a4, in_var_d_a4, in_var_a3, in_var_a2, in_var_a1,
          step):
        print("\n589: %s-R:" % (step))
        in_var_v_b0 = []
        in_var_d_b0 = []
        in_var_v_b1 = []
        in_var_d_b1 = []
        in_var_v_b2 = []
        in_var_d_b2 = []
        in_var_v_b3 = []
        in_var_d_b3 = []
        in_var_v_b4 = []
        in_var_d_b4 = []
        for i in range(32):
            in_var_v_b0.append("bv0" + "_" + str(step) + "_" + str(i))
            in_var_d_b0.append("bd0" + "_" + str(step) + "_" + str(i))
            in_var_v_b1.append("bv1" + "_" + str(step) + "_" + str(i))
            in_var_d_b1.append("bd1" + "_" + str(step) + "_" + str(i))
            in_var_v_b2.append("bv2" + "_" + str(step) + "_" + str(i))
            in_var_d_b2.append("bd2" + "_" + str(step) + "_" + str(i))
            in_var_v_b3.append("bv3" + "_" + str(step) + "_" + str(i))
            in_var_d_b3.append("bd3" + "_" + str(step) + "_" + str(i))
            in_var_v_b4.append("bv4" + "_" + str(step) + "_" + str(i))
            in_var_d_b4.append("bd4" + "_" + str(step) + "_" + str(i))

        # Claim signed difference vectors ∇c2,∇c3 of size 33.
        in_var_v_c0 = []
        in_var_d_c0 = []
        in_var_v_c1 = []
        in_var_d_c1 = []
        in_var_v_c2 = []
        in_var_d_c2 = []
        for i in range(33):
            in_var_v_c0.append("cv0" + "_" + str(step) + "_" + str(i))
            in_var_d_c0.append("cd0" + "_" + str(step) + "_" + str(i))
            in_var_v_c1.append("cv1" + "_" + str(step) + "_" + str(i))
            in_var_d_c1.append("cd1" + "_" + str(step) + "_" + str(i))
            in_var_v_c2.append("cv2" + "_" + str(step) + "_" + str(i))
            in_var_d_c2.append("cd2" + "_" + str(step) + "_" + str(i))

        # print("722行代码表示将m赋值给b:\nASSERT %s\n"%eqn)
        for i in range(32):
            self.__constraints.append("ASSERT %s = %s;\n" % (self.save_variable(in_var_v_m[i]), in_var_v_b0[i]))
            self.__constraints.append("ASSERT %s = %s;\n" % (self.save_variable(in_var_d_m[i]), in_var_d_b0[i]))
        self.derive_cond(in_var_a1, in_var_v_a1, in_var_d_a1)
        self.derive_cond(in_var_a2, in_var_v_a2, in_var_d_a2)
        self.derive_cond(in_var_a3, in_var_v_a3, in_var_d_a3)
        self.boolfast_model(fNa, in_var_v_a3, in_var_d_a3, in_var_v_a2, in_var_d_a2, in_var_v_a1, in_var_d_a1,
                            in_var_v_b1, in_var_d_b1)
        self.boolfull_model(fNa, in_var_v_a3, in_var_d_a3, in_var_v_a2, in_var_d_a2, in_var_v_a1, in_var_d_a1,
                            in_var_v_b1, in_var_d_b1, in_var_a3, in_var_a2, in_var_a1)

        self.modadd_model(in_var_v_b0, in_var_d_b0, in_var_v_b1, in_var_d_b1, in_var_v_c0, in_var_d_c0,
                          in_var_v_b2, in_var_d_b2)

        self.modadd_model(in_var_v_b2, in_var_d_b2, in_var_v_a0, in_var_d_a0, in_var_v_c1, in_var_d_c1,
                          in_var_v_b3, in_var_d_b3)
        if self.__bounds_rounds - 4 <= step:
            self.expand_model(in_var_v_b3, in_var_d_b3, in_var_v_c2, in_var_d_c2,
                              self.right_shift(in_var_v_a4, rotation_Constant_left[step]),
                              self.right_shift(in_var_d_a4, rotation_Constant_left[step]), 1)
        else:
            self.expand_model(in_var_v_b3, in_var_d_b3, in_var_v_c2, in_var_d_c2,
                              self.right_shift(in_var_v_a4, rotation_Constant_left[step]),
                              self.right_shift(in_var_d_a4, rotation_Constant_left[step]), 0)

    """检查赋值是否重复"""

    def check_assign(self, s):
        if s not in self.__assign:
            self.__assign.append(s)

    def assign_value(self):

        for i in range(self.__bounds_rounds - 4, self.__bounds_rounds):
            for j in range(32):
                temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable("xd_" + str(i) + "_" + str(j)),
                                                                     self.save_variable("xv_" + str(i) + "_" + str(j)))
                self.check_assign(temp)
        ss = ["=====n====n=====================",
              "====u=====================u=====",
              "==0=========================00==",
              "==1=============01=========011=="]
        for i in range(len(ss)):
            for j in range(32):
                if ss[i][31 - j] == "=":
                    temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("xd_" + str(i) + "_" + str(j)),
                        self.save_variable("xv_" + str(i) + "_" + str(j)))
                    self.check_assign(temp)
                elif ss[i][31 - j] == "n":
                    temp = "ASSERT %s = 0bin1;\nASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("xd_" + str(i) + "_" + str(j)),
                        self.save_variable("xv_" + str(i) + "_" + str(j)),
                        self.save_variable("x_" + str(i) + "_" + str(j)))
                    self.check_assign(temp)
                elif ss[i][31 - j] == "u":
                    temp = "ASSERT %s = 0bin1;\nASSERT %s = 0bin1;\nASSERT %s = 0bin1;\n" % (
                        self.save_variable("xd_" + str(i) + "_" + str(j)),
                        self.save_variable("xv_" + str(i) + "_" + str(j)),
                        self.save_variable("x_" + str(i) + "_" + str(j)))
                    self.check_assign(temp)
                elif ss[i][31 - j] == "0":
                    temp = "ASSERT %s = 0bin0;\n" % (
                        self.save_variable("x_" + str(i) + "_" + str(j)))
                    temp += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("xd_" + str(i) + "_" + str(j)),
                        self.save_variable("xv_" + str(i) + "_" + str(j)))

                    self.check_assign(temp)
                elif ss[i][31 - j] == "1":
                    temp = "ASSERT %s = 0bin1;\n" % (
                        self.save_variable("x_" + str(i) + "_" + str(j)))
                    temp += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("xd_" + str(i) + "_" + str(j)),
                        self.save_variable("xv_" + str(i) + "_" + str(j)))

                    self.check_assign(temp)

        for i in range(16):
            if i == 2:
                for j in range(32):
                    if j != (self.__num + 7) % 32:
                        temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                            self.save_variable("md_" + str(i) + "_" + str(j)),
                            self.save_variable("mv_" + str(i) + "_" + str(j)))
                        self.__constraints.append(temp)
                    else:
                        temp = "ASSERT %s = 0bin1;\nASSERT %s = 0bin1;\n" % (
                            self.save_variable("md_" + str(i) + "_" + str(j)),
                            self.save_variable("mv_" + str(i) + "_" + str(j)))
                        self.__constraints.append(temp)
            elif i == 12:
                for j in range(32):
                    if j != self.__num:
                        temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                            self.save_variable("md_" + str(i) + "_" + str(j)),
                            self.save_variable("mv_" + str(i) + "_" + str(j)))
                        self.__constraints.append(temp)
                    else:
                        temp = "ASSERT %s = 0bin1;\nASSERT %s = 0bin0;\n" % (
                            self.save_variable("md_" + str(i) + "_" + str(j)),
                            self.save_variable("mv_" + str(i) + "_" + str(j)))
                        self.__constraints.append(temp)
            else:
                for j in range(32):
                    temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("md_" + str(i) + "_" + str(j)),
                        self.save_variable("mv_" + str(i) + "_" + str(j)))
                    self.__constraints.append(temp)
        # obj = "ASSERT BVPLUS(10,"
        # for i in range(11, 17):
        #     for j in range(32):
        #         if i == 16 and j == 31:
        #             obj += "0bin000000000@xd_%s_%s) = 0bin" % (i, j) + bin(2)[2:].zfill(10) + ";\n"
        #         else:
        #             obj += "0bin000000000@xd_%s_%s" % (i, j) + ", "
        # self.__constraints.append(obj)

    def Object(self, object_value):
        obj = "ASSERT BVPLUS(10,"
        for i in range(4, 17):
            for j in range(32):
                if i == 16 and j == 31:
                    obj += "0bin000000000@xd_%s_%s) = 0bin" % (i, j) + bin(object_value)[2:].zfill(10) + ";\n"
                else:
                    obj += "0bin000000000@xd_%s_%s" % (i, j) + ", "

        return obj

    def main(self):
        in_var_v_a = []
        in_var_d_a = []
        in_var_v_m = []
        in_var_d_m = []
        in_var_a = []
        for step in range(0, self.__bounds_rounds):
            temp_v_a = []
            temp_d_a = []
            temp_a = []
            for i in range(32):
                temp_v_a.append("xv_" + str(step) + "_" + str(i))
                temp_d_a.append("xd_" + str(step) + "_" + str(i))
                temp_a.append("x_" + str(step) + "_" + str(i))
            in_var_v_a.append(temp_v_a)
            in_var_d_a.append(temp_d_a)

            in_var_a.append(temp_a)
        for step in range(0, 16):
            temp_v_m = []
            temp_d_m = []
            for i in range(32):
                temp_v_m.append("mv_" + str(step) + "_" + str(i))
                temp_d_m.append("md_" + str(step) + "_" + str(i))
            in_var_v_m.append(temp_v_m)
            in_var_d_m.append(temp_d_m)

        for i in range(self.__step, self.__bounds_rounds):
            self.R(Bool_left[(i - 4) // 16],
                   in_var_v_m[message_order_left[(i)]],
                   in_var_d_m[message_order_left[(i)]],
                   in_var_v_a[i - 4],
                   in_var_d_a[i - 4],
                   in_var_v_a[i - 3],
                   in_var_d_a[i - 3],
                   in_var_v_a[i - 2],
                   in_var_d_a[i - 2],
                   in_var_v_a[i - 1],
                   in_var_d_a[i - 1],
                   in_var_v_a[i],
                   in_var_d_a[i],
                   in_var_a[i - 1],
                   in_var_a[i - 2],
                   in_var_a[i - 3], i)

    def solver(self):
        self.main()
        self.assign_value()
        constrain = "".join(self.__constraints)
        assign = "".join(self.__assign)
        variable = "".join(self.__declare)
        query = '\n' + 'QUERY FALSE;\nCOUNTEREXAMPLE;'

        for i in range(80, -1, -1):
            print("差分路线中有差分的个数为:%s" % i)
            obj = self.Object(i)
            file_write = open("right_model.cvc", "w")
            file_write.write(variable)
            file_write.write(constrain)
            file_write.write(assign)
            file_write.write(obj)
            file_write.write(query)
            file_write.close()
            stp_parameters = ["stp", "right_model.cvc", "--cryptominisat", "--threads", "16"]
            R = subprocess.check_output(stp_parameters)

            if "Valid.\n" != R.decode():
                file = open("left_res2.out", "w")
                print("差分路线中有差分的个数为:%s 满足" % i)
                file.write(R.decode())
                file.close()

            else:
                print("差分路线中有差分的个数为:%s 不满足" % i)
                break


if __name__ == '__main__':
    step = 4
    bounds = 17
    for i in range(1):
        print(i)
        FunctionModel(step, bounds, i).solver()
