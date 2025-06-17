from z3 import *


def determine_exist_one(solver, main_var, *vars):
    exist_one = Or([v == 1 for v in vars])
    solver.add(main_var == If(exist_one, BitVecVal(1, 1), BitVecVal(0, 1)))


def determine_all_one(solver, main_var, *vars):
    # 所有输入变量均为1的逻辑与结果
    all_one = And([v == 1 for v in vars])
    # 使用If表达式来设置main_var的值
    # 如果all_one为True (即所有vars为1), main_var应设置为1，否则为0
    solver.add(main_var == If(all_one, BitVecVal(1, 1), BitVecVal(0, 1)))


def determine_all_zero(solver, main_var, *vars):
    all_zero = Or([v == 1 for v in vars])
    solver.add(main_var == If(all_zero, BitVecVal(0, 1), BitVecVal(1, 1)))  # 将结果转换为 BitVec


def determine_existzero(solver, main_var, *vars):
    exist_zero = And([v == 1 for v in vars])
    solver.add(main_var == If(exist_zero, BitVecVal(0, 1), BitVecVal(1, 1)))


variables = []


def add_variable(var):
    global variables
    variables.append(var)
    return var


def addfivexor_red(solver, DA, DP, DC1, z_size):
    num_rounds = len(DP)
    # DA_Allone = [[[[add_variable(f"DA_Allone_{round}_{x}_{z}_{v}",BitVec(f'DA_Allone_{round}_{x}_{z}_{v}', 1)) for v in range(3)] for z in range(64)] for x in range(5)] for round in range(num_rounds)]
    # DA_Allzero = [[BitVec(f'DA_Allzero_{x}_{z}', 1) for z in range(64)] for x in range(5)]
    DA_Allone = [
        [[[add_variable(BitVec(f'DA_Allone_{round}_{x}_{z}_{v}', 1)) for v in range(3)] for z in range(z_size)] for x in
         range(5)] for round in range(num_rounds)]
    DA_Allzero = [[add_variable(BitVec(f'DA_Allzero_{x}_{z}', 1)) for z in range(z_size)] for x in range(5)]
    t1 = [1, 1, -1]

    for round in range(num_rounds):
        for x in range(5):
            for z in range(z_size):
                for v in range(3):
                    if round == 0:
                        if x == 0:
                            if v != 1:
                                determine_all_one(solver, DA_Allone[round][x][z][v],
                                                  DA[round][x][0][z][v],
                                                  DA[round][x][1][z][v],
                                                  DA[round][x][2][z][v],
                                                  DA[round][x][4][z][v])
                            else:
                                solver.add(DA_Allone[round][x][z][v] == 1)
                        elif x == 1:
                            if v != 1:
                                determine_all_one(solver, DA_Allone[round][x][z][v],
                                                  DA[round][x][0][z][v],
                                                  DA[round][x][2][z][v],
                                                  DA[round][x][3][z][v],
                                                  DA[round][x][4][z][v])
                            else:
                                solver.add(DA_Allone[round][x][z][v] == 1)
                        elif x == 4:
                            if v != 1:
                                determine_all_one(solver, DA_Allone[round][x][z][v],
                                                  DA[round][x][0][z][v],
                                                  DA[round][x][2][z][v],
                                                  DA[round][x][4][z][v])
                            else:
                                solver.add(DA_Allone[round][x][z][v] == 1)

                        else:
                            solver.add(DA_Allone[round][x][z][v] == 1)
                    else:
                        determine_all_one(solver, DA_Allone[round][x][z][v],
                                          DA[round][x][0][z][v],
                                          DA[round][x][1][z][v],
                                          DA[round][x][2][z][v],
                                          DA[round][x][3][z][v],
                                          DA[round][x][4][z][v])

                # 优化
                solver.add(DA_Allone[round][x][z][1] == DP[round][x][z][1])
                solver.add(Or(DA_Allone[round][x][z][1] == 1, DP[round][x][z][
                    0] == 0))  # DA_Allone[round][x][z][1] >= DP[round][x][z][0]
                solver.add(Or(DA_Allone[round][x][z][0] == 0,
                              DP[round][x][z][0] == 1))  # DA_Allone[round][x][z][0] <= DP[round][x][z][0]

                # 乘法--待定
                # solver.add(t1[0] * DC1[round][x][z] + t1[1] * DA_Allone[round][x][z][0] + t1[2] * DP[round][x][z][0] == 0)
                solver.add(DC1[round][x][z] + DA_Allone[round][x][z][0] == DP[round][x][z][0])  # 乘法改为加法
                solver.add(DA_Allone[round][x][z][2] == DP[round][x][z][2])
                if round == 0:
                    solver.add(Or(DC1[round][x][z] == 0, DA_Allzero[x][z] == 1))  # DC1[round][x][z] <= DA_Allzero[x][z]
                    # solver.add(If(DC1[round][x][z] == 1,DA_Allzero[x][z] ==1,True))


