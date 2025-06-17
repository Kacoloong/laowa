import subprocess

from constrain_condition import *


class FunctionModel:
    def __init__(self, steps, bounds, message_bound):

        self.__bounds_rounds = bounds
        self.__message_bound = message_bound
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

    """检查赋值是否重复"""

    def check_assign(self, s):
        if s not in self.__assign:
            self.__assign.append(s)

    def left_shift(self, order, num):
        """
        表示循环移位
        :param order:
        :param num:
        :return:
        """
        return order[-num:] + order[:-num]

    def xor_function(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                     out_var_d, in_var_0, in_var_1, in_var_2):
        eqn = "% xor" + "%s model\n" % out_var_d[0]
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

    def if_function(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v, out_var_d,
                    in_var_0, in_var_1, in_var_2):

        eqn = ""
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
            eqn += self.create_constraints(temp, ifx_full_constrain)
        self.__constraints.append(eqn)

    def maj_function(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                     out_var_d, in_var_0, in_var_1, in_var_2, ):
        eqn = ""
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
            eqn += self.create_constraints(temp, maj_full_constrain)
        self.__constraints.append(eqn)

    def expand_model(self, in_var_v, in_var_d, c_var_v, c_var_d, out_var_v, out_var_d):

        eqn = "% expand_model\n"
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (c_var_v[0], c_var_d[0])
        for i in range(32):
            temp = [self.save_variable(in_var_v[i]),
                    self.save_variable(in_var_d[i]),
                    self.save_variable(c_var_v[i]),
                    self.save_variable(c_var_d[i]),

                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),
                    self.save_variable(c_var_v[i + 1]),
                    self.save_variable(c_var_d[i + 1])]

            eqn += self.create_constraints(temp, expand_model_contsrain_1)

        self.__constraints.append(eqn)

    def modadd_model(self, in_var_v_0, in_var_d_0,
                     in_var_v_1, in_var_d_1,
                     in_var_c_v, in_var_c_d,
                     out_var_v, out_var_d):
        eqn = "ASSERT %s = 0bin0;\n" % (in_var_c_v[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c_d[0])
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

    def R(self, in_var_v_m, in_var_d_m, in_var_v_a0, in_var_d_a0, in_var_v_a1, in_var_d_a1, in_var_v_a2, in_var_d_a2,
          in_var_v_a3, in_var_d_a3, in_var_v_a4, in_var_d_a4, in_var_v_e0, in_var_d_e0, in_var_v_e1, in_var_d_e1,
          in_var_v_e2, in_var_d_e2, in_var_v_e3, in_var_d_e3, in_var_v_e4, in_var_d_e4, in_var_a0, in_var_a1, in_var_a2,
          in_var_a3, in_var_e0, in_var_e1, in_var_e2, in_var_e3, step):
        # Claim signed difference vectors ∇b0,∇b1,∇b2,∇b3 of size 32,let a reputation b0, b1,b2,b3
        in_var_v_b = []
        in_var_d_b = []
        for i in range(10):
            temp_b_v = []
            temp_b_d = []
            for j in range(32):
                temp_b_v.append("bv" + str(i) + "_" + str(step) + "_" + str(j))
                temp_b_d.append("bd" + str(i) + "_" + str(step) + "_" + str(j))
            in_var_v_b.append(temp_b_v)
            in_var_d_b.append(temp_b_d)

        # Claim signed difference vectors ∇c2,∇c3 of size 33.
        in_var_v_c = []
        in_var_d_c = []
        for i in range(8):
            temp_c_v = []
            temp_c_d = []
            for j in range(33):
                temp_c_v.append("cv" + str(i) + "_" + str(step) + "_" + str(j))
                temp_c_d.append("cd" + str(i) + "_" + str(step) + "_" + str(j))

            in_var_v_c.append(temp_c_v)
            in_var_d_c.append(temp_c_d)

        self.xor_function(in_var_v_e3, in_var_d_e3,
                          self.left_shift(in_var_v_e3, 19), self.left_shift(in_var_d_e3, 19),
                          self.left_shift(in_var_v_e3, 29), self.left_shift(in_var_d_e3, 29),
                          in_var_v_b[0], in_var_d_b[0],
                          in_var_e3,
                          self.left_shift(in_var_e3, 19),
                          self.left_shift(in_var_e3, 29))

        self.maj_function(self.left_shift(in_var_v_e1, 2), self.left_shift(in_var_d_e1, 2),
                          in_var_v_e2, in_var_d_e2,
                          in_var_v_e3, in_var_d_e3,
                          in_var_v_b[1], in_var_d_b[1],
                          self.left_shift(in_var_e1, 2),
                          in_var_e2,
                          in_var_e3)

        self.modadd_model(self.left_shift(in_var_v_e0, 2), self.left_shift(in_var_d_e0, 2),
                          in_var_v_b[0], in_var_d_b[0],
                          in_var_v_c[0], in_var_d_c[0],
                          in_var_v_b[2], in_var_d_b[2])
        self.modadd_model(in_var_v_b[2], in_var_d_b[2],
                          in_var_v_b[1], in_var_d_b[1],
                          in_var_v_c[1], in_var_d_c[1],
                          in_var_v_b[3], in_var_d_b[3])
        self.modadd_model(in_var_v_m, in_var_d_m,
                          in_var_v_b[3], in_var_d_b[3],
                          in_var_v_c[2], in_var_d_c[2],
                          in_var_v_b[4], in_var_d_b[4])
        # computer ai
        self.expand_model(in_var_v_b[4], in_var_d_b[4],
                          in_var_v_c[3], in_var_d_c[3],
                          in_var_v_a4, in_var_d_a4)

        # computer Ei
        self.xor_function(in_var_v_a3, in_var_d_a3,
                          self.left_shift(in_var_v_a3, 11), self.left_shift(in_var_d_a3, 11),
                          self.left_shift(in_var_v_a3, 25), self.left_shift(in_var_d_a3, 25),
                          in_var_v_b[5], in_var_d_b[5],
                          in_var_a3,
                          self.left_shift(in_var_a3, 11),
                          self.left_shift(in_var_a3, 25))

        self.if_function(self.left_shift(in_var_v_a1, 17), self.left_shift(in_var_d_a1, 17),
                         in_var_v_a2, in_var_d_a2,
                         in_var_v_a3, in_var_d_a3,
                         in_var_v_b[6], in_var_d_b[6],
                         self.left_shift(in_var_a1, 17),
                         in_var_a2,
                         in_var_a3)
        # print(self.left_shift(in_var_v_a1, 17))

        self.modadd_model(in_var_v_b[5], in_var_d_b[5],
                          in_var_v_b[6], in_var_d_b[6],
                          in_var_v_c[4], in_var_d_c[4],
                          in_var_v_b[7], in_var_d_b[7])

        self.modadd_model(in_var_v_m, in_var_d_m,
                          in_var_v_b[7], in_var_d_b[7],
                          in_var_v_c[5], in_var_d_c[5],
                          in_var_v_b[8], in_var_d_b[8])
        self.modadd_model(self.left_shift(in_var_v_a0, 17), self.left_shift(in_var_d_a0, 17),
                          in_var_v_b[8], in_var_d_b[8],
                          in_var_v_c[6], in_var_d_c[6],
                          in_var_v_b[9], in_var_d_b[9])
        self.expand_model(in_var_v_b[9], in_var_d_b[9],
                          in_var_v_c[7], in_var_d_c[7],
                          in_var_v_e4, in_var_d_e4)

    def message_expand(self, in_var_v_w0, in_var_d_w0, in_var_v_w1, in_var_d_w1, in_var_v_w2, in_var_d_w2, in_var_v_w3,
                       in_var_d_w3, in_var_w0, in_var_w2, in_var_v_w4, in_var_d_w4, step):
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
            in_var_v_b0.append("mv0" + "_" + str(step) + "_" + str(i))
            in_var_d_b0.append("md0" + "_" + str(step) + "_" + str(i))
            in_var_v_b1.append("mv1" + "_" + str(step) + "_" + str(i))
            in_var_d_b1.append("md1" + "_" + str(step) + "_" + str(i))
            in_var_v_b2.append("mv2" + "_" + str(step) + "_" + str(i))
            in_var_d_b2.append("md2" + "_" + str(step) + "_" + str(i))
            in_var_v_b3.append("mv3" + "_" + str(step) + "_" + str(i))
            in_var_d_b3.append("md3" + "_" + str(step) + "_" + str(i))
            in_var_v_b4.append("mv4" + "_" + str(step) + "_" + str(i))
            in_var_d_b4.append("md4" + "_" + str(step) + "_" + str(i))
        in_var_v_c0 = []
        in_var_d_c0 = []
        in_var_v_c1 = []
        in_var_d_c1 = []
        in_var_v_c2 = []
        in_var_d_c2 = []
        in_var_v_c3 = []
        in_var_d_c3 = []
        for i in range(33):
            in_var_v_c0.append("mcv0" + "_" + str(step) + "_" + str(i))
            in_var_d_c0.append("mcd0" + "_" + str(step) + "_" + str(i))
            in_var_v_c1.append("mcv1" + "_" + str(step) + "_" + str(i))
            in_var_d_c1.append("mcd1" + "_" + str(step) + "_" + str(i))
            in_var_v_c2.append("mcv2" + "_" + str(step) + "_" + str(i))
            in_var_d_c2.append("mcd2" + "_" + str(step) + "_" + str(i))
            in_var_v_c3.append("mcv3" + "_" + str(step) + "_" + str(i))
            in_var_d_c3.append("mcd3" + "_" + str(step) + "_" + str(i))

        self.xor_function(in_var_v_w0, in_var_d_w0,
                          self.left_shift(in_var_v_w0, 7), self.left_shift(in_var_d_w0, 7),
                          self.left_shift(in_var_v_w0, 22), self.left_shift(in_var_d_w0, 22),
                          in_var_v_b0, in_var_d_b0,
                          in_var_w0,
                          self.left_shift(in_var_w0, 7),
                          self.left_shift(in_var_w0, 22))
        self.modadd_model(in_var_v_b0, in_var_d_b0,
                          in_var_v_w1, in_var_d_w1,
                          in_var_v_c0, in_var_d_c0,
                          in_var_v_b1, in_var_d_b1)
        self.xor_function(in_var_v_w2, in_var_d_w2,
                          self.left_shift(in_var_v_w2, 13), self.left_shift(in_var_d_w2, 13),
                          self.left_shift(in_var_v_w2, 27), self.left_shift(in_var_d_w2, 27),
                          in_var_v_b2, in_var_d_b2,
                          in_var_w2,
                          self.left_shift(in_var_w2, 13),
                          self.left_shift(in_var_w2, 27))
        self.modadd_model(in_var_v_b1, in_var_d_b1,
                          in_var_v_b2, in_var_d_b2,
                          in_var_v_c1, in_var_d_c1,
                          in_var_v_b3, in_var_d_b3)
        self.modadd_model(in_var_v_b3, in_var_d_b3,
                          in_var_v_w3, in_var_d_w3,
                          in_var_v_c2, in_var_d_c2,
                          in_var_v_b4, in_var_d_b4)
        self.expand_model(in_var_v_b4, in_var_d_b4, in_var_v_c3, in_var_d_c3, in_var_v_w4, in_var_d_w4)

    def assign_value(self):

        for step in range(self.__step - 4, self.__step):
            for i in range(32):
                temp = "ASSERT xv_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                temp += "ASSERT xd_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                temp += "ASSERT yv_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                temp += "ASSERT yd_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                self.__constraints.append(temp)

        for step in range(self.__bounds_rounds - 4, self.__bounds_rounds):
            for i in range(32):
                temp = "ASSERT xv_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                temp += "ASSERT xd_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                self.__constraints.append(temp)
        for step in range(self.__bounds_rounds - 4, self.__bounds_rounds):
            for i in range(32):
                temp = "ASSERT yv_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                temp += "ASSERT yd_" + str(step) + "_" + str(i) + " = 0bin0;\n"
                self.__constraints.append(temp)
        ss = ["================================",
              "================================",
              "================================",
              "================================",
              "================================",
              "================================",
              "==u=============n============n==",
              "=============================n==",
              "=======n==============n======u==",
              "================================",
              "================================",
              "================================",
              "===u===n=====================u==",
              "================================",
              "==n====u=n==n===n=====u====u====",
              "================================",
              "=============================n==",
              "================================",
              "================================",
              "================================",
              "================================",
              "================================",
              "================================",
              "================================", ]
        for i in range(len(ss)):
            for j in range(32):
                if ss[i][j] == "u":
                    temp = "ASSERT wv_" + str(i) + "_" + str(31 - j) + " = 0bin1;\n"
                    temp += "ASSERT wd_" + str(i) + "_" + str(31 - j) + " = 0bin1;\n"
                    self.__constraints.append(temp)
                elif ss[i][j] == "n":
                    temp = "ASSERT wv_" + str(i) + "_" + str(31 - j) + " = 0bin0;\n"
                    temp += "ASSERT wd_" + str(i) + "_" + str(31 - j) + " = 0bin1;\n"
                    self.__constraints.append(temp)
                elif ss[i][j] == "=":
                    temp = "ASSERT wv_" + str(i) + "_" + str(31 - j) + " = 0bin0;\n"
                    temp += "ASSERT wd_" + str(i) + "_" + str(31 - j) + " = 0bin0;\n"
                    self.__constraints.append(temp)

    def main(self):
        print(f"start step: {self.__step}")
        print(f"end step: {self.__bounds_rounds}")
        in_var_v_a = []
        in_var_d_a = []
        in_var_v_e = []
        in_var_d_e = []
        in_var_a = []
        in_var_e = []
        in_var_v_w = []
        in_var_d_w = []
        in_var_w = []
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
        for step in range(0, self.__bounds_rounds):
            temp_v_e = []
            temp_d_e = []
            temp_e = []
            for i in range(32):
                temp_v_e.append("yv_" + str(step) + "_" + str(i))
                temp_d_e.append("yd_" + str(step) + "_" + str(i))
                temp_e.append("y_" + str(step) + "_" + str(i))
            in_var_v_e.append(temp_v_e)
            in_var_d_e.append(temp_d_e)
            in_var_e.append(temp_e)

        for step in range(0, self.__message_bound):
            temp_v_w = []
            temp_d_w = []
            temp_w = []
            for i in range(32):
                temp_v_w.append("wv_" + str(step) + "_" + str(i))
                temp_d_w.append("wd_" + str(step) + "_" + str(i))
                temp_w.append("w_" + str(step) + "_" + str(i))
            in_var_v_w.append(temp_v_w)
            in_var_d_w.append(temp_d_w)
            in_var_w.append(temp_w)

        for i in range(self.__step, self.__bounds_rounds):
            self.R(in_var_v_w[i], in_var_d_w[i], in_var_v_a[i - 4], in_var_d_a[i - 4],
                   in_var_v_a[i - 3], in_var_d_a[i - 3], in_var_v_a[i - 2], in_var_d_a[i - 2],
                   in_var_v_a[i - 1], in_var_d_a[i - 1], in_var_v_a[i], in_var_d_a[i],
                   in_var_v_e[i - 4], in_var_d_e[i - 4], in_var_v_e[i - 3], in_var_d_e[i - 3],
                   in_var_v_e[i - 2], in_var_d_e[i - 2], in_var_v_e[i - 1], in_var_d_e[i - 1],
                   in_var_v_e[i], in_var_d_e[i], in_var_a[i - 4], in_var_a[i - 3], in_var_a[i - 2], in_var_a[i - 1],
                   in_var_e[i - 4], in_var_e[i - 3], in_var_e[i - 2], in_var_e[i - 1], i)
        for i in range(self.__message_bound):
            if i > 15:
                self.message_expand(in_var_v_w[i - 1], in_var_d_w[i - 1],
                                    in_var_v_w[i - 9], in_var_d_w[i - 9],
                                    in_var_v_w[i - 15], in_var_d_w[i - 15],
                                    in_var_v_w[i - 16], in_var_d_w[i - 16],
                                    in_var_w[i - 1], in_var_w[i - 15],
                                    in_var_v_w[i], in_var_d_w[i], i)

        # temp = "ASSERT BVPLUS(10,"
        # for i in range(self.__step, self.__bounds_rounds):
        #     for j in range(32):
        #         if i == self.__bounds_rounds - 1 and j == 31:
        #             temp += "0bin000000000@%s) = 0bin%s;\n" % (
        #                 "yd_" + str(i) + "_" + str(j), bin(13)[2:].zfill(10))
        #         else:
        #             temp += "0bin000000000@%s," % ("yd_" + str(i) + "_" + str(j))
        # self.__constraints.append(temp)

    def obj_value(self, obj_value):
        temp = "ASSERT BVPLUS(10,"
        for i in range(self.__step, self.__bounds_rounds):
            for j in range(32):
                if i == self.__bounds_rounds - 1 and j == 31:
                    temp += "0bin000000000@%s) = 0bin%s;\n" % (
                        "yd_" + str(i) + "_" + str(j), bin(obj_value)[2:].zfill(10))
                else:
                    temp += "0bin000000000@%s," % ("yd_" + str(i) + "_" + str(j))
        return temp

    def solver(self):
        self.main()
        self.assign_value()
        constrain = "".join(self.__constraints)
        assign = "".join(self.__assign)
        variable = "".join(self.__declare)
        query = '\n' + 'QUERY FALSE;\nCOUNTEREXAMPLE;'
        for obj_val in range(30, -1, -1):
            file_write = open("model.cvc", "w")
            obj = self.obj_value(obj_val)
            file_write.write(variable)
            file_write.write(constrain)
            file_write.write(assign)
            file_write.write(obj)
            file_write.write(query)
            file_write.close()
            print("差分路线中有差分的个数为%s" % obj_val)
            stp_parameters = ["stp", "model.cvc", "--cryptominisat", "--threads", "16"]
            R = subprocess.check_output(stp_parameters)
            if "Valid.\n" != R.decode():
                file = open("right_res2_" + str(obj_val) + ".out", "w")
                file.write(R.decode())
                file.close()
                print("差分路线中有差分的个数为%s: 满足" % obj_val)
            else:
                print("差分路线中有差分的个数为%s: 不满足" % obj_val)
                break


if __name__ == '__main__':
    step = 8
    bounds = 18
    message_bound = 24
    FunctionModel(step, bounds, message_bound).solver()
