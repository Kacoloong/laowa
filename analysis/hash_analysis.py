import gurobipy
import logging
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import misc


class DifferentialAnalysis:

    def __init__(self, round: int,
                 line_transform_constants: tuple[tuple[int]]) -> None:

        self.__model = gurobipy.Model()
        self.__model.setParam(gurobipy.GRB.Param.OutputFlag, False)
        self.__state_size = misc.SIZE
        self.__state_vars = []
        self.__auxil_vars = []
        self.__round = round
        self.__line_transform_constants = line_transform_constants

    @property
    def state_size(self):
        return self.__state_size

    @property
    def state_vars(self):
        return self.__state_vars

    @property
    def auxi_vars(self):
        return self.__auxil_vars

    @property
    def model(self):
        return self.__model

    @property
    def round(self):
        return self.__round

    @property
    def line_transform_constants(self) -> tuple[tuple[int]]:
        return self.__line_transform_constants

    def __generate_variables(self) -> None:
        for r in range(self.round):
            state_vars_per_round = []
            auxil_vars_per_round = []
            for i in range(self.state_size):
                state_vars_per_round.append(
                    self.model.addVar(vtype=gurobipy.GRB.BINARY,
                                      name=f"x_{r}_{i}"))  # 第r轮输入的各字节。
            for i in range(self.state_size // misc.COLUMN_LENGTH):
                auxil_vars_per_round.append(
                    self.model.addVar(vtype=gurobipy.GRB.BINARY,
                                      name=f"d_{r}_{i}"))  # 第r轮的辅助变量。
            self.__state_vars.append(state_vars_per_round)
            self.__auxil_vars.append(auxil_vars_per_round)
        self.model.update()

        logging.debug(f'misc vars: {self.__state_vars}')
        logging.debug(f'Auxi vars{self.__auxil_vars}')

    def __add_mds_cocnstraints(self, var_in, var_out, auxil_var) -> None:
        '''
        var_in:输入mds矩阵一列的4个字节。
        var_out:输出mds矩阵一列的4个字节。
        auxil_var用来表示输入的的var_in是否有任何字节活跃。
        '''

        self.model.addConstr(sum(var_in) + sum(var_out) - 5 * auxil_var
                             >= 0)  # MDS定义改变输出活跃字节个数。
        self.model.addConstr(sum(var_in) - auxil_var >= 0)  # MDS
        self.model.addConstr(sum(var_out) - auxil_var >= 0)
        for i in range(4):
            self.model.addConstr(auxil_var - var_in[i] >= 0)
            self.model.addConstr(auxil_var - var_out[i] >= 0)
        self.model.update()

    def __permutation(self) -> None:
        for r in range(self.round - 1):  # 最后一轮不需要建模
            for z in range(misc.LANE_LENGTH):
                for x in range(misc.ROW_LENGTH):  # 列
                    var_in = []
                    var_out = []
                    for y in range(misc.COLUMN_LENGTH):  # 行
                        # 表示第r轮经过行移位后第i列的变量。
                        var_in_sub = misc.get_id(z, y, x)
                        var_in.append(
                            self.state_vars[r][var_in_sub])  # 列移位不影响var_in
                        new_z = (z + self.line_transform_constants[y][x]
                                 ) % misc.LANE_LENGTH
                        var_out_sub = misc.get_id(new_z, y, x)
                        var_out.append(self.state_vars[r + 1][var_out_sub])
                        logging.info(f'var_in_sub: {var_in_sub}')
                        logging.info(f'var_out: {var_out_sub}')
                    # var_in: 第r轮经过行移位后第i行对应的变量。
                    # var_out: 第r+1轮输入变量。
                    self.__add_mds_cocnstraints(
                        var_in, var_out,
                        self.__auxil_vars[r][z * misc.ROW_LENGTH +
                                             x])  # var_in和var_out参与 MDS 约束。
            logging.info(f'Round:{r} ends')

        # 遍历约束并打印详细信息
        # constraints = self.model.getConstrs()
        # for constr in constraints:
        #     # 获取约束的名称
        #     name = constr.ConstrName
        #     # 获取约束的表达式（线性部分）
        #     expr = self.model.getRow(constr)
        #     # 打印约束的名称和表达式
        #     logging.info(f"{name}: {expr}")

    def __set_object_function(self) -> None:
        equation = []
        for i in range(self.round):
            equation.append(sum(self.state_vars[i]))
        self.model.setObjective(sum(equation),
                                gurobipy.GRB.MINIMIZE)  # 攻击者希望活跃S盒越少越好。
        self.model.update()

    def __init_constraints(self) -> None:
        # 第一轮输入至少有一个活跃字节
        self.model.addConstr(sum(self.state_vars[0]) >= 1)  # pyright:ignore
        self.model.update()

    def solve(self):
        self.__generate_variables()
        self.__permutation()
        self.__set_object_function()
        self.__init_constraints()
        self.model.write('example_model.lp')
        logging.debug(f'Object before optim: {self.model.getObjective()}')
        self.model.optimize()
        obj = self.model.getObjective()
        if self.model.status == 2:
            # for v in self.model.getVars():
            #     if v.x == 1:  # pyright:ignore
            #         logging.info(f'{v.VarName}: {v.xn}')  # pyright:ignore
            return obj.getValue()
        else:
            raise RuntimeError(
                f'Unable to solve the system of {self.line_transform_constants} {self.round} '
            )


def main():
    start_time = time.time()

    lane_transforms = ((
        (2, 2, 3, 6),
        (1, 1, 0, 7),
        (7, 6, 2, 4),
        (5, 7, 6, 2),
    ), (
        (2, 7, 2, 3),
        (0, 4, 3, 6),
        (4, 3, 1, 4),
        (1, 1, 5, 0),
    ), (
        (0, 1, 0, 2),
        (6, 6, 5, 3),
        (1, 4, 6, 5),
        (4, 7, 1, 7),
    ), (
        (1, 7, 1, 6),
        (7, 3, 6, 2),
        (2, 6, 2, 3),
        (4, 0, 7, 5),
    ), (
        (0, 4, 1, 5),
        (4, 3, 2, 6),
        (5, 2, 6, 4),
        (7, 0, 0, 0),
    ), (
        (5, 1, 1, 6),
        (1, 0, 4, 3),
        (0, 5, 6, 1),
        (3, 6, 2, 4),
    ), (
        (7, 5, 7, 6),
        (2, 0, 3, 7),
        (1, 2, 4, 2),
        (5, 7, 6, 0),
    ), (
        (5, 3, 5, 1),
        (3, 7, 0, 3),
        (0, 6, 3, 4),
        (4, 1, 7, 5),
    ), (
        (6, 3, 2, 4),
        (0, 2, 1, 0),
        (3, 0, 3, 7),
        (7, 7, 7, 1),
    ), (
        (7, 7, 1, 0),
        (0, 4, 7, 7),
        (3, 2, 6, 4),
        (5, 3, 3, 6),
    ), (
        (2, 3, 4, 1),
        (0, 2, 3, 4),
        (5, 4, 2, 6),
        (1, 7, 0, 2),
    ), (
        (4, 3, 2, 0),
        (0, 7, 6, 5),
        (6, 5, 0, 6),
        (1, 0, 7, 4),
    ), (
        (7, 6, 4, 0),
        (2, 3, 7, 1),
        (4, 5, 0, 7),
        (6, 1, 6, 4),
    ), (
        (6, 4, 5, 6),
        (5, 0, 0, 5),
        (0, 3, 7, 4),
        (2, 6, 4, 0),
    ), (
        (3, 5, 6, 6),
        (2, 3, 4, 1),
        (1, 1, 0, 0),
        (7, 4, 7, 2),
    ), (
        (1, 6, 5, 1),
        (5, 5, 1, 6),
        (2, 7, 2, 0),
        (7, 2, 7, 4),
    ), (
        (4, 4, 2, 7),
        (5, 3, 1, 6),
        (3, 2, 6, 1),
        (0, 6, 7, 3),
    ))
    lane_transforms = (((2, 7, 2, 3), (0, 4, 3, 6), (4, 3, 1, 4), (1, 1, 5, 0)), )
    for l in lane_transforms:
        for round in range(20, 21):
            result = DifferentialAnalysis(round, l).solve()
            # 最终检查：单S盒最可能差分路径的概率^活跃S盒的个数必须小于随机函数的差分概率。
            # r * f.sbox.prob_of_diff_path >= misc.SIZE and max_r <= r:
            end_time = time.time()
            with open('./active_sbox_results', 'a') as f:
                f.write(
                    f'Round: {round} lane_transform:\n{l}\nno: {result} time: {end_time - start_time}\n'
                )


if __name__ == '__main__':
    main()