def addtwoxor_red(solver, DP2, DP, DC12, z_size):
    num_rounds = len(DP)
    # DP_Allone = [[[[BitVec(f'DP_Allone_{round}_{x}_{z}_{v}', 1) for v in range(3)] for z in range(64)] for x in range(5)] for round in range(num_rounds)]
    # DP_Allzero = [[[BitVec(f'DP_Allzero_{round}_{x}_{z}', 1) for z in range(64)] for x in range(5)] for round in range(num_rounds)]
    DP_Allone = [
        [[[add_variable(BitVec(f'DP_Allone_{round}_{x}_{z}_{v}', 1)) for v in range(3)] for z in range(z_size)] for x in
         range(5)] for round in range(num_rounds)]
    DP_Allzero = [[[add_variable(BitVec(f'DP_Allzero_{round}_{x}_{z}', 1)) for z in range(z_size)] for x in range(5)]
                  for round in range(num_rounds)]

    t1 = [1, 1, -1]

    for round in range(num_rounds):
        for x in range(5):
            for z in range(z_size):
                for k in range(3):
                    determine_all_one(solver, DP_Allone[round][x][z][k], DP[round][(x + 4) % 5][z][k],
                                      DP[round][(x + 1) % 5][(z + z_size - 1) % z_size][k])
                determine_all_zero(solver, DP_Allzero[round][x][z], DP[round][(x + 4) % 5][z][0],
                                   DP[round][(x + 1) % 5][(z + z_size - 1) % z_size][0])
                # 可以直接dp=dp2
                solver.add(DP_Allone[round][x][z][1] == DP2[round][x][z][1])  # v1=w1
                solver.add(Or(DP2[round][x][z][0] == 0,
                              DP_Allone[round][x][z][1] == 1))  # DP_Allone[round][x][z][1] >= DP2[round][x][z][0]
                solver.add(Or(DP_Allone[round][x][z][0] == 0,
                              DP2[round][x][z][0] == 1))  # DP_Allone[round][x][z][0] <= DP2[round][x][z][0]
                # solver.add(If(DP2[round][x][z][0] == 1,DP_Allone[round][x][z][1] == 1,True))
                # solver.add(If(DP_Allone[round][x][z][0]==1,DP2[round][x][z][0] == 1,True))

                # solver.add(t1[0] * DC12[round][x][z] + t1[1] * DP_Allone[round][x][z][0] + t1[2] * DP2[round][x][z][0] == 0)
                solver.add(DC12[round][x][z] + DP_Allone[round][x][z][0] == DP2[round][x][z][0])
                solver.add(DP_Allone[round][x][z][2] == DP2[round][x][z][2])  # v2=w2
                solver.add(Or(DC12[round][x][z] == 0, DP_Allzero[round][x][z] == 1))
                # solver.add(If(DC12[round][x][z] == 1,DP_Allzero[round][x][z] == 1,True))


