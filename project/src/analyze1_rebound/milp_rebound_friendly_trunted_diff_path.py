import gurobipy as gp
import os
import shutil
from time import time

# import numpy as np
# from src.analyze1_rebound.ulity import multiply_elements
def multiply_elements(lst):
    product = 1
    for number in lst:
        product *= number
    return product

class MILPFindReboundPath:
    """
    MILPFindReboundPath
    使用MILP寻找Rebound友好的截断差分路线
    """

    def __init__(
        self,
        ciphername,
        cipher_state,
        cipher_state_size,
        cipher_mds,
        cipher_shift,
        cipher_mc_mr,
        cipher_last_mix,
        cipher_key_size,
        rounds,
        begin_round,
        end_round,
    ) -> None:
        self.model = gp.Model()
        self.model.setParam(gp.GRB.Param.OutputFlag, False)

        ## 要分析的算法名称
        self.cipher_name = ciphername
        ## 要分析的轮数
        self.analyze_rounds = rounds
        ## 要分析的算法状态表示
        ## 列表类型，如AES:[4,4],Whirlpool:[8,8]
        self.cipher_state = cipher_state
        ## 要分析算法的状态字数量
        ## AES:4*4=16,Whirlpool:8*8=64
        self.cipher_state_words = multiply_elements(cipher_state)

        self.cipher_state_size = cipher_state_size
        self.n_row = cipher_state[0]
        self.n_column = cipher_state[1]
        self.cipher_mds = cipher_mds
        self.mds_branch_number = self.mds_differential_branch_number(self.cipher_mds)
        # 默认左循环移位或上循环移位
        self.cipher_shift = cipher_shift
        self.cipher_mc_mr = cipher_mc_mr

        ## 最后一轮是否包含列混淆或行混淆
        self.cipher_last_mix = cipher_last_mix
        self.after_shift_matrix = []
        state_matrix = [
            [self.n_row * i + j for j in range(self.n_column)]
            for i in range(self.n_row)
        ]
        if self.cipher_mc_mr == 0:

            transposed_matrix = list(zip(*state_matrix))
            # 对转置后的每一行应用循环左移
            rotated_rows = [
                self.left_rotate(row, shift)
                for row, shift in zip(transposed_matrix, self.cipher_shift)
            ]
            # 再次转置以恢复原始的行列方向
            self.after_shift_matrix = list(zip(*rotated_rows))
        else:
            for i in range(self.n_column):
                self.after_shift_matrix.append(
                    self.left_rotate(state_matrix[i], self.cipher_shift[i])
                )
        # print(self.after_shift_matrix)
        # print(self.flatten_state(self.after_shift_matrix))
        self.key_size = cipher_key_size
        self.state_vars = []
        self.auxi_vars = []
        self.aes_type = 128
        self.inbound_begin_round = begin_round
        self.inbound_end_round = end_round

        self.milp_lpfile_folder = ""
        self.milp_lpfile_name = ""

    def left_rotate(self, row, n):
        """向左循环移动列表中的元素"""
        return row[n:] + row[:n]

    def mds_differential_branch_number(self, mds):
        return len(mds) + 1

    def generate_variables(self) -> None:
        """
        生成搜索截断差分路线中需要使用的变量
        """
        model = self.model
        rounds = self.analyze_rounds
        state_size = self.cipher_state_words
        mds_n_row = len(self.cipher_mds)

        ## 如果最后一轮包含MDS变换，那么需要多生成一个mds操作所需的变量和mds输出的变量
        if self.cipher_last_mix:
            for r in range(rounds + 1):
                temp = []
                for i in range(state_size):
                    temp.append(model.addVar(vtype=gp.GRB.BINARY, name=f"x_{r}_{i}"))
                self.state_vars.append(temp)
            for r in range(rounds):
                temp = []
                for i in range(int(state_size / mds_n_row)):
                    temp.append(model.addVar(vtype=gp.GRB.BINARY, name=f"d_{r}_{i}"))
                self.auxi_vars.append(temp)
        ## 否则不需要
        else:
            for r in range(rounds):
                temp = []
                for i in range(state_size):
                    temp.append(model.addVar(vtype=gp.GRB.BINARY, name=f"x_{r}_{i}"))
                self.state_vars.append(temp)
            for r in range(rounds - 1):
                temp = []
                for i in range(int(state_size / mds_n_row)):
                    temp.append(model.addVar(vtype=gp.GRB.BINARY, name=f"d_{r}_{i}"))
                self.auxi_vars.append(temp)
        model.update()
        # print("状态变量:", self.state_vars)
        # print("辅助变量:", self.auxi_vars)

    def mds_cocnstraints(self, var_in, var_out, auxi_var) -> None:
        """
        生成搜索截断差分路线中MDS变换的约束
        var_in 为输入向量
        var_out 为输出向量
        auxi_var 为辅助变量，表示这一行或列是否活跃
        """
        model = self.model
        model.addConstr(
            sum(var_in) + sum(var_out) - self.mds_branch_number * auxi_var >= 0
        )
        model.addConstr(sum(var_in) - auxi_var >= 0)
        model.addConstr(sum(var_out) - auxi_var >= 0)
        for i in range(len(var_in)):
            model.addConstr(auxi_var - var_in[i] >= 0)
            model.addConstr(auxi_var - var_out[i] >= 0)
        model.update()

    def generate_round_function_constraint(self):
        """
        生成搜索截断差分路线中杂凑密码算法的轮函数约束
        """
        # model = self.model
        rounds = self.analyze_rounds
        # state_size = self.cipher_state
        state_vars = self.state_vars
        # index = [[0, 5, 10, 15], [4, 9, 14, 3], [8, 13, 2, 7], [12, 1, 6, 11]]
        if self.cipher_last_mix:
            if self.cipher_mc_mr == 0:
                for r in range(rounds):
                    for i in range(self.n_column):
                        var_in = []
                        var_out = []
                        for j in range(self.n_row):
                            var_in.append(state_vars[r][self.after_shift_matrix[i][j]])
                        for j in range(self.n_row):
                            var_out.append(state_vars[r + 1][self.n_row * i + j])
                        # print("in", var_in)
                        # print("out", var_out)
                        self.mds_cocnstraints(var_in, var_out, self.auxi_vars[r][i])
            else:
                for r in range(rounds):
                    for i in range(self.n_row):
                        var_in = []
                        var_out = []
                        for j in range(self.n_column):
                            var_in.append(state_vars[r][self.after_shift_matrix[j][i]])
                        for j in range(self.n_column):
                            var_out.append(state_vars[r + 1][self.n_column * j + i])
                        # print("in", var_in)
                        # print("out", var_out)
                        self.mds_cocnstraints(var_in, var_out, self.auxi_vars[r][i])
        else:
            if self.cipher_mc_mr == 0:
                for r in range(rounds - 1):
                    for i in range(self.n_column):
                        var_in = []
                        var_out = []
                        for j in range(self.n_row):
                            var_in.append(state_vars[r][self.after_shift_matrix[i][j]])
                        for j in range(self.n_row):
                            var_out.append(state_vars[r + 1][self.n_row * i + j])
                        # print("in", var_in)
                        # print("out", var_out)
                        self.mds_cocnstraints(var_in, var_out, self.auxi_vars[r][i])
            else:
                for r in range(rounds - 1):
                    for i in range(self.n_row):
                        var_in = []
                        var_out = []
                        for j in range(self.n_column):
                            var_in.append(state_vars[r][self.after_shift_matrix[j][i]])
                        for j in range(self.n_column):
                            var_out.append(state_vars[r + 1][self.n_column * j + i])
                        # print("in", var_in)
                        # print("out", var_out)
                        self.mds_cocnstraints(var_in, var_out, self.auxi_vars[r][i])
        # constraints = model.getConstrs()
        # for constr in constraints:
        #     print(f"Constraint Name: {constr.ConstrName}")
        #     print(f"Constraint: {model.getRow(constr)}")
        #     print(f"Sense: {constr.Sense}")
        #     print(f"RHS: {constr.RHS}")

    def aes_round(self) -> None:
        # model = self.model
        rounds = self.analyze_rounds
        # state_size = self.cipher_state
        state_vars = self.state_vars
        index = [[0, 5, 10, 15], [4, 9, 14, 3], [8, 13, 2, 7], [12, 1, 6, 11]]
        for r in range(rounds - 1):
            for i in range(4):
                var_in = []
                var_out = []
                for j in range(4):
                    var_in.append(state_vars[r][index[i][j]])
                for j in range(4):
                    var_out.append(state_vars[r + 1][4 * i + j])
                # print(var_in)
                # print(var_out)
                self.mds_cocnstraints(var_in, var_out, self.auxi_vars[r][i])
        # constraints = model.getConstrs()

    def set_object_function(self) -> None:
        equation = []
        for i in range(self.analyze_rounds):
            equation.append(sum(self.state_vars[i]))
        self.model.setObjective(sum(equation), gp.GRB.MINIMIZE)
        self.model.update()

    def init_constraints(self) -> None:
        self.model.addConstr(sum(self.state_vars[0]) >= 1)
        self.model.update()

    ## Inbound 的约束
    ## 1. Inbound轮中的活跃S盒个数要小于自由度（状态大小和密钥状态大小）
    ## 2. 尽量最大活跃S盒的数量
    ## 3. Inbound阶段产生的起始点要大于Outbound所需要使用的起始点
    def inbound_constraints(self) -> None:
        """
        生成搜索截断差分路线中Inbound阶段的约束
        """
        ## 活跃S盒的个数小于自由度
        equation = []
        begin_round, end_round = self.inbound_begin_round, self.inbound_end_round
        for r in range(begin_round, end_round + 1):
            equation.append(sum(self.state_vars[r]))
        # print(
        #     "Inbound inequality:",
        #     sum(equation) <= self.cipher_state_words + self.key_size,
        # )
        self.model.addConstr(sum(equation) <= (self.cipher_state_words + self.key_size))
        ## 2.尽量最大活跃S盒的数量
        # self.model.setObjective(sum(equation), index=0, sense=GRB.MAXIMIZE)
        self.model.update()

    ## Outbound 的约束
    ## 1.MC操作的概率加上碰撞的概率要大于生日悖论的概率
    ## 2.初始活跃位置要和最后的活跃位置相等
    ## 3.初始活跃的字节要大于0
    def outbound_constraints(self) -> None:
        """
        生成搜索截断差分路线中中Outbound阶段的约束
        """
        begin_round, end_round = self.inbound_begin_round, self.inbound_end_round
        ## 前Outbound轮的约束
        forward_equation = []
        ## back Outbound轮的约束
        backward_equation = []
        ## l 表示截断前向和后向截断差分的概率
        ## branch_number - forward_equation[r][i] 表示有几个状态是非活跃的，那么乘一个状态的比特数就是截断差分成立的概率
        l = 0
        state_vars = self.state_vars[: begin_round - 1]
        # index = [[0, 5, 10, 15], [4, 9, 14, 3], [8, 13, 2, 7], [12, 1, 6, 11]]
        ## 将前向，后向的活跃字节记录下来
        if self.cipher_last_mix:
            if self.cipher_mc_mr == 0:
                for r in range(begin_round - 1):
                    temp_equation = []
                    for i in range(self.n_column):
                        temp_var = []
                        for j in range(self.n_row):
                            temp_var.append(
                                state_vars[r][self.after_shift_matrix[i][j]]
                            )
                        temp_equation.append(sum(temp_var))
                    forward_equation.append(temp_equation)

                for r in range(end_round + 2, self.analyze_rounds + 1):
                    temp_equation = []
                    for i in range(self.n_column):
                        temp_var = []
                        for j in range(self.n_row):
                            temp_var.append(self.state_vars[r][self.n_row * i + j])
                        temp_equation.append(sum(temp_var))
                    backward_equation.append(temp_equation)

                for r in range(begin_round - 1):
                    for i in range(self.n_column):
                        l += self.auxi_vars[r][i] * (
                            self.n_row - forward_equation[r][i]
                        )

                back_auxi_vars = self.auxi_vars[end_round + 1 : self.analyze_rounds]
                for r in range(len(backward_equation)):
                    for i in range(self.n_column):
                        l += back_auxi_vars[r][i] * (
                            self.n_row - backward_equation[r][i]
                        )
            else:
                for r in range(begin_round - 1):
                    temp_equation = []
                    for i in range(self.n_row):
                        temp_var = []
                        for j in range(self.n_column):
                            temp_var.append(
                                state_vars[r][self.after_shift_matrix[j][i]]
                            )
                        temp_equation.append(sum(temp_var))
                    forward_equation.append(temp_equation)

                for r in range(end_round + 2, self.analyze_rounds + 1):
                    temp_equation = []
                    for i in range(self.n_row):
                        temp_var = []
                        for j in range(self.n_column):
                            temp_var.append(self.state_vars[r][self.n_column * j + i])
                        temp_equation.append(sum(temp_var))
                    backward_equation.append(temp_equation)

                for r in range(begin_round - 1):
                    for i in range(self.n_row):
                        l += self.auxi_vars[r][i] * (
                            self.n_column - forward_equation[r][i]
                        )

                back_auxi_vars = self.auxi_vars[end_round + 1 : self.analyze_rounds]
                for r in range(len(backward_equation)):
                    for i in range(self.n_row):
                        l += back_auxi_vars[r][i] * (
                            self.n_column - backward_equation[r][i]
                        )
        else:
            if self.cipher_mc_mr == 0:
                for r in range(begin_round - 1):
                    temp_equation = []
                    for i in range(self.n_column):
                        temp_var = []
                        for j in range(self.n_row):
                            temp_var.append(
                                state_vars[r][self.after_shift_matrix[i][j]]
                            )
                        temp_equation.append(sum(temp_var))
                    forward_equation.append(temp_equation)

                for r in range(end_round + 2, self.analyze_rounds):
                    temp_equation = []
                    for i in range(self.n_column):
                        temp_var = []
                        for j in range(self.n_row):
                            temp_var.append(self.state_vars[r][self.n_row * i + j])
                        temp_equation.append(sum(temp_var))
                    backward_equation.append(temp_equation)

                for r in range(begin_round - 1):
                    for i in range(self.n_column):
                        l += self.auxi_vars[r][i] * (
                            self.n_row - forward_equation[r][i]
                        )

                back_auxi_vars = self.auxi_vars[end_round + 1 : self.analyze_rounds - 1]
                for r in range(len(backward_equation)):
                    for i in range(self.n_column):
                        l += back_auxi_vars[r][i] * (
                            self.n_row - backward_equation[r][i]
                        )
            else:
                for r in range(begin_round - 1):
                    temp_equation = []
                    for i in range(self.n_row):
                        temp_var = []
                        for j in range(self.n_column):
                            temp_var.append(
                                state_vars[r][self.after_shift_matrix[j][i]]
                            )
                        temp_equation.append(sum(temp_var))
                    forward_equation.append(temp_equation)

                for r in range(end_round + 2, self.analyze_rounds):
                    temp_equation = []
                    for i in range(self.n_row):
                        temp_var = []
                        for j in range(self.n_column):
                            temp_var.append(self.state_vars[r][self.n_column * j + i])
                        temp_equation.append(sum(temp_var))
                    backward_equation.append(temp_equation)

                for r in range(begin_round - 1):
                    for i in range(self.n_row):
                        l += self.auxi_vars[r][i] * (
                            self.n_column - forward_equation[r][i]
                        )

                back_auxi_vars = self.auxi_vars[end_round + 1 : self.analyze_rounds - 1]
                for r in range(len(backward_equation)):
                    for i in range(self.n_row):
                        l += back_auxi_vars[r][i] * (
                            self.n_column - backward_equation[r][i]
                        )
        ## 设置目标函数，使得搜索到的截断差分概率最大，概率的对数最小
        # print("l:", l)
        self.model.setObjective(
            self.cipher_state_size * (l + sum(self.state_vars[0])),
            gp.GRB.MINIMIZE,
        )
        # print(
        #     "outbound inequality:",
        #     8 * (l + sum(self.__state_vars[0])) <= int(self.__aes_type / 2) - 1,
        # )
        cipher_state_word = self.cipher_state_words
        # print("cipher_state_word", cipher_state_word)
        ## 1.MC或MR操作的概率加上碰撞的概率要大于生日悖论的概率
        # self.model.addConstr(8 * (l + sum(self.__state_vars[0])) <= int(self.__aes_type/2)-1)
        self.model.addConstr(
            self.cipher_state_size * (l + sum(self.state_vars[0]))
            <= int((self.cipher_state_size * cipher_state_word) / 2)
        )
        # self.model.addConstr(8 * (l + sum(self.__state_vars[0])) <= 31)
        # self.model.update()
        ## 2.初始活跃位置要和最后的活跃位置相等,寻找碰撞的条件
        begin_state = self.state_vars[0]
        if self.cipher_last_mix:
            end_state = self.state_vars[self.analyze_rounds]
            for i in range(cipher_state_word):
                self.model.addConstr(begin_state[i] == end_state[i])
        else:
            end_state = self.state_vars[self.analyze_rounds - 1]
            after_shift_matrix = self.flatten_state(self.after_shift_matrix)
            after_sr_state = []
            # print(self.after_shift_matrix)
            # print(after_shift_matrix)
            for i in range(cipher_state_word):
                after_sr_state.append(end_state[after_shift_matrix[i]])
            for i in range(cipher_state_word):
                self.model.addConstr(begin_state[i] == after_sr_state[i])
        self.model.update()
        # constraints = self.model.getConstrs()
        # for constr in constraints:
        #     print(f"Constraint Name: {constr.ConstrName}")
        #     print(f"Constraint: {self.model.getRow(constr)}")
        #     print(f"Sense: {constr.Sense}")
        #     print(f"RHS: {constr.RHS}")

    @staticmethod
    def flatten_state(s):
        state_bits = [s[i][j] for i in range(len(s)) for j in range(len(s[0]))]
        return state_bits

    def construct_active_sbox_model(self) -> None:
        """
        构建寻找最小活跃S盒模型
        """
        self.generate_variables()
        self.aes_round()
        self.set_object_function()
        self.init_constraints()

        folder_path = "AES_active_sbox_milp_lp"
        filename = f"AES{self.aes_type}_round_{self.analyze_rounds}.lp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.model.write(f"{folder_path}/{filename}")

    def construct_rebound_friend_model(self) -> None:
        """
        构建寻找Rebound分析友好的阶段差分路线模型
        """
        self.generate_variables()
        # self.aes_round()
        self.generate_round_function_constraint()
        self.inbound_constraints()
        self.outbound_constraints()
        self.init_constraints()

        self.milp_lpfile_folder = f"{self.cipher_name}_rebound_milp_lp"
        self.milp_lpfile_name = f"{self.cipher_name}_round_{self.analyze_rounds}_{self.inbound_begin_round}_{self.inbound_end_round}.lp"
        # self.milp_lpfile_name = f"AES{self.aes_type}_round_{self.analyze_rounds}.lp"
        if not os.path.exists(self.milp_lpfile_folder):
            os.makedirs(self.milp_lpfile_folder)
        self.model.write(f"{self.milp_lpfile_folder}/{self.milp_lpfile_name}")

    def remove_foler(self):
        shutil.rmtree(self.folder_path)

    def solver(self):
        """
        求解一个最优解
        """
        # self.construct_active_sbox_model()
        c_model_start_time = time()
        self.construct_rebound_friend_model()
        c_model_end_time = time() - c_model_start_time
        model = self.model
        s_model_start_time = time()
        model.optimize()
        s_model_end_time = time() - s_model_start_time
        # os.remove(f"{self.__milp_lpfile_folder}/{self.__milp_lpfile_name}")
        cipher_state_word = self.cipher_state_words
        if model.status == gp.GRB.OPTIMAL:
            obj = model.getObjective()
            # print("objective function:", obj)s
            obj_value = obj.getValue()
            # print("截断差分概率:", obj_value)
            # number_sol = model.getAttr("SolCount")
            # print("num sols:", number_sol)
            if self.cipher_last_mix:
                solution = [
                    [0 for i in range(cipher_state_word)]
                    for i in range(self.analyze_rounds + 1)
                ]
                mds_solution = [
                    [0 for i in range(len(self.cipher_mds))]
                    for i in range(self.analyze_rounds)
                ]
            else:
                solution = [
                    [0 for i in range(cipher_state_word)]
                    for i in range(self.analyze_rounds)
                ]
                mds_solution = [
                    [0 for i in range(len(self.cipher_mds))]
                    for i in range(self.analyze_rounds - 1)
                ]
            state_vars = self.state_vars
            auxi_vars = self.auxi_vars
            if model.status == gp.GRB.OPTIMAL:
                for i in range(len(state_vars)):
                    for j in range(cipher_state_word):
                        if state_vars[i][j].xn == 1:
                            solution[i][j] = 1
                for i in range(len(auxi_vars)):
                    for j in range(len(self.cipher_mds)):
                        if auxi_vars[i][j].xn == 1:
                            mds_solution[i][j] = 1
            # print(solution)
            return solution, mds_solution, obj_value, c_model_end_time, s_model_end_time
        else:
            return None

    def solvers(self, num_sol):
        """
        用于求解多个最优解
        """
        c_model_start_time = time()
        self.construct_rebound_friend_model()
        c_model_end_time = time() - c_model_start_time
        model = self.model
        model.setParam("PoolSearchMode", 2)
        model.setParam("PoolSolutions", num_sol)
        s_model_start_time = time()
        model.optimize()
        s_model_end_time = time() - s_model_start_time
        cipher_state_word = self.cipher_state_words
        if model.status == gp.GRB.OPTIMAL:
            obj = model.getObjective()
            obj_value = obj.getValue()
            # print(obj1)
            # print(obj1.getValue())
            number_sol = model.getAttr("SolCount")
            # print("num sols:", number_sol)
            result_solution = []
            result_mds_solution = []

            for i in range(number_sol):
                model.setParam("SolutionNumber", i)
                # print("sol:",i)

                if self.cipher_last_mix:
                    solution = [
                        [0 for i in range(cipher_state_word)]
                        for i in range(self.analyze_rounds + 1)
                    ]
                    mds_solution = [
                        [0 for i in range(len(self.cipher_mds))]
                        for i in range(self.analyze_rounds)
                    ]
                else:
                    solution = [
                        [0 for i in range(cipher_state_word)]
                        for i in range(self.analyze_rounds)
                    ]
                    mds_solution = [
                        [0 for i in range(len(self.cipher_mds))]
                        for i in range(self.analyze_rounds - 1)
                    ]
                state_vars = self.state_vars
                auxi_vars = self.auxi_vars
                for i in range(len(state_vars)):
                    for j in range(cipher_state_word):
                        if state_vars[i][j].xn == 1:
                            solution[i][j] = 1
                result_solution.append(solution)

                for i in range(len(auxi_vars)):
                    for j in range(len(self.cipher_mds)):
                        if auxi_vars[i][j].xn == 1:
                            mds_solution[i][j] = 1
                result_mds_solution.append(mds_solution)
            return (
                result_solution,
                result_mds_solution,
                obj_value,
                c_model_end_time,
                s_model_end_time,
                number_sol,
            )
        else:
            return None

if __name__ == "__main__":
    rounds = 6
    inbound_begin_round = 1
    inbound_end_round = 4
    ciphername = "AES_128"
    cipher_state = [4, 4]
    cipher_state_size = 128
    cipher_mds = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    cipher_shift = [0, 1, 2, 3]
    cipher_mc_mr = 0
    cipher_last_mix = False
    cipher_key_size = 16

    AES_TD = MILPFindReboundPath(
        ciphername,
        cipher_state,
        cipher_state_size,
        cipher_mds,
        cipher_shift,
        cipher_mc_mr,
        cipher_last_mix,
        cipher_key_size,
        rounds,
        inbound_begin_round,
        inbound_end_round,
    )

    print("输出一个解:")
    result = AES_TD.solver()
    if result is not None:
        solution, mds_solution = result[0], result[1]
        print("截断差分:", solution)
        print("经过MDS矩阵活跃列:", mds_solution)
        inbound_path = solution[inbound_begin_round : inbound_end_round + 1]
        inbound_active_mds = mds_solution[inbound_begin_round:inbound_end_round]
        print("Inbound 阶段路线:", inbound_path)
        print("Inbound 阶段活跃列:", inbound_active_mds)
        print("\n")
    else:
        print("请选择其他的轮数进行输入")
