import time

from gurobipy import *
from src.analyze2_diff_collision.boolear import *


# sys.stdout = open(os.devnull, 'w')

class FunctionModel:
    def __init__(self, startRounds, staRounds, msgBound, outputFile, block_size,
                 msg_i1, msg_i2, msg_i3, msg_i4, msg_i5, msg_i6,
                 status_i1, status_i2, status_i3, status_i4, status_i5, status_i6):

        self.__staRounds = staRounds
        self.__msgRounds = msgBound
        self.__startRounds = startRounds
        self.__declare = []  # 存储变量
        self.__constraints = []  # 存储约束语句
        self.__assign = []  # 存储赋值约束
        self.__objective = []  # 存储目标函数
        self.__msgResult = []  # 存储目标函数结果
        self.__model_msg = Model()
        self.__model_msgEA = Model()
        self.__outputFile = outputFile
        self.__msg_i1 = msg_i1
        self.__msg_i2 = msg_i2
        self.__msg_i3 = msg_i3
        self.__msg_i4 = msg_i4
        self.__msg_i5 = msg_i5
        self.__msg_i6 = msg_i6
        self.__status_i1 = status_i1
        self.__status_i2 = status_i2
        self.__status_i3 = status_i3
        self.__status_i4 = status_i4
        self.__status_i5 = status_i5
        self.__status_i6 = status_i6
        self.__block_size = block_size

        self.__result = []
        self.__aState = [["*" for _ in range(32)] for _ in range(self.__msgRounds)]
        self.__eState = [["*" for _ in range(32)] for _ in range(self.__msgRounds)]
        self.__wState = [["*" for _ in range(32)] for _ in range(self.__msgRounds)]
        self.__xorE = [["*" for _ in range(32)] for _ in range(self.__msgRounds)]
        self.__ifE = [["*" for _ in range(32)] for _ in range(self.__msgRounds)]
        self.signed_statusCondition = [["*" for _ in range(32)] for _ in range(self.__msgRounds)]

    def save_variable(self, s):
        temp = s
        if temp not in self.__declare:
            self.__declare.append(temp)
        return s

    """检查赋值是否重复"""

    def check_assign(self, s):
        if s not in self.__assign:
            self.__assign.append(s)

    def right_shift(self, order, num):
        return order[num:] + order[:num]

    def left_shift(self, order, num):
        return order[-num:] + order[:-num]

    def xor_function(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                     out_var_d, in_var_0, in_var_1, in_var_2):
        maxor = [[0, -1, 0, -1, 0, -1, 0, 1, 0, 0, 0, -2],
                 [0, -1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, -1, -1, -1, -1, -3],
                 [0, 0, 0, 0, 0, 0, -1, 0, -1, -1, 1, -2],
                 [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, -1, 0, -1, 1, -1, -2],
                 [0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, -1, 0, 1, 1, 1, 0],
                 [0, 0, 1, -1, 0, 0, 0, 0, 0, -1, 0, -1],
                 [0, 0, 0, 0, 0, 0, -1, 0, 1, -1, -1, -2],
                 [0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, -1, 0, 1, 0, 1, 0, 0, 0, 0],
                 [0, -1, 0, -1, 0, 1, 0, -1, 0, 0, 0, -2],
                 [0, 1, 0, -1, 0, -1, 0, -1, 0, 0, 0, -2],
                 [0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, -1, 1, -1, 1, -1],
                 [0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0],
                 [1, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1],
                 [0, -1, 0, 1, 0, -1, 0, -1, 0, 0, 0, -2],
                 [0, 0, 0, 0, 0, 0, 1, -1, -1, 1, 1, -1],
                 [0, 0, 0, 0, 1, -1, 0, 0, 0, 0, -1, -1],
                 [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, -1, 1, 1, -1, -1],
                 [0, 1, 0, 1, 0, -1, 0, 1, 0, 0, 0, 0]]
        eqn = ""
        for i in range(len(maxor)):
            for j in range(self.__block_size):
                eqn += (
                    f"{maxor[i][0]} {self.save_variable(in_var_v_0[j])} + "
                    f"{maxor[i][1]} {self.save_variable(in_var_d_0[j])} + "
                    f"{maxor[i][2]} {self.save_variable(in_var_v_1[j])} + "
                    f"{maxor[i][3]} {self.save_variable(in_var_d_1[j])} + "
                    f"{maxor[i][4]} {self.save_variable(in_var_v_2[j])} + "
                    f"{maxor[i][5]} {self.save_variable(in_var_d_2[j])} + "
                    f"{maxor[i][6]} {self.save_variable(out_var_v[j])} + "
                    f"{maxor[i][7]} {self.save_variable(out_var_d[j])} + "
                    f"{maxor[i][8]} {self.save_variable(in_var_0[j])} + "
                    f"{maxor[i][9]} {self.save_variable(in_var_1[j])} + "
                    f"{maxor[i][10]} {self.save_variable(in_var_2[j])} >= {maxor[i][11]}\n")
        self.__constraints.append(eqn)

    def if_function(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v, out_var_d,
                    in_var_0, in_var_1, in_var_2):
        maif = [[-1, 0, 0, 0, 0, 1, 1, -1, 0, 0, 1, -1],
                [0, -1, 0, -1, 0, 0, 0, 1, 1, 1, 1, -1],
                [0, -1, 0, 1, 0, 0, 0, -1, 1, 1, 1, -1],
                [0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0],
                [0, -1, 0, 1, 0, 0, 0, 1, 1, -1, 1, -1],
                [-1, 0, 0, 0, 1, -1, -1, 0, 0, 0, 0, -2],
                [1, -1, 0, 1, 0, 0, -1, 0, 0, -1, 0, -2],
                [1, 0, 0, 1, 0, 0, 0, -1, -1, 0, 0, -1],
                [1, -1, 0, 1, 0, 0, 0, 1, 0, 1, -1, -1],
                [0, -1, -1, 0, 0, 0, 0, 1, 1, 0, -1, -2],
                [0, 0, 0, 0, 1, -1, 0, 0, 0, 0, -1, -1],
                [0, 0, 0, 0, 0, 0, 1, -1, -1, -1, 0, -2],
                [-1, 0, 0, 0, -1, 0, 0, 1, 0, -1, 0, -2],
                [-1, 0, 0, 0, 1, 0, -1, 0, 0, 0, -1, -2],
                [-1, 0, 0, 0, 0, 1, 0, 1, 0, -1, 1, -1],
                [0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [1, 0, 0, -1, 0, 0, 0, 1, -1, 0, 0, -1],
                [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, -1, 0, -1, 1, 0, -1],
                [0, 0, 0, 0, 0, 0, 1, -1, 1, 0, -1, -1],
                [0, -1, 0, 0, -1, 0, 1, -1, 0, 0, 0, -2],
                [0, -1, 1, -1, 0, 0, -1, 0, 0, 0, 0, -2],
                [0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0],
                [0, 0, 1, -1, 0, 0, 0, 0, 0, -1, 0, -1],
                [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0],
                [-1, 0, 0, 0, 0, -1, 0, 1, 0, 1, 1, -1],
                [1, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1],
                [-1, 0, 0, 0, 0, 1, 0, 1, 0, 1, -1, -1],
                [0, 1, 0, 0, 0, 1, 0, -1, 1, 0, 0, 0],
                [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, -1, -1, 0, 0, 0, 1, -1, 0, 0, 0, -2],
                [0, 1, 0, 0, 0, -1, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, -1, 0, 1, 0, 1, 0],
                [0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
        eqn = ""
        for i in range(len(maif)):
            for j in range(self.__block_size):
                eqn += (
                    f"{maif[i][0]} {self.save_variable(in_var_v_0[j])} + "
                    f"{maif[i][1]} {self.save_variable(in_var_d_0[j])} + "
                    f"{maif[i][2]} {self.save_variable(in_var_v_1[j])} + "
                    f"{maif[i][3]} {self.save_variable(in_var_d_1[j])} + "
                    f"{maif[i][4]} {self.save_variable(in_var_v_2[j])} + "
                    f"{maif[i][5]} {self.save_variable(in_var_d_2[j])} + "
                    f"{maif[i][6]} {self.save_variable(out_var_v[j])} + "
                    f"{maif[i][7]} {self.save_variable(out_var_d[j])} + "
                    f"{maif[i][8]} {self.save_variable(in_var_0[j])} + "
                    f"{maif[i][9]} {self.save_variable(in_var_1[j])} + "
                    f"{maif[i][10]} {self.save_variable(in_var_2[j])} >= {maif[i][11]}\n")
        self.__constraints.append(eqn)

    def maj_function(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v, out_var_d,
                     in_var_0, in_var_1, in_var_2):
        eqn = ""
        mamaj = [[0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [-1, 0, 0, 0, 0, 1, 1, -1, 0, 0, 0, -1],
                 [0, 0, 0, 1, 0, -1, -1, 0, 0, 0, 1, -1],
                 [0, 0, 0, -1, 0, -1, 0, 1, 0, 1, 1, -1],
                 [0, 1, 0, 0, 1, 0, -1, 0, -1, 0, -1, -2],
                 [1, -1, 0, 0, 1, -1, 0, 1, 0, 0, 0, -1],
                 [0, 0, 0, 1, -1, 0, 1, 0, -1, 1, 0, -1],
                 [0, 0, 0, 0, 1, -1, 0, 0, 0, 0, -1, -1],
                 [0, -1, 0, 0, 1, 0, -1, 0, 1, 0, 0, -1],
                 [0, 0, 0, -1, 1, 0, 0, 1, 1, 1, -1, -1],
                 [0, 0, 0, 0, 0, 0, 1, -1, -1, 0, -1, -2],
                 [-1, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0, -1],
                 [0, 1, 0, 0, -1, 0, 1, -1, 0, 0, 0, -1],
                 [1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 1, -1],
                 [1, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1],
                 [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, 0, -2],
                 [0, -1, 1, 0, 0, 1, 0, 1, 0, -1, 1, -1],
                 [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, -1, 1, 0, -1, 0, 0, 0, 0, -1],
                 [1, 0, 1, -1, 0, 0, -1, 0, 0, 0, 0, -1],
                 [0, 1, 0, 0, 0, 1, 0, -1, 1, 0, 1, 0],
                 [0, 0, 1, -1, 0, 0, 0, 0, 0, -1, 0, -1],
                 [0, 1, -1, 0, 0, 0, 1, 0, 1, 0, -1, -1],
                 [0, 1, 0, 0, 1, -1, 0, 1, -1, 1, 0, -1],
                 [0, -1, 0, 1, 0, 1, 0, 1, 0, 1, -1, -1],
                 [1, -1, 1, 0, 0, 0, -1, 0, 0, 0, 0, -1],
                 [0, 0, 0, 1, 1, 0, -1, 0, 0, -1, -1, -2],
                 [0, 0, -1, 0, 0, 1, 1, -1, 0, 0, 0, -1],
                 [0, 1, 0, 0, -1, 0, 1, 0, 1, -1, 0, -1],
                 [0, 0, 0, 1, 1, -1, 0, 1, 1, -1, 0, -1],
                 [0, -1, 0, -1, 0, 0, 0, 1, 1, 1, 0, -1],
                 [0, 0, 0, 1, -1, 0, 1, -1, 0, 0, 0, -1],
                 [-1, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, -1],
                 [0, 0, 0, 1, 0, 1, 0, -1, 0, 1, 1, 0],
                 [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, -1, 0, -1, -1, -2],
                 [0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 0, 0, -1, 0, 1, 0, 1, -1, 0, 1, -1],
                 [-1, 0, 0, 1, 0, 0, 1, -1, 0, 0, 0, -1],
                 [0, 0, -1, 0, -1, 0, 1, 0, 0, 0, 0, -1],
                 [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, -1, 0, 0, 0, 1, -1, 0, 0, 0, -1],
                 [0, 1, 0, 1, 0, 0, 0, -1, 1, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0]]
        eqn = ""
        for i in range(len(mamaj)):
            for j in range(self.__block_size):
                eqn += (
                    f"{mamaj[i][0]} {self.save_variable(in_var_v_0[j])} + "
                    f"{mamaj[i][1]} {self.save_variable(in_var_d_0[j])} + "
                    f"{mamaj[i][2]} {self.save_variable(in_var_v_1[j])} + "
                    f"{mamaj[i][3]} {self.save_variable(in_var_d_1[j])} + "
                    f"{mamaj[i][4]} {self.save_variable(in_var_v_2[j])} + "
                    f"{mamaj[i][5]} {self.save_variable(in_var_d_2[j])} + "
                    f"{mamaj[i][6]} {self.save_variable(out_var_v[j])} + "
                    f"{mamaj[i][7]} {self.save_variable(out_var_d[j])} + "
                    f"{mamaj[i][8]} {self.save_variable(in_var_0[j])} + "
                    f"{mamaj[i][9]} {self.save_variable(in_var_1[j])} + "
                    f"{mamaj[i][10]} {self.save_variable(in_var_2[j])} >= {mamaj[i][11]}\n")
        self.__constraints.append(eqn)

    def expand_model(self, in_var_v, in_var_d, c_var_v, c_var_d, out_var_v, out_var_d, flag):
        ma1 = [[0, 1, 0, 1, 0, -1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, -1, 1, 0],
               [0, 0, -1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, -1, 1, 0, 0, 0],
               [0, -1, 0, -1, 0, -1, 0, 0, -2],
               [0, 1, 0, -1, 0, 1, 0, 0, 0],
               [0, 0, -1, 0, 0, 0, 1, -1, -1],
               [-1, 0, 1, 0, 0, 1, 0, -1, -1],
               [-1, 0, 0, 0, -1, 0, 0, -1, -2],
               [1, -1, 0, 0, 0, 0, -1, 0, -1],
               [-1, 0, 0, -1, 0, -1, 0, 0, -2],
               [0, 1, 1, 0, 1, 0, 0, -1, 0],
               [0, 0, 0, 0, -1, 0, -1, 0, -1],
               [0, 0, 0, 1, 1, 0, 1, -1, 0],
               [-1, 0, 0, 1, 1, 0, 0, 1, 0],
               [1, 0, 1, 0, -1, 0, 0, 1, 0],
               [1, -1, 1, 0, 0, 1, 0, 1, 0],
               [-1, 0, -1, 0, 0, 0, 0, 1, -1],
               [0, 0, -1, 0, 1, -1, 0, 1, -1]]
        ma0 = [[0, 1, 0, -1, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, -1, 1, 0, 0, 0],
               [0, 0, -1, 0, 0, 0, -1, 0, -1],
               [0, 0, -1, 1, 0, 0, 0, 0, 0],
               [0, -1, 0, -1, 0, -1, 0, 0, -2],
               [0, 0, 0, 0, 0, 0, -1, 1, 0],
               [0, 1, 0, 1, 0, -1, 0, 0, 0],
               [1, 0, 0, 1, 0, 0, -1, 0, 0],
               [0, 0, 0, 0, -1, 0, 1, -1, -1],
               [-1, 1, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, -1, 1, 0, 0, -1, -1],
               [-1, 0, 0, 1, 1, 0, 0, -1, -1],
               [0, 0, 1, 0, 0, 1, 1, -1, 0],
               [-1, 0, 1, 0, 0, 1, 0, 1, 0],
               [1, 0, -1, 0, 1, 0, 0, 1, 0],
               [1, -1, 0, 1, 1, 0, 0, 1, 0],
               [-1, 0, 0, 0, -1, 0, 0, 1, -1],
               [0, 0, 1, -1, -1, 0, 0, 1, -1],
               [-1, 0, 0, 0, 0, 0, 1, -1, -1]]
        eqn = "%s = 0\n%s = 0\n" % (c_var_v[0], c_var_d[0])
        if flag == 1:
            for i in range(len(ma1)):
                for j in range(self.__block_size):
                    eqn += (
                        f"{ma1[i][0]} {self.save_variable(in_var_v[j])} + "
                        f"{ma1[i][1]} {self.save_variable(in_var_d[j])} + "
                        f"{ma1[i][2]} {self.save_variable(c_var_v[j])} + "
                        f"{ma1[i][3]} {self.save_variable(c_var_d[j])} + "
                        f"{ma1[i][4]} {self.save_variable(out_var_v[j])} + "
                        f"{ma1[i][5]} {self.save_variable(out_var_d[j])} + "
                        f"{ma1[i][6]} {self.save_variable(c_var_v[j + 1])} + "
                        f"{ma1[i][7]} {self.save_variable(c_var_d[j + 1])} >= "
                        f"{ma1[i][8]}\n")
        else:
            for i in range(len(ma0)):
                for j in range(self.__block_size):
                    eqn += (
                        f"{ma0[i][0]} {self.save_variable(out_var_v[j])} + "
                        f"{ma0[i][1]} {self.save_variable(out_var_d[j])} + "
                        f"{ma0[i][2]} {self.save_variable(in_var_v[j])} + "
                        f"{ma0[i][3]} {self.save_variable(in_var_d[j])} + "
                        f"{ma0[i][4]} {self.save_variable(c_var_v[j])} + "
                        f"{ma0[i][5]} {self.save_variable(c_var_d[j])} + "
                        f"{ma0[i][6]} {self.save_variable(c_var_v[j + 1])} + "
                        f"{ma0[i][7]} {self.save_variable(c_var_d[j + 1])} >= "
                        f"{ma0[i][8]} \n")
        self.__constraints.append(eqn)

    def modadd_model(self, in_var_v_0, in_var_d_0,
                     in_var_v_1, in_var_d_1,
                     in_var_c_v, in_var_c_d,
                     out_var_v, out_var_d):
        ma = [[0, 1, 0, 1, 0, 1, 0, -1, 0, 0, 0],
              [0, -1, 0, -1, 0, -1, 0, 1, 0, 0, -2],
              [0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0],
              [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0],
              [-1, 0, 0, 0, 0, 0, 0, 0, 1, -1, -1],
              [1, 0, -1, 0, 1, 0, 0, 0, 0, -1, -1],
              [0, 0, 1, 0, 1, 0, 0, 0, -1, 0, 0],
              [0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0],
              [1, 0, 0, 0, 1, -1, -1, 0, 0, 0, -1],
              [0, 0, 1, -1, 1, 0, -1, 0, 0, 0, -1],
              [1, 0, 1, 0, -1, 0, 0, 0, 0, -1, -1],
              [0, -1, 0, 1, 0, -1, 0, -1, 0, 0, -2],
              [0, -1, -1, 0, 0, 1, 0, -1, 0, 0, -2],
              [0, 1, 0, -1, 0, -1, 0, -1, 0, 0, -2],
              [0, -1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
              [1, -1, 1, 0, 0, 0, -1, 0, 0, 0, -1],
              [0, 0, -1, 0, -1, 0, 1, 0, 1, 0, -1],
              [0, 1, 0, 1, 0, 0, 0, 0, 0, -1, 0],
              [1, 0, 0, 0, 0, 0, -1, 0, 0, -1, -1],
              [1, -1, 1, -1, 1, 0, 0, 0, 0, 1, -1],
              [0, 0, 0, 0, 0, 0, 1, -1, -1, 0, -1],
              [1, 0, 1, 0, 1, -1, 0, 1, 0, 1, 0],
              [0, 0, 0, 0, 0, 1, 0, -1, 0, -1, -1],
              [-1, 0, 0, 0, -1, 0, 1, 0, 0, 1, -1],
              [-1, 0, -1, 0, 0, 0, 1, 0, 0, 1, -1],
              [0, 1, -1, 0, 0, 1, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, -1, 0, 0, -1, -1],
              [0, 0, 0, 0, 1, 0, -1, 0, 0, -1, -1],
              [-1, 0, 0, 0, 0, 1, 1, -1, 0, 0, -1],
              [0, 1, 0, -1, 0, 1, 0, 1, 0, 0, 0],
              [0, 1, 0, 1, -1, 0, 1, 0, 0, 0, 0],
              [-1, 0, -1, 0, -1, 0, 0, 0, 0, 1, -2]]
        eqn = "%s = 0\n%s = 0\n" % (in_var_c_v[0], in_var_c_d[0])
        for i in range(len(ma)):
            for j in range(self.__block_size):
                eqn += (
                    f"{ma[i][0]} {self.save_variable(in_var_v_0[j])} + "
                    f"{ma[i][1]} {self.save_variable(in_var_d_0[j])} + "
                    f"{ma[i][2]} {self.save_variable(in_var_v_1[j])} + "
                    f"{ma[i][3]} {self.save_variable(in_var_d_1[j])} + "
                    f"{ma[i][4]} {self.save_variable(in_var_c_v[j])} + "
                    f"{ma[i][5]} {self.save_variable(in_var_c_d[j])} + "
                    f"{ma[i][6]} {self.save_variable(out_var_v[j])} + "
                    f"{ma[i][7]} {self.save_variable(out_var_d[j])} + "
                    f"{ma[i][8]} {self.save_variable(in_var_c_v[j + 1])} + "
                    f"{ma[i][9]} {self.save_variable(in_var_c_d[j + 1])} >= {ma[i][10]} \n")
        self.__constraints.append(eqn)

    def R(self, in_var_v_m, in_var_d_m, in_var_v_a0, in_var_d_a0, in_var_v_a1, in_var_d_a1, in_var_v_a2,
          in_var_d_a2,
          in_var_v_a3, in_var_d_a3, in_var_v_a4, in_var_d_a4, in_var_v_e0, in_var_d_e0, in_var_v_e1, in_var_d_e1,
          in_var_v_e2, in_var_d_e2, in_var_v_e3, in_var_d_e3, in_var_v_e4, in_var_d_e4, in_var_a0, in_var_a1,
          in_var_a2,
          in_var_a3, in_var_e0, in_var_e1, in_var_e2, in_var_e3, step):
        # Claim signed difference vectors ∇b0,∇b1,∇b2,∇b3 of size 32,let a reputation b0, b1,b2,b3
        in_var_v_b = []
        in_var_d_b = []
        for i in range(10):
            temp_b_v = []
            temp_b_d = []
            for j in range(self.__block_size):
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
            for j in range(self.__block_size+1):
                temp_c_v.append("cv" + str(i) + "_" + str(step) + "_" + str(j))
                temp_c_d.append("cd" + str(i) + "_" + str(step) + "_" + str(j))

            in_var_v_c.append(temp_c_v)
            in_var_d_c.append(temp_c_d)

        self.xor_function(self.right_shift(in_var_v_e3, self.__status_i4),
                          self.right_shift(in_var_d_e3, self.__status_i4),
                          self.right_shift(in_var_v_e3, self.__status_i5),
                          self.right_shift(in_var_d_e3, self.__status_i5),
                          self.right_shift(in_var_v_e3, self.__status_i6),
                          self.right_shift(in_var_d_e3, self.__status_i6),
                          in_var_v_b[0], in_var_d_b[0],
                          self.right_shift(in_var_e3, self.__status_i4),
                          self.right_shift(in_var_e3, self.__status_i5),
                          self.right_shift(in_var_e3, self.__status_i6))

        self.if_function(in_var_v_e3, in_var_d_e3,
                         in_var_v_e2, in_var_d_e2,
                         in_var_v_e1, in_var_d_e1,
                         in_var_v_b[1], in_var_d_b[1],
                         in_var_e3,
                         in_var_e2,
                         in_var_e1)

        self.modadd_model(in_var_v_e0, in_var_d_e0,
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
        # computer Ei
        self.modadd_model(in_var_v_a0, in_var_d_a0,
                          in_var_v_b[4], in_var_d_b[4],
                          in_var_v_c[3], in_var_d_c[3],
                          in_var_v_b[5], in_var_d_b[5])

        if step > self.__staRounds - 5:
            self.expand_model(in_var_v_b[5], in_var_d_b[5],
                              in_var_v_c[4], in_var_d_c[4],
                              in_var_v_e4, in_var_d_e4, 0)
        else:
            self.expand_model(in_var_v_b[5], in_var_d_b[5],
                              in_var_v_c[4], in_var_d_c[4],
                              in_var_v_e4, in_var_d_e4, 1)

        # computer Ai
        self.xor_function(self.right_shift(in_var_v_a3, self.__status_i1),
                          self.right_shift(in_var_d_a3, self.__status_i1),
                          self.right_shift(in_var_v_a3, self.__status_i2),
                          self.right_shift(in_var_d_a3, self.__status_i2),
                          self.right_shift(in_var_v_a3, self.__status_i3),
                          self.right_shift(in_var_d_a3, self.__status_i3),
                          in_var_v_b[6], in_var_d_b[6],
                          self.right_shift(in_var_a3, self.__status_i1),
                          self.right_shift(in_var_a3, self.__status_i2),
                          self.right_shift(in_var_a3, self.__status_i3))

        self.maj_function(in_var_v_a3, in_var_d_a3,
                          in_var_v_a2, in_var_d_a2,
                          in_var_v_a1, in_var_d_a1,
                          in_var_v_b[7], in_var_d_b[7],
                          in_var_a3,
                          in_var_a2,
                          in_var_a1)

        self.modadd_model(in_var_v_b[4], in_var_d_b[4],
                          in_var_v_b[6], in_var_d_b[6],
                          in_var_v_c[5], in_var_d_c[5],
                          in_var_v_b[8], in_var_d_b[8])

        self.modadd_model(in_var_v_b[8], in_var_d_b[8],
                          in_var_v_b[7], in_var_d_b[7],
                          in_var_v_c[6], in_var_d_c[6],
                          in_var_v_b[9], in_var_d_b[9])

        if step > self.__staRounds - 9:
            self.expand_model(in_var_v_b[9], in_var_d_b[9],
                              in_var_v_c[7], in_var_d_c[7],
                              in_var_v_a4, in_var_d_a4, 0)
        else:
            self.expand_model(in_var_v_b[9], in_var_d_b[9],
                              in_var_v_c[7], in_var_d_c[7],
                              in_var_v_a4, in_var_d_a4, 1)

    def message_expand(self, in_var_v_w0, in_var_d_w0, in_var_v_w1, in_var_d_w1, in_var_v_w2, in_var_d_w2,
                       in_var_v_w3, in_var_d_w3, in_var_w0, in_var_w2, in_var_v_w4, in_var_d_w4, step):
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

        for i in range(self.__block_size):
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
        for i in range(self.__block_size+1):
            in_var_v_c0.append("mcv0" + "_" + str(step) + "_" + str(i))
            in_var_d_c0.append("mcd0" + "_" + str(step) + "_" + str(i))
            in_var_v_c1.append("mcv1" + "_" + str(step) + "_" + str(i))
            in_var_d_c1.append("mcd1" + "_" + str(step) + "_" + str(i))
            in_var_v_c2.append("mcv2" + "_" + str(step) + "_" + str(i))
            in_var_d_c2.append("mcd2" + "_" + str(step) + "_" + str(i))
            in_var_v_c3.append("mcv3" + "_" + str(step) + "_" + str(i))
            in_var_d_c3.append("mcd3" + "_" + str(step) + "_" + str(i))
        # replace shift variable
        temp_v0 = []
        temp_d0 = []
        temp_v1 = []
        temp_d1 = []
        temp_0 = []
        temp_1 = []
        for i in range(self.__msg_i6):
            temp_v0.append("temp0v" + "_" + str(step) + "_" + str(i))
            temp_d0.append("temp0d" + "_" + str(step) + "_" + str(i))
            temp_0.append("temp0" + "_" + str(step) + "_" + str(i))
        for i in range(self.__msg_i3):
            temp_v1.append("temp1v" + "_" + str(step) + "_" + str(i))
            temp_d1.append("temp1d" + "_" + str(step) + "_" + str(i))
            temp_1.append("temp1" + "_" + str(step) + "_" + str(i))
        for i in range(self.__msg_i6):
            temp = "%s = 0\n" % ("temp0v" + "_" + str(step) + "_" + str(i))
            temp += "%s = 0\n" % ("temp0d" + "_" + str(step) + "_" + str(i))
            temp += "%s = 0\n" % ("temp0" + "_" + str(step) + "_" + str(i))
            self.__constraints.append(temp)
        for i in range(self.__msg_i3):
            temp = "%s = 0\n" % ("temp1v" + "_" + str(step) + "_" + str(i))
            temp += "%s = 0\n" % ("temp1d" + "_" + str(step) + "_" + str(i))
            temp += "%s = 0\n" % ("temp1" + "_" + str(step) + "_" + str(i))
            self.__constraints.append(temp)

        # print(len(self.right_shift(in_var_v_w2, 3)[:29] + temp_v1))

        self.xor_function(self.right_shift(in_var_v_w0, self.__msg_i4), self.right_shift(in_var_d_w0, self.__msg_i4),
                          self.right_shift(in_var_v_w0, self.__msg_i5), self.right_shift(in_var_d_w0, self.__msg_i5),
                          self.right_shift(in_var_v_w0, self.__msg_i6)[:self.__block_size - self.__msg_i6] + temp_v0,
                          self.right_shift(in_var_d_w0, self.__msg_i6)[:self.__block_size - self.__msg_i6] + temp_d0,
                          in_var_v_b0, in_var_d_b0,
                          self.right_shift(in_var_w0, self.__msg_i4),
                          self.right_shift(in_var_w0, self.__msg_i5),
                          self.right_shift(in_var_w0, self.__msg_i6)[:self.__block_size - self.__msg_i6] + temp_0)
        self.modadd_model(in_var_v_b0, in_var_d_b0,
                          in_var_v_w1, in_var_d_w1,
                          in_var_v_c0, in_var_d_c0,
                          in_var_v_b1, in_var_d_b1)
        self.xor_function(self.right_shift(in_var_v_w2, self.__msg_i1), self.right_shift(in_var_d_w2, self.__msg_i1),
                          self.right_shift(in_var_v_w2, self.__msg_i2), self.right_shift(in_var_d_w2, self.__msg_i2),
                          self.right_shift(in_var_v_w2, self.__msg_i3)[:self.__block_size - self.__msg_i3] + temp_v1,
                          self.right_shift(in_var_d_w2, self.__msg_i3)[:self.__block_size - self.__msg_i3] + temp_d1,
                          in_var_v_b2, in_var_d_b2,
                          self.right_shift(in_var_w2, self.__msg_i1),
                          self.right_shift(in_var_w2, self.__msg_i2),
                          self.right_shift(in_var_w2, self.__msg_i3)[:self.__block_size - self.__msg_i3] + temp_1)
        self.modadd_model(in_var_v_b1, in_var_d_b1,
                          in_var_v_b2, in_var_d_b2,
                          in_var_v_c1, in_var_d_c1,
                          in_var_v_b3, in_var_d_b3)
        self.modadd_model(in_var_v_b3, in_var_d_b3,
                          in_var_v_w3, in_var_d_w3,
                          in_var_v_c2, in_var_d_c2,
                          in_var_v_b4, in_var_d_b4)
        self.expand_model(in_var_v_b4, in_var_d_b4, in_var_v_c3, in_var_d_c3, in_var_v_w4, in_var_d_w4, 0)

    def assignMsgValue(self):
        temp = ""
        for i in range(self.__msgRounds):
            for j in range(self.__block_size):
                if i == self.__msgRounds - 1 and j == self.__block_size-1:
                    temp += "wd_" + str(i) + "_" + str(j) + " >= 1\n"
                else:
                    temp += "wd_" + str(i) + "_" + str(j) + " + "
        self.__constraints.append(temp)

        for i in range(18, self.__msgRounds):
            for j in range(self.__block_size):
                temp = "%s = 0\n" % (self.save_variable("wv_" + str(i) + "_" + str(31 - j)))
                temp += "%s = 0\n" % (self.save_variable("wd_" + str(i) + "_" + str(31 - j)))
                self.__constraints.append(temp)
        for i in range(0, 7):
            for j in range(self.__block_size):
                temp = "%s = 0\n" % (self.save_variable("wv_" + str(i) + "_" + str(31 - j)))
                temp += "%s = 0\n" % (self.save_variable("wd_" + str(i) + "_" + str(31 - j)))
                self.__constraints.append(temp)
        for i in range(9, 12):
            for j in range(self.__block_size):
                temp = "%s = 0\n" % (self.save_variable("wv_" + str(i) + "_" + str(31 - j)))
                temp += "%s = 0\n" % (self.save_variable("wd_" + str(i) + "_" + str(31 - j)))
                self.__constraints.append(temp)
        for i in range(13, 15):
            for j in range(self.__block_size):
                temp = "%s = 0\n" % (self.save_variable("wv_" + str(i) + "_" + str(31 - j)))
                temp += "%s = 0\n" % (self.save_variable("wd_" + str(i) + "_" + str(31 - j)))
                self.__constraints.append(temp)
        for i in range(16, 17):
            for j in range(self.__block_size):
                temp = "%s = 0\n" % (self.save_variable("wv_" + str(i) + "_" + str(31 - j)))
                temp += "%s = 0\n" % (self.save_variable("wd_" + str(i) + "_" + str(31 - j)))
                self.__constraints.append(temp)
        ssw = ["========un==u=nuuuuu==nu=n===n==",
               "=====u==n===n=========nn========",
               "================================",
               "================================",
               "================================",
               "==========u=======n===u==n=n==nn",
               "================================",
               "================================",
               "=u==nn=n=u==u=====un=uu==u===u==",
               "================================",
               "======nnn===u=========uu========"]
        for step in range(len(ssw)):
            for i in range(self.__block_size):
                if ssw[step][i] == "u":
                    temp = "%s = 1\n" % (self.save_variable("wv_" + str(step + 7) + "_" + str(31 - i)))
                    temp += "%s = 1\n" % (self.save_variable("wd_" + str(step + 7) + "_" + str(31 - i)))
                    self.__constraints.append(temp)
                elif ssw[step][i] == "n":
                    temp = "%s = 0\n" % (self.save_variable("wv_" + str(step + 7) + "_" + str(31 - i)))
                    temp += "%s = 1\n" % (self.save_variable("wd_" + str(step + 7) + "_" + str(31 - i)))
                    self.__constraints.append(temp)
                else:
                    temp = "%s = 0\n" % (self.save_variable("wd_" + str(step + 7) + "_" + str(31 - i)))
                    self.__constraints.append(temp)

    def assignEAValue(self):

        for step in range(self.__startRounds - 4, self.__startRounds):
            for i in range(self.__block_size):
                temp = "xv_" + str(step) + "_" + str(i) + " = 0\n"
                temp += "xd_" + str(step) + "_" + str(i) + " = 0\n"
                temp += "yv_" + str(step) + "_" + str(i) + " = 0\n"
                temp += "yd_" + str(step) + "_" + str(i) + " = 0\n"
                self.__constraints.append(temp)
        for step in range(self.__staRounds - 8, self.__staRounds):
            for i in range(self.__block_size):
                temp = "xv_" + str(step) + "_" + str(i) + " = 0\n"
                temp += "xd_" + str(step) + "_" + str(i) + " = 0\n"
                self.__constraints.append(temp)
        for step in range(self.__staRounds - 4, self.__staRounds):
            for i in range(self.__block_size):
                temp = "yv_" + str(step) + "_" + str(i) + " = 0\n"
                temp += "yd_" + str(step) + "_" + str(i) + " = 0\n"
                self.__constraints.append(temp)
        ssa = ["=======unn==u======n===nn=uuuu==",
               "nnnnn=nnnn========nuu===========",
               "====un==n==nu=======nu=u========"]
        for step in range(len(ssa)):
            for i in range(self.__block_size):
                if ssa[step][i] == "u":
                    temp = "%s = 1\n" % (self.save_variable("xv_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    temp += "%s = 1\n" % (self.save_variable("xd_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    self.__constraints.append(temp)
                elif ssa[step][i] == "n":
                    temp = "%s = 0\n" % (self.save_variable("xv_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    temp += "%s = 1\n" % (self.save_variable("xd_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    self.__constraints.append(temp)
                else:
                    temp = "%s = 0\n" % (self.save_variable("xd_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    self.__constraints.append(temp)
        sse = ["=========u==u===nuu=uuuu=n===n==",
               "=n=n======u==u=n==un===n==n=====",
               "==n=n====u======nn===u========u=",
               "u=====nuuu==uun==u==n==n====u=u=",
               "=n===uuuuu========n=uun==n===n==",
               "=========u==u===================",
               "=====u=nunuuu=========nn========"]
        for step in range(len(sse)):
            for i in range(self.__block_size):
                if sse[step][i] == "u":
                    temp = "%s = 1\n" % (self.save_variable("yv_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    temp += "%s = 1\n" % (self.save_variable("yd_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    self.__constraints.append(temp)
                elif sse[step][i] == "n":
                    temp = "%s = 0\n" % (self.save_variable("yv_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    temp += "%s = 1\n" % (self.save_variable("yd_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    self.__constraints.append(temp)
                else:
                    temp = "%s = 0\n" % (self.save_variable("yd_" + str(step + 7) + "_" + str(self.__block_size-1 - i)))
                    self.__constraints.append(temp)

    def bilidRoundModel(self):
        in_var_v_a = []
        in_var_d_a = []
        in_var_v_e = []
        in_var_d_e = []
        in_var_a = []
        in_var_e = []
        in_var_v_w = []
        in_var_d_w = []
        in_var_w = []
        for step in range(0, self.__staRounds):
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
        for step in range(0, self.__staRounds):
            temp_v_e = []
            temp_d_e = []
            temp_e = []
            for i in range(self.__block_size):
                temp_v_e.append("yv_" + str(step) + "_" + str(i))
                temp_d_e.append("yd_" + str(step) + "_" + str(i))
                temp_e.append("y_" + str(step) + "_" + str(i))
            in_var_v_e.append(temp_v_e)
            in_var_d_e.append(temp_d_e)
            in_var_e.append(temp_e)

        for step in range(0, self.__msgRounds):
            temp_v_w = []
            temp_d_w = []
            temp_w = []
            for i in range(self.__block_size):
                temp_v_w.append("wv_" + str(step) + "_" + str(i))
                temp_d_w.append("wd_" + str(step) + "_" + str(i))
                temp_w.append("w_" + str(step) + "_" + str(i))
            in_var_v_w.append(temp_v_w)
            in_var_d_w.append(temp_d_w)
            in_var_w.append(temp_w)

        for i in range(self.__startRounds, self.__staRounds):
            self.R(in_var_v_w[i], in_var_d_w[i], in_var_v_a[i - 4], in_var_d_a[i - 4],
                   in_var_v_a[i - 3], in_var_d_a[i - 3], in_var_v_a[i - 2], in_var_d_a[i - 2],
                   in_var_v_a[i - 1], in_var_d_a[i - 1], in_var_v_a[i], in_var_d_a[i],
                   in_var_v_e[i - 4], in_var_d_e[i - 4], in_var_v_e[i - 3], in_var_d_e[i - 3],
                   in_var_v_e[i - 2], in_var_d_e[i - 2], in_var_v_e[i - 1], in_var_d_e[i - 1],
                   in_var_v_e[i], in_var_d_e[i], in_var_a[i - 4], in_var_a[i - 3], in_var_a[i - 2], in_var_a[i - 1],
                   in_var_e[i - 4], in_var_e[i - 3], in_var_e[i - 2], in_var_e[i - 1],
                   i)

    def bilidMsgModel(self):
        in_var_v_w = []
        in_var_d_w = []
        in_var_w = []

        for step in range(0, self.__msgRounds):
            temp_v_w = []
            temp_d_w = []
            temp_w = []
            for i in range(self.__block_size):
                temp_v_w.append("wv_" + str(step) + "_" + str(i))
                temp_d_w.append("wd_" + str(step) + "_" + str(i))
                temp_w.append("w_" + str(step) + "_" + str(i))
            in_var_v_w.append(temp_v_w)
            in_var_d_w.append(temp_d_w)
            in_var_w.append(temp_w)
        for i in range(self.__msgRounds):
            if i > 15:
                self.message_expand(in_var_v_w[i - 2], in_var_d_w[i - 2],
                                    in_var_v_w[i - 7], in_var_d_w[i - 7],
                                    in_var_v_w[i - 15], in_var_d_w[i - 15],
                                    in_var_v_w[i - 16], in_var_d_w[i - 16],
                                    in_var_w[i - 2], in_var_w[i - 15],
                                    in_var_v_w[i], in_var_d_w[i], i)

    def objMsg(self):
        temp = ""
        for i in range(self.__msgRounds):
            for j in range(self.__block_size):
                if i == self.__msgRounds - 1 and j == self.__block_size-1:
                    temp += "wd_" + str(i) + "_" + str(j) + " + " + "wv_" + str(i) + "_" + str(j) + "\n"
                else:
                    temp += "wd_" + str(i) + "_" + str(j) + " + " + "wv_" + str(i) + "_" + str(j) + " + "
        self.__objective.append(temp)

    def objAStatus(self):
        temp = ""
        for i in range(self.__startRounds, self.__staRounds):
            for j in range(self.__block_size):
                if i == self.__staRounds - 1 and j == self.__block_size-1:
                    temp += "xd_" + str(i) + "_" + str(j) + "\n"
                else:
                    temp += "xd_" + str(i) + "_" + str(j) + " + "
        self.__objective.append(temp)

    def solver(self):
        self.objMsg()
        self.bilidMsgModel()
        self.assignMsgValue()
        constrain = "".join(self.__constraints)
        assign = "".join(self.__assign)
        variable = "\n".join(self.__declare)
        variable += "\nEnd"
        obj = "".join(self.__objective)
        file_write = open("right_model.lp", "w")
        file_write.write("Minimize\n" + obj)
        file_write.write("Subject To\n" + constrain)
        file_write.write(assign)
        file_write.write("Binary" + "\n" + variable)
        file_write.close()
        self.__model_msg = read("right_model.lp")

        self.__model_msg.setParam('LogToConsole', 0)
        self.__model_msg.optimize()
        if self.__model_msg.status == 2:
            for v in self.__model_msg.getVars():
                if v.VarName in obj:
                    # print(v.x, v.VarName)
                    self.__msgResult.append(v.VarName + " = " + str(int(v.x)))
            # obj = self.__model_msg.getObjective()
            # print(obj.getValue())
            # # 获取目标函数的值
            # obj = self.__model_msg.getObjective()
            # print(f"Objective function value: {obj.getValue()}")

    def solverAStatus(self):
        self.solver()
        # self.__constraints.clear()
        self.__assign.clear()
        self.__objective.clear()
        self.__declare.clear()
        self.objAStatus()
        # self.assignMsgValue()
        # self.bilidMsgModel()
        self.bilidRoundModel()
        self.assignEAValue()
        constrain = "".join(self.__constraints)
        assign = "".join(self.__assign)
        assign += "\n".join(self.__msgResult)
        variable = "\n".join(self.__declare)
        variable += "\nEnd"
        obj = "".join(self.__objective)
        file_write = open("right_model1.lp", "w")
        file_write.write("Minimize\n" + obj)
        file_write.write("Subject To\n" + constrain)
        file_write.write(assign)
        file_write.write("\nBinary" + "\n" + variable)
        file_write.close()

        self.__model_msgEA = read("right_model1.lp")
        self.__model_msgEA.setParam('OutputFlag', 0)
        self.__model_msgEA.optimize()
        if self.__model_msgEA.status == 2:
            for v in self.__model_msgEA.getVars():
                if (
                        "wv" in v.VarName) or "wd" in v.VarName or "xv" in v.VarName or "xd" in v.VarName or "yv" in v.VarName or "yd" in v.VarName or "bv0" in v.VarName or "bd0" in v.VarName or "bv1" in v.VarName or "bd1" in v.VarName:
                    self.__result.append(v.VarName + " = " + str(int(v.x)))
            # obj = self.__model_msgEA.getObjective()
            # print(obj.getValue())
            # # 获取目标函数的值
            # obj = self.__model_msgEA.getObjective()
            # print(f"Objective function value: {obj.getValue()}")

    def clearData(self, s):
        try:
            s = re.sub(r'ASSERT\( | \);\s*|Invalid\.\n', '', s).strip()
            parts = s.split(" = ")

            if len(parts) != 2:
                raise ValueError("Unexpected format")

            col = int(parts[0].split("_")[1])
            row = int(parts[0].split("_")[2])
            value = parts[1].replace("0b", "")

            return col, row, value
        except (IndexError, ValueError):
            raise ValueError("Failed to parse data")

    def get_status_transition(self, current_status, value):
        status_mapping = {
            ("1", "1"): "u",
            ("0", "0"): "=",
            ("1", "0"): "n",
            ("0", "1"): "n"
        }
        return status_mapping.get((current_status, value))

    def process_data(self, da, signed_status, substring):
        result = self.clearData(da)
        if result:
            col, row, value = result
            current_status = signed_status[col][row]
            if current_status == "*":
                signed_status[col][row] = value
            else:
                new_status = self.get_status_transition(current_status, value)
                if new_status is not None:
                    signed_status[col][row] = new_status

    def process_results(self):
        for da in self.__result:
            if any(substring in da for substring in ["xv", "xd"]):
                self.process_data(da, self.__aState, ["xv", "xd"])
            elif any(substring in da for substring in ["yv", "yd"]):
                self.process_data(da, self.__eState, ["yv", "yd"])
            elif any(substring in da for substring in ["wv", "wd"]):
                self.process_data(da, self.__wState, ["wv", "wd"])
            elif any(substring in da for substring in ["bv1", "bd1"]):
                self.process_data(da, self.__ifE, ["bv1", "bd1"])
            elif any(substring in da for substring in ["bv0", "bd0"]):
                self.process_data(da, self.__xorE, ["bv0", "bd0"])
        self.signed_statusCondition = [row[:] for row in self.__eState]

    def add_consition(self):
        for i in range(3, len(self.__eState)):
            cin1, cin2, cin3, cin4 = ifx(self.__eState[i - 1],
                                         self.__eState[i - 2],
                                         self.__eState[i - 3],
                                         self.__ifE[i],
                                         self.signed_statusCondition[i - 1],
                                         self.signed_statusCondition[i - 2],
                                         self.signed_statusCondition[i - 3],
                                         self.signed_statusCondition[i - 4])
            self.signed_statusCondition[i - 1] = cin1
            self.signed_statusCondition[i - 2] = cin2
            self.signed_statusCondition[i - 3] = cin3
            self.signed_statusCondition[i - 4] = cin4
        for i in range(1, len(self.__eState)):
            cin1, cin2, cin3 = Exor(self.__eState[i - 1],
                                    self.__ifE[i],
                                    self.signed_statusCondition[i - 1],
                                    self.signed_statusCondition[i - 2],
                                    self.signed_statusCondition[i])
            self.signed_statusCondition[i - 1] = cin1
            self.signed_statusCondition[i - 2] = cin2
            self.signed_statusCondition[i] = cin3
        for i in range(3, len(self.__eState)):
            cin1, cin2, cin3, cin4 = ifx(self.__eState[i - 1],
                                         self.__eState[i - 2],
                                         self.__eState[i - 3],
                                         self.__ifE[i],
                                         self.signed_statusCondition[i - 1],
                                         self.signed_statusCondition[i - 2],
                                         self.signed_statusCondition[i - 3],
                                         self.signed_statusCondition[i - 4])
            self.signed_statusCondition[i - 1] = cin1
            self.signed_statusCondition[i - 2] = cin2
            self.signed_statusCondition[i - 3] = cin3
            self.signed_statusCondition[i - 4] = cin4
        for i in range(1, len(self.__eState)):
            cin1, cin2, cin3 = Exor(self.__eState[i - 1],
                                    self.__ifE[i],
                                    self.signed_statusCondition[i - 1],
                                    self.signed_statusCondition[i - 2],
                                    self.signed_statusCondition[i])
            self.signed_statusCondition[i - 1] = cin1
            self.signed_statusCondition[i - 2] = cin2
            self.signed_statusCondition[i] = cin3

    def printer(self):
        self.solverAStatus()
        self.process_results()
        self.add_consition()
        # print("=== signed_statusA ===")
        # for i in range(len(self.__aState)):
        #     row = self.__aState[i]
        #     print(f"{i:2}: {''.join(reversed(row)).replace('*', '=')}")
        #
        # # print("=== signed_statusE ===")
        # for i in range(len(self.signed_statusCondition)):
        #     row = self.signed_statusCondition[i]
        #     print(f"{i:2}: {''.join(reversed(row)).replace('*', '=')}")
        #
        # print("=== signed_statusM ===")
        # for i in range(len(self.__wState)):
        #     row = self.__wState[i]
        #     print(f"{i:2}: \"{''.join(reversed(row)).replace('*', '=')}\"")

    def save_pdf(self):
        self.printer()
        title_main = "\\documentclass{standalone}\n"
        title_main += "\\standaloneconfig{border=1pt 1pt 1pt 1pt}\n"
        title_main += "\\usepackage{graphicx} % Required for inserting images\n"
        title_main += "\\usepackage{color}\n"
        title_main += "\\usepackage{comment}\n"
        title_main += "\\usepackage{booktabs}\n"
        title_main += "\\usepackage{verbatim}\n"
        title_main += "\\usepackage{graphicx}\n"
        title_main += "\\begin{document}\n"
        title_main += "\\begin{tabular}{c|c|c|c|} \\toprule\n"
        title_main += "$i$ &$\\nabla A_i$ & $\\nabla E_i$ &  $\\nabla W_i$  \\\\ \\midrule\n"
        strNull = "================================"
        for i in range(4):
            title_main += f"$\\texttt{{{i - 4}}}$ & \\texttt{{{strNull}}} & \\texttt{{{strNull}}} & \\texttt{{}}  \\\\ \n"
        for i in range(len(self.signed_statusCondition)):
            aState = ''.join(reversed(self.__aState[i])).replace('*', '=')
            eState = ''.join(reversed(self.signed_statusCondition[i])).replace('*', '=')
            wState = ''.join(reversed(self.__wState[i])).replace('*', '=')
            title_main += f"$\\texttt{{{i}}}$ & \\texttt{{{aState}}} & \\texttt{{{eState}}} & \\texttt{{{wState}}}  \\\\ \n"
        title_main += "\\bottomrule\n"
        title_main += "\\end{tabular}\n"
        title_main += "\\end{document}\n"
        file_write = open(self.__outputFile, "w")
        file_write.write(title_main)
        file_write.close()
        # print(title_main)


if __name__ == '__main__':
    start = time.time()
    startRounds = 7
    staRounds = 18
    msgBound = 27
    outputFile = "result.txt"
    block_size = 32
    msg_i1 = 2
    msg_i2 = 13
    msg_i3 = 22
    msg_i4 = 6
    msg_i5 = 11
    msg_i6 = 25
    status_i1 = 7
    status_i2 = 18
    status_i3 = 3
    status_i4 = 17
    status_i5 = 19
    status_i6 = 10
    FunctionModel(startRounds, staRounds, msgBound, outputFile, block_size,
                  msg_i1, msg_i2, msg_i3, msg_i4, msg_i5, msg_i6,
                  status_i1, status_i2, status_i3, status_i4, status_i5, status_i6).save_pdf()
    print(time.time() - start)