def addTheta_red(solver, DA, DP2, DB, DC2, z_size, rho):
    num_rounds = len(DP2)
    # DP2_Allone = [[[[[BitVec(f'DP2_Allone_{round}_{x}_{y}_{z}_{v}', 1) for v in range(3)] for z in range(64)] for y in range(5)] for x in range(5)] for round in range(num_rounds)]
    # DP2_Allzero = [[[[BitVec(f'DP2_Allzero_{round}_{x}_{y}_{z}', 1) for z in range(64)] for y in range(5)] for x in range(5)] for round in range(num_rounds)]
    DP2_Allone = [[[[[add_variable(BitVec(f'DP2_Allone_{round}_{x}_{y}_{z}_{v}', 1)) for v in range(3)] for z in
                     range(z_size)] for y in range(5)] for x in range(5)] for round in range(num_rounds)]
    DP2_Allzero = [
        [[[add_variable(BitVec(f'DP2_Allzero_{round}_{x}_{y}_{z}', 1)) for z in range(z_size)] for y in range(5)] for x
         in range(5)] for round in range(num_rounds)]

    t1 = [1, 1, -1]

    for round in range(num_rounds):
        for x in range(5):
            for y in range(5):
                for z in range(z_size):
                    for v in range(3):
                        determine_all_one(solver, DP2_Allone[round][x][y][z][v], DA[round][x][y][z][v],
                                          DP2[round][x][z][v])

                    determine_all_zero(solver, DP2_Allzero[round][x][y][z], DA[round][x][y][z][0], DP2[round][x][z][0])

                    solver.add(
                        DP2_Allone[round][x][y][z][1] == DB[round][y][(2 * x + 3 * y) % 5][(z + rho[x][y]) % z_size][1])

                    solver.add(Or(DP2_Allone[round][x][y][z][1] == 1,
                                  DB[round][y][(2 * x + 3 * y) % 5][(z + rho[x][y]) % z_size][0] == 0))
                    solver.add(Or(DP2_Allone[round][x][y][z][0] == 0,
                                  DB[round][y][(2 * x + 3 * y) % 5][(z + rho[x][y]) % z_size][0] == 1))
                    # solver.add(If(DB[round][y][(2*x+3*y)%5][(z+rho[x][y])%64][0] == 1,DP2_Allone[round][x][y][z][1] == 1,True))
                    # solver.add(If(DP2_Allone[round][x][y][z][0] == 1,DB[round][y][(2*x+3*y)%5][(z+rho[x][y])%64][0] == 1,True))
                    # solver.add( t1[0] * DC2[round][x][y][z] + t1[1] * DP2_Allone[round][x][y][z][0] + t1[2] * DB[round][y][(2*x+3*y)%5][(z+rho[x][y])%64][0] == 0)
                    solver.add(DC2[round][x][y][z] + DP2_Allone[round][x][y][z][0] ==
                               DB[round][y][(2 * x + 3 * y) % 5][(z + rho[x][y]) % z_size][0])

                    solver.add(
                        DP2_Allone[round][x][y][z][2] == DB[round][y][(2 * x + 3 * y) % 5][(z + rho[x][y]) % z_size][2])
                    solver.add(Or(DC2[round][x][y][z] == 0, DP2_Allzero[round][x][y][z] == 1))
                    # solver.add(If(DC2[round][x][y][z] == 1,DP2_Allzero[round][x][y][z] == 1,True))


def addSbox_nc(solver, DB, DA, z_size):
    t = [[1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1],
         [0, 1, -1, 1, 0, 0, 1, 0, 0, -1, -1, 1],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1],
         [0, -1, 0, 0, 0, -1, 0, 0, -1, 0, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
         [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, -1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, -1, 0],
         [0, 1, -1, 0, 1, -1, 0, 1, -1, 0, -1, 1],
         [0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 1, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1],
         [-1, 1, 0, -1, 1, 0, -1, 1, 0, 1, -1, 0],
         [0, -1, 0, 0, -1, 0, -1, 1, -1, 0, 1, 0],
         [0, -1, 0, -1, 1, -1, 0, -1, 0, 0, 1, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0]]
    c = [0, 0, 0, 0, -2, 0, 0, 0, 0, 0, -2, 0, 0, -2, -2, 0, 0, 0, 0]
    # 定义生成线性表达式的函数

    # 遍历round、x、y、z和q，添加约束
    for round in range(len(DB)):
        for x in range(5):
            for y in range(5):
                for z in range(z_size):
                    for q in range(19):
                        # 生成线性表达式
                        lin_expr = lin_expr_of_2(t[q],
                                                 DB[round][x][y][z][0], DB[round][x][y][z][1], DB[round][x][y][z][2],
                                                 DB[round][(x + 1) % 5][y][z][0], DB[round][(x + 1) % 5][y][z][1],
                                                 DB[round][(x + 1) % 5][y][z][2],
                                                 DB[round][(x + 2) % 5][y][z][0], DB[round][(x + 2) % 5][y][z][1],
                                                 DB[round][(x + 2) % 5][y][z][2],
                                                 DA[round + 1][x][y][z][0], DA[round + 1][x][y][z][1],
                                                 DA[round + 1][x][y][z][2])

                        # 添加线性约束，>= c[q]
                        solver.add(lin_expr >= c[q])


