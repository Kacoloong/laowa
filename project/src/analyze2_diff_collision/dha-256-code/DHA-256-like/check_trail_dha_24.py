# -*- coding: utf-8 -*-
# @Time    : 2022 2022/7/6 13:51
# @Author  : liyx
# @Project : computer_pycharm
# @file_name :sha_256_test.py
import subprocess
import time

from constrain_condition import *


class ripemd:
    def __init__(self, rounds, message):
        self.__rounds = rounds
        self.__message_rounds = message
        self.__declare = []  # 存储变量
        self.__constraints = []  # 存储约束语句
        self.__assign = []  # 存储赋值约束
        self.__in_var_a_0 = []  # 存储右分支的变量
        self.__in_var_a_1 = []
        self.__in_var_e_0 = []  # 存储右分支的变量
        self.__in_var_e_1 = []
        self.__in_var_m_0 = []  # 存储消息字变量
        self.__in_var_m_1 = []
        self.__in_var_c = []  # 常数K
        self.create_variable()

    def create_variable(self):
        # 左分支的变量
        for step in range(self.__rounds + 4):
            temp_0 = []
            temp_1 = []
            for i in range(32):
                temp_0.append("a0_" + str(step) + "_" + str(i))
                temp_1.append("a1_" + str(step) + "_" + str(i))
            self.__in_var_a_0.append(temp_0)
            self.__in_var_a_1.append(temp_1)
        for step in range(self.__message_rounds):
            temp = []
            for i in range(32):
                temp.append("c_" + str(step) + "_" + str(i))
            self.__in_var_c.append(temp)
            # 右分支变量左分支的变量
        for step in range(self.__rounds + 4):
            temp_0 = []
            temp_1 = []
            for i in range(32):
                temp_0.append("e0_" + str(step) + "_" + str(i))
                temp_1.append("e1_" + str(step) + "_" + str(i))
            self.__in_var_e_0.append(temp_0)
            self.__in_var_e_1.append(temp_1)

        for m in range(self.__message_rounds):
            temp_0 = []
            temp_1 = []
            for i in range(32):
                temp_0.append("w0_" + str(m) + "_" + str(i))
                temp_1.append("w1_" + str(m) + "_" + str(i))
            self.__in_var_m_0.append(temp_0)
            self.__in_var_m_1.append(temp_1)

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

    def left_shift(self, order, num):
        """
        表示循环移位
        :param order:
        :param num:
        :return:
        """
        return order[-num:] + order[:-num]

    def modadd(self, a, b, c, v):
        """
        计算模加操作的函数v = (a ⊞ b)
        :param a:表示模加操作的输入
        :param b:表示模加操作的输入
        :param v:表示模加操作的输出
        :return:
        """
        eqn = "%"
        eqn += " %s %s %s %s \n" % (a[0], b[0], c[0], v[0])
        self.__constraints.append(eqn)
        for i in range(32):
            temp = [self.save_variable(a[i]),
                    self.save_variable(b[i]),
                    self.save_variable(c[i]),
                    self.save_variable(v[i]),
                    self.save_variable(c[i + 1])]
            eqn = self.create_constraints(temp, modadd_model)
            self.__constraints.append(eqn)

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

    def boolean(self, x0, x1, x2, out, fna):
        if fna == "MAJ":
            for i in range(32):
                temp = [self.save_variable(x0[i]),
                        self.save_variable(x1[i]),
                        self.save_variable(x2[i]),
                        self.save_variable(out[i])]
                eqn = self.create_constraints(temp, maj)
                self.__constraints.append(eqn)
        elif fna == "XOR":
            for i in range(32):
                temp = [self.save_variable(x0[i]),
                        self.save_variable(x1[i]),
                        self.save_variable(x2[i]),
                        self.save_variable(out[i])]
                eqn = self.create_constraints(temp, xor)
                self.__constraints.append(eqn)
        elif fna == "IF":
            for i in range(32):
                temp = [self.save_variable(x0[i]),
                        self.save_variable(x1[i]),
                        self.save_variable(x2[i]),
                        self.save_variable(out[i])]
                eqn = self.create_constraints(temp, ifx)
                self.__constraints.append(eqn)

    def R_r(self, fna0, fna1, a0, a1, a2, a3, a4, e0, e1, e2, e3, e4, m, c, step, num):
        in_var_b0 = []
        in_var_b1 = []
        in_var_b2 = []
        in_var_b3 = []
        in_var_b4 = []
        in_var_b5 = []
        in_var_b6 = []
        in_var_b7 = []
        in_var_b8 = []
        in_var_b9 = []
        in_var_b10 = []
        for i in range(32):
            in_var_b0.append("b0" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b1.append("b1" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b2.append("b2" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b3.append("b3" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b4.append("b4" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b5.append("b5" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b6.append("b6" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b7.append("b7" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b8.append("b8" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b9.append("b9" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b10.append("b10" + str(num) + "_" + str(step) + "_" + str(i))
        in_var_c0 = []
        in_var_c1 = []
        in_var_c2 = []
        in_var_c3 = []
        in_var_c4 = []
        in_var_c5 = []
        in_var_c6 = []
        in_var_c7 = []
        for i in range(33):
            in_var_c0.append("c0" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c1.append("c1" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c2.append("c2" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c3.append("c3" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c4.append("c4" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c5.append("c5" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c6.append("c6" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c7.append("c7" + str(num) + "_" + str(step) + "_" + str(i))
        eqn = "ASSERT %s = 0bin0;\n" % (in_var_c0[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c1[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c2[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c3[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c4[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c5[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c6[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c7[0])

        self.__constraints.append(eqn)
        self.boolean(e3,
                     self.left_shift(e3, 19),
                     self.left_shift(e3, 29),
                     in_var_b0, "XOR")
        self.boolean(self.left_shift(e1, 2), e2, e3, in_var_b1, "MAJ")
        self.modadd(in_var_b0, in_var_b1, in_var_c0, in_var_b2)
        self.modadd(m, in_var_b2, in_var_c1, in_var_b3)
        self.modadd(c, in_var_b3, in_var_c2, in_var_b4)
        # computer ei
        self.modadd(self.left_shift(e0, 2), in_var_b4, in_var_c3, a4)
        # computer ai
        self.boolean(a3,
                     self.left_shift(a3, 11),
                     self.left_shift(a3, 25),
                     in_var_b6, "XOR")
        self.boolean(self.left_shift(a1, 17), a2, a3, in_var_b7, "IF")
        self.modadd(in_var_b7, in_var_b6, in_var_c4, in_var_b8)
        self.modadd(in_var_b8, m, in_var_c5, in_var_b9)
        self.modadd(c, in_var_b9, in_var_c6, in_var_b10)
        self.modadd(in_var_b10, self.left_shift(a0, 17), in_var_c7, e4)

    def assign_value_e(self):
        x = ["================================",
             "================================",
             "================================",
             "================================",

             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "=====u===u===============u======",
             "============n===========n=======",
             "======================u=====n===",
             "================================",
             "================================",
             "======nu===n===============n====",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================"]
        for step in range(self.__message_rounds):
            for i in range(32):
                eqn = "ASSERT %s = 0bin%s;\n" % (self.save_variable(self.__in_var_c[step][31 - i]),
                                                 bin(k_constant[step])[2:].zfill(32)[i])
                self.__constraints.append(eqn)

        for step in range(self.__rounds + 4):
            for i in range(32):
                if x[step][31 - i] == "n":
                    eqn = "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_e_0[step][i])
                    eqn += "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_e_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "u":
                    eqn = "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_e_0[step][i])
                    eqn += "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_e_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "=":
                    eqn = "ASSERT %s = %s;\n" % (self.save_variable(self.__in_var_e_0[step][i]),
                                                 self.save_variable(self.__in_var_e_1[step][i]))
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "1":
                    eqn = "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_e_0[step][i])
                    eqn += "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_e_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "0":
                    eqn = "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_e_0[step][i])
                    eqn += "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_e_1[step][i])
                    self.__assign.append(eqn)

    def assign_value_a(self):
        x = ["================================",
             "================================",
             "================================",
             "================================",

             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",

             "01010111110===========0000=10111",
             "1010000=111==0=0===0==0000=10=0=",
             "01=01uunn=nnnnnnnnnnnnnnnn1=11=0",
             "11u000n10000n0n0u0uu10n01110u1u1",
             "010110110101u00u01110100011u0101",
             "uuuu00011u101101001110u1uu100nuu",
             "0=un=11unuu00111010=110u0100101=",
             "011nuuuuuuu1101000000n1uuuu00000",
             "======0==========01===0101======",
             "======1===========0===1100======",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================"]

        for step in range(self.__rounds + 4):
            print(x[step])
            for i in range(32):
                if x[step][31 - i] == "n":
                    eqn = "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_a_0[step][i])
                    eqn += "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_a_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "u":
                    eqn = "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_a_0[step][i])
                    eqn += "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_a_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "1":
                    eqn = "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_a_0[step][i])
                    eqn += "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_a_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "0":
                    eqn = "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_a_0[step][i])
                    eqn += "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_a_1[step][i])
                    self.__assign.append(eqn)
                else:
                    eqn = "ASSERT %s = %s;\n" % (self.save_variable(self.__in_var_a_0[step][i]),
                                                 self.save_variable(self.__in_var_a_1[step][i]))
                    self.__assign.append(eqn)

    def message_expand(self, in_w_0, in_w_1, in_w_2, in_w_3, out_w, num, step):
        in_var_b0 = []
        in_var_b1 = []
        in_var_b2 = []
        in_var_b3 = []

        for i in range(32):
            in_var_b0.append("b0w" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b1.append("b1w" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b2.append("b2w" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_b3.append("b3w" + str(num) + "_" + str(step) + "_" + str(i))

        in_var_c0 = []
        in_var_c1 = []
        in_var_c2 = []

        for i in range(33):
            in_var_c0.append("c0w" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c1.append("c1w" + str(num) + "_" + str(step) + "_" + str(i))
            in_var_c2.append("c2w" + str(num) + "_" + str(step) + "_" + str(i))

        eqn = "ASSERT %s = 0bin0;\n" % (in_var_c0[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c1[0])
        eqn += "ASSERT %s = 0bin0;\n" % (in_var_c2[0])
        self.__constraints.append(eqn)

        self.boolean(in_w_0,
                     self.left_shift(in_w_0, 7),
                     self.left_shift(in_w_0, 22),
                     in_var_b0, "XOR")

        self.boolean(in_w_2,
                     self.left_shift(in_w_2, 13),
                     self.left_shift(in_w_2, 27),
                     in_var_b1, "XOR")
        self.modadd(in_var_b0, in_var_b1, in_var_c0, in_var_b2)
        self.modadd(in_w_1, in_var_b2, in_var_c1, in_var_b3)
        self.modadd(in_w_3, in_var_b3, in_var_c2, out_w)

    def main_R(self):

        for step in range(4, self.__rounds + 4):
            self.R_r("IF", "MAJ", self.__in_var_a_0[step - 4], self.__in_var_a_0[step - 3],
                     self.__in_var_a_0[step - 2], self.__in_var_a_0[step - 1], self.__in_var_a_0[step],
                     self.__in_var_e_0[step - 4], self.__in_var_e_0[step - 3], self.__in_var_e_0[step - 2],
                     self.__in_var_e_0[step - 1], self.__in_var_e_0[step], self.__in_var_m_0[step - 4],
                     self.__in_var_c[step - 4], step, 0)
            self.R_r("IF", "MAJ", self.__in_var_a_1[step - 4], self.__in_var_a_1[step - 3],
                     self.__in_var_a_1[step - 2], self.__in_var_a_1[step - 1], self.__in_var_a_1[step],
                     self.__in_var_e_1[step - 4], self.__in_var_e_1[step - 3], self.__in_var_e_1[step - 2],
                     self.__in_var_e_1[step - 1], self.__in_var_e_1[step], self.__in_var_m_1[step - 4],
                     self.__in_var_c[step - 4], step, 1)
        for step in range(self.__message_rounds):
            if step > 15:
                self.message_expand(self.__in_var_m_0[step - 1],
                                    self.__in_var_m_0[step - 9],
                                    self.__in_var_m_0[step - 15],
                                    self.__in_var_m_0[step - 16],
                                    self.__in_var_m_0[step],
                                    0, step)
                self.message_expand(self.__in_var_m_1[step - 1],
                                    self.__in_var_m_1[step - 9],
                                    self.__in_var_m_1[step - 15],
                                    self.__in_var_m_1[step - 16],
                                    self.__in_var_m_1[step],
                                    1, step)

    def assign_value_w(self):
        x = ["================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",

             "=====u==un==============un======",
             "==u=nn==nu=====n==nn==nuuu===un=",
             "================================",
             "================================",
             "================================",
             "================================",

             "=====u========u==========n====u=",
             "================================",
             "================================",
             "=====u===u===============u======",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             "================================",
             ]

        for step in range(self.__message_rounds):
            for i in range(32):
                if x[step][31 - i] == "n":
                    eqn = "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_m_0[step][i])
                    eqn += "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_m_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "u":
                    eqn = "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_m_0[step][i])
                    eqn += "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_m_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "=":
                    eqn = "ASSERT %s = %s;\n" % (self.save_variable(self.__in_var_m_0[step][i]),
                                                 self.save_variable(self.__in_var_m_1[step][i]))
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "1":
                    eqn = "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_m_0[step][i])
                    eqn += "ASSERT %s = 0bin1;\n" % self.save_variable(self.__in_var_m_1[step][i])
                    self.__assign.append(eqn)
                elif x[step][31 - i] == "0":
                    eqn = "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_m_0[step][i])
                    eqn += "ASSERT %s = 0bin0;\n" % self.save_variable(self.__in_var_m_1[step][i])
                    self.__assign.append(eqn)

    def main(self):

        start = time.time()
        self.main_R()
        self.assign_value_a()
        self.assign_value_e()
        self.assign_value_w()
        query = '\n' + 'QUERY FALSE;\nCOUNTEREXAMPLE;'
        constrain = "".join(self.__constraints)
        assign = "".join(self.__assign)
        variable = "".join(self.__declare)
        file_write = open("file.cvc", "w")
        file_write.write(variable)
        file_write.write(constrain)
        file_write.write(assign)
        file_write.write(query)
        file_write.close()
        print("start solver")
        stp_parameters = ["stp", "file.cvc", "--cryptominisat", "--threads", "16"]
        R = subprocess.check_output(stp_parameters)
        print(R.decode())
        open("res2_" + str(self.__rounds) + "_" + str(self.__message_rounds) + ".out", "w").write(R.decode())
        print(time.time() - start)


if __name__ == '__main__':
    ripemd(25, 25).main()