def addDoMnew(solver, DA, dom, z_size, rho):
    Nowhite = [[add_variable(BitVec(f"Nowhite_{x}_{z}", 1)) for z in range(z_size)] for x in range(2)]
    Existred = [[add_variable(BitVec(f"Existred_{x}_{z}", 1)) for z in range(z_size)] for x in range(2)]
    Existblue = [[add_variable(BitVec(f"Existblue_{x}_{z}", 1)) for z in range(z_size)] for x in range(2)]

    r = len(DA) - 1
    for z in range(z_size):
        determine_all_one(solver, Nowhite[0][z],
                          DA[r][3][0][(z - rho[3][0] + z_size) % z_size][1],
                          DA[r][3][3][(z - rho[3][0] + z_size) % z_size][1],
                          DA[r][0][2][(z - rho[0][2] + z_size) % z_size][1],
                          DA[r][0][0][(z - rho[0][2] + z_size) % z_size][1])

        determine_all_one(solver, Nowhite[1][z],
                          DA[r][4][1][(z - rho[4][1] + z_size) % z_size][1],
                          DA[r][4][4][(z - rho[4][1] + z_size) % z_size][1],
                          DA[r][1][3][(z - rho[1][3] + z_size) % z_size][1],
                          DA[r][1][1][(z - rho[1][3] + z_size) % z_size][1])

        determine_existzero(solver, Existred[0][z],
                            DA[r][3][0][(z - rho[3][0] + z_size) % z_size][0],
                            DA[r][3][3][(z - rho[3][0] + z_size) % z_size][0])

        determine_existzero(solver, Existred[1][z],
                            DA[r][4][1][(z - rho[4][1] + z_size) % z_size][0],
                            DA[r][4][4][(z - rho[4][1] + z_size) % z_size][0])

        determine_existzero(solver, Existblue[0][z],
                            DA[r][3][0][(z - rho[3][0] + z_size) % z_size][2],
                            DA[r][3][3][(z - rho[3][0] + z_size) % z_size][2])

        determine_existzero(solver, Existblue[1][z],
                            DA[r][4][1][(z - rho[4][1] + z_size) % z_size][2],
                            DA[r][4][4][(z - rho[4][1] + z_size) % z_size][2])

        determine_all_one(solver, dom[0][z], Nowhite[0][z], Existred[0][z], Existblue[0][z])
        determine_all_one(solver, dom[1][z], Nowhite[1][z], Existred[1][z], Existblue[1][z])


# 为了在计算红、蓝自由度的时候减去灰色的。
def beta_constraints(solver, DA, beta, z_size):
    for z in range(z_size):
        determine_all_one(solver, beta[0][z], DA[0][0][0][z][0], DA[0][0][0][z][2])
        determine_all_one(solver, beta[1][z], DA[0][0][1][z][0], DA[0][0][1][z][2])
        determine_all_one(solver, beta[2][z], DA[0][0][2][z][0], DA[0][0][2][z][2])
        determine_all_one(solver, beta[3][z], DA[0][0][4][z][0], DA[0][0][4][z][2])


def lin_expr_of(coeffs, *vars):
    return sum(c * v for c, v in zip(coeffs, vars))


def lin_expr_of_2(t_row, *args):
    # 将1位BitVec转换为整数（0或1），然后与t的系数相乘
    return Sum([t_coef * If(arg == 1, 1, 0) for t_coef, arg in zip(t_row, args) if t_coef != 0])


def extend_to_8bit(bv):
    return ZeroExt(7, bv)  # 将1-bit扩展为32-bit

