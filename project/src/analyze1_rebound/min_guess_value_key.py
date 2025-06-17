import os
import itertools
import subprocess
import shutil
from src.gdsat import ReduceGDtoSAT


class MinGuessKey:

    def __init__(
        self,
        inbound_begin,
        inbound_end,
        num_inbound,
        inbound_cover_round,
        solution,
        active_colunm,
        maxguess,
        maxstep,
        solution_number,
    ) -> None:

        self.inbound_begin = inbound_begin
        self.inbound_end = inbound_end
        ## Inbound 覆盖的轮数
        self.rounds = self.inbound_end - self.inbound_begin + 1
        # print(self.rounds)
        ## Inbound 的个数
        assert num_inbound == len(inbound_cover_round)
        self.n_inbound = num_inbound
        ## 每一个 Inbound阶段覆盖的轮数
        self.inbound_cover_round = inbound_cover_round
        ## Inbound 阶段的截断差分路线
        self.solution = solution
        ## Inbound 阶段的差分状态变量
        self.x_diff_state = [
            [f"dx_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end + 1)
        ]
        self.y_diff_state = [
            [f"dy_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end + 1)
        ]
        self.z_diff_state = [
            [f"dz_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end)
        ]
        # print(x_diff_state)
        # print(y_diff_state)
        # print(z_diff_state)

        ## Inbound 阶段的每一个状态差分是否可知
        ## -1 为差分为0，0为差分未知
        ## 初始全为0，然后根据solution来初始化
        ## x表示经过SB前的状态，y表示经过SB和SR的状态，z表示经过MC的状态
        self.x_know_diff_state = [
            [-1 for i in range(16)]
            for j in range(self.inbound_begin, self.inbound_end + 1)
        ]
        self.y_know_diff_state = []
        self.z_know_diff_state = [
            [-1 for i in range(16)] for j in range(self.inbound_begin, self.inbound_end)
        ]
        # print(x_know_diff_state)

        ## Inbound 阶段状态值变量
        self.x_value_state = [
            [f"vx_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end + 1)
        ]
        self.y_value_state = [
            [f"vy_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end + 1)
        ]
        self.z_value_state = [
            [f"vz_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end)
        ]

        ## 连接Inbound 阶段的密钥变量
        self.key_state = [
            [f"rc_{i}_{k}" for k in range(16)]
            for i in range(self.inbound_begin, self.inbound_end)
        ]

        ## 经过MC的列是否活跃
        self.mds_is_active = active_colunm

        ## MDS矩阵的规格
        self.mds_size = 4

        ## 最大猜测变量个数
        self.maxguess = maxguess
        # print(self.maxguess)

        ## 最大推导步数（最大推导多少步能得到所有变量）
        self.maxstep = maxstep
        # print(self.maxstep)
        self.filename = ""

        self.folder_path = f"{solution_number}mg_{self.maxguess}_ms_{self.maxstep}"
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        self.index_sr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]

    def mds_relation(self, vars, n_vars):
        """
        根据MDS矩阵输入输出间未知变量的个数来构建关系\\
        MDS：4*4\\
        input=[x0,x1,x2,x3]\\
        output=[y0,y1,y2,y3]\\
        len(input)+len(output) 未知变量个数>=5\\
        那么知道input和output中任意4个值就能推出其他值，通过这个来构建关系
        """
        content = ""
        for quarter in itertools.combinations(vars, n_vars):
            for element in vars:
                if element not in quarter:
                    content += ",".join(quarter) + " => " + element + "\n"
        return content

    def diff2value(self, dx_vars, dy_vars, vx_vars, vy_vars):
        """
        已知S盒的非零兼容差分可用推导出S盒的输入输出\\
        通过这个来构建变量之间的关系
        """
        content = ""
        for dx in range(len(dx_vars)):
            # for vx in range(len(vx_vars)):
            content += f"{dx_vars[dx]},{dy_vars[dx]} => {vx_vars[dx]}\n"
            content += f"{dx_vars[dx]},{dy_vars[dx]} => {vy_vars[dx]}\n"
        return content

    def init_diff_state(self):
        """
        根据Solution，截断差分路线来初始化状态差分是否可知
        """
        solution = self.solution
        # for i in range(16):
        index_sr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]

        ## 根据solution截断差分路线设置已知或位置差分
        ## 1 为已知非零差分
        ## -1 为已知零差分
        ## 0 为未知差分

        ## solution中为1表示，这个字节差分非零，也就是将x_know_diff_state设为未知差分
        for i in range(len(solution) - 1):
            # print(i)
            for j in range(16):
                if solution[i][j] == 1:
                    self.x_know_diff_state[i][j] = 0

            ## y_know_diff_state 的差分由x_know_diff_state循环移位得到
            x_after_sr = []
            for j in range(16):
                x_after_sr.append(self.x_know_diff_state[i][index_sr[j]])
            self.y_know_diff_state.append(x_after_sr)

            ## z_know_diff_state 的差分由solutiuon确定，是进过MC之后的状态差分
            # print(len(self.z_know_diff_state))
            # print(len(solution)-1)
            for j in range(16):
                if solution[i + 1][j] == 1:
                    self.z_know_diff_state[i][j] = 0

        for i in range(16):
            if solution[-1][i] == 1:
                self.x_know_diff_state[-1][i] = 0

        x_after_sr = []
        for j in range(16):
            x_after_sr.append(self.x_know_diff_state[-1][index_sr[j]])
        self.y_know_diff_state.append(x_after_sr)

        # print(self.x_know_diff_state)
        # print(self.y_know_diff_state)
        # print(self.z_know_diff_state)

    def value_mds(self):
        content = "#值的mds关系\n"
        ## 值的mds关系
        ## 值则需要将所有的状态加入
        for r in range(self.rounds - 1):
            for i in range(4):
                # if self.mds_is_active[r][i]==1:
                content += self.mds_relation(
                    self.y_value_state[r][4 * i : 4 * i + 4]
                    + self.z_value_state[r][4 * i : 4 * i + 4],
                    4,
                )
        return content

    def sbox_value(self):
        content = "#S盒连接值\n"
        ## 已知S盒输入或输出可以推出对应的输出或输入
        for r in range(self.rounds):
            for i in range(16):
                # if self.x_know_diff_state[r][i]==-1:
                content += f"{self.x_value_state[r][self.index_sr[i]]}, {self.y_value_state[r][i]}\n"
        return content

    def generate_relations(self):
        index_sr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
        content = ""
        content += "connection relations\n"

        ## 建立Inbound阶段中每一轮的MDS矩阵前后的差分关系
        ## 最后一轮的MDS矩阵可以省略
        content += "#差分的mds 关系\n"
        ## 差分的mds 关系
        for r in range(self.rounds - 1):
            for i in range(4):
                ## 只要将活跃的列或行加入即可
                if self.mds_is_active[r][i] == 1:
                    temp_y = []
                    temp_z = []
                    for j in range(4):
                        ## 只用将未知状态差分加入即可
                        if self.y_know_diff_state[r][i * 4 + j] == 0:
                            temp_y.append(self.y_diff_state[r][i * 4 + j])
                        if self.z_know_diff_state[r][i * 4 + j] == 0:
                            temp_z.append(self.z_diff_state[r][i * 4 + j])
                    n_vars = len(temp_y + temp_z) - self.mds_size
                    # content+=self.mds_relation(self.y_diff_state[r][4*i:4*i+4]+self.z_diff_state[r][4*i:4*i+4])
                    content += self.mds_relation(temp_y + temp_z, n_vars)

        content += "#值的mds关系\n"
        ## 值的mds关系
        ## 值则需要将所有的状态加入
        for r in range(self.rounds - 1):
            for i in range(4):
                # if self.mds_is_active[r][i]==1:
                content += self.mds_relation(
                    self.y_value_state[r][4 * i : 4 * i + 4]
                    + self.z_value_state[r][4 * i : 4 * i + 4],
                    4,
                )
                # temp_y=[]
                # temp_z=[]
                # for j in range(4):
                #     if self.y_know_diff_state[r][i*4+j]==0:
                #         temp_y.append(self.y_value_state[r][i*4+j])
                #     if self.z_know_diff_state[r][i*4+j]==0:
                #         temp_z.append(self.z_value_state[r][i*4+j])

                # content+=self.mds_relation(temp_y+temp_z)

        content += "#S盒差分和值的关系\n"
        ## S盒差分和值的关系
        ## 因为知道非零兼容差分可以推出S盒输入输出值，所以可以建立关系
        for r in range(self.rounds):
            # for i in range(4):
            dx_vars = []
            dy_vars = []
            vx_vars = []
            vy_vars = []
            for i in range(16):
                ## 对于非零差分可建立关系
                if self.x_know_diff_state[r][index_sr[i]] == 0:
                    dx_vars.append(self.x_diff_state[r][index_sr[i]])
                    vx_vars.append(self.x_value_state[r][index_sr[i]])
                if self.y_know_diff_state[r][i] == 0:
                    dy_vars.append(self.y_diff_state[r][i])
                    vy_vars.append(self.y_value_state[r][i])
            # print(dx_vars)
            # print(dy_vars)
            # print(vx_vars)
            # print(vy_vars)
            content += self.diff2value(dx_vars, dy_vars, vx_vars, vy_vars)

        content += "#S盒连接值\n"
        ## 已知S盒输入或输出可以推出对应的输出或输入
        for r in range(self.rounds):
            # print(self.x_know_diff_state[r])
            for i in range(16):
                if self.x_know_diff_state[r][index_sr[i]] == -1:
                    content += f"{self.x_value_state[r][index_sr[i]]}, {self.y_value_state[r][i]}\n"
        # for i in range(16):
        #     # if self.x_know_diff_state[1][]
        #     content+=f"{self.x_value_state[2][index_sr[i]]}, {self.y_value_state[2][i]}\n"

        content += "#轮差分之间连接的关系\n"
        ## 轮差分关系的连接
        ## 例：dZ1=dX1
        for r in range(self.rounds - 1):
            for i in range(4):
                # if self.mds_is_active[r][i]==1:
                for j in range(4):
                    if self.x_know_diff_state[r + 1][i * 4 + j] == 0:
                        content += f"{self.x_diff_state[r+1][i*4+j]}, {self.z_diff_state[r][i*4+j]}\n"
            # for i in range(16):
            # if self.z_know_diff_state[r][i]==0:
            #     content += f"{self.x_diff_state[r+1][i]}, {self.z_diff_state[r][i]}\n"

        return content

    def add_key_sch_relations(self):

        content = "#部分轮密钥经过S盒\n"
        ## 根据密钥生成算法建立关系
        for r in range(len(self.key_state) - 1):
            for i in range(4):
                content += f"{self.key_state[r][12+i]}, s{self.key_state[r][12+i]}\n"

        content += "#轮密钥与状态之间关系添加\n"
        ## 轮密钥的关系添加
        ## 不同Inbound 连接出加上全部的key与状态关系，Inbound内部只加上有差分的状态关系
        # content+="algebraic relations\n"
        # for r in range(self.rounds-1):
        #     for i in range(16):
        #         if self.z_know_diff_state[r][i]==0:
        #             content += f"{self.z_value_state[r][i]} + {self.x_value_state[r+1][i]} + {self.key_state[r][i]}\n"

        # for n in range(self.n_inbound):
        #     begin_r=0
        #     if n!=0:
        #         begin_r=sum(self.inbound_cover_round[:n])
        #     end_r=sum(self.inbound_cover_round[:n+1])
        #     print(begin_r,end_r)
        for r in range(self.rounds - 1):
            for i in range(16):
                # if self.z_know_diff_state[r][i]==0:
                # content += f"{self.z_value_state[r][i]} + {self.x_value_state[r+1][i]} + {self.key_state[r][i]}\n"
                content += f"{self.z_value_state[r][i]}, {self.x_value_state[r+1][i]}, {self.key_state[r][i]}\n"
        # for r in range(1):
        #     for i in range(16):
        #         content += f"{self.z_value_state[r][i]} + {self.x_value_state[r+1][i]} + {self.key_state[r][i]}\n"
        # for r in range(1,2):
        #     for i in range(16):
        #         if self.z_know_diff_state[r][i]==0:
        #             content += f"{self.z_value_state[r][i]} + {self.x_value_state[r+1][i]} + {self.key_state[r][i]}\n"
        # for r in range(2,3):
        #     for i in range(16):
        #         if self.z_know_diff_state[r][i]==0:
        #             content += f"{self.z_value_state[r][i]} + {self.x_value_state[r+1][i]} + {self.key_state[r][i]}\n"

        content += "#轮密钥之间关系添加\n"
        for r in range(1, len(self.key_state)):
            # content += f"{self.key_state[r][3]} + s{self.key_state[r-1][12]} + {self.key_state[r-1][3]}\n"
            content += f"{self.key_state[r][3]}, s{self.key_state[r-1][12]}, {self.key_state[r-1][3]}\n"
            for i in range(3):
                # content += f"{self.key_state[r][i]} + s{self.key_state[r-1][13+i]} + {self.key_state[r-1][i]}\n"
                content += f"{self.key_state[r][i]}, s{self.key_state[r-1][13+i]}, {self.key_state[r-1][i]}\n"
            for i in range(1, 4):
                for j in range(4):
                    # content += f"{self.key_state[r][i*4+j]} + {self.key_state[r][(i-1)*4+j]} + {self.key_state[r-1][i*4+j]}\n"
                    content += f"{self.key_state[r][i*4+j]}, {self.key_state[r][(i-1)*4+j]}, {self.key_state[r-1][i*4+j]}\n"

        return content

    # def add_know_vars(self):
    #     content="#设置零差分\n"
    #     for r in range(self.rounds-1):
    #         for i in range(4):
    #             if self.mds_is_active[r][i]==1:
    #                 for j in range(4):
    #                     if self.y_know_diff_state[r][4*i+j]==-1:
    #                         content += f"{self.y_diff_state[r][i*4+j]}\n"
    #                 for j in range(4):
    #                     if self.z_know_diff_state[r][4*i+j]==-1:
    #                         content += f"{self.z_diff_state[r][4*i+j]}\n"
    #                 for j in range(4):
    #                     if self.x_know_diff_state[r+1][4*i+j]==-1:
    #                         content += f"{self.x_diff_state[r+1][4*i+j]}\n"
    #     return content

    def set_know_value(self):
        content = "#设置已知值\n"

        for r in range(self.rounds):
            for i in range(16):
                # if self.x_know_diff_state[0][i]==0 or self.x_know_diff_state[0][i]==-1:
                if self.x_know_diff_state[r][i] == 0:
                    content += f"{self.x_value_state[r][i]}\n"
            for i in range(16):
                if self.y_know_diff_state[r][i] == 0:
                    content += f"{self.y_value_state[r][i]}\n"

        # for n in range(self.n_inbound-1):
        #     tmp=sum(self.inbound_cover_round[:n+1])-1
        #     # print(tmp)
        #     # print(self.z_know_diff_state[tmp])
        #     for i in range(16):
        #         if self.z_know_diff_state[tmp][i]==0:
        #             content +=f"{self.z_diff_state[tmp][i]}\n"
        # for i in range(16):
        #     if self.z_know_diff_state[2][i]==0:
        #         content +=f"{self.z_diff_state[2][i]}\n"

        # for i in range(16):
        #     if self.y_know_diff_state[-1][i]==0:
        #         content += f"{self.y_diff_state[-1][i]}\n"
        # content+="dx_0_5\ndx_0_10\ndx_0_15\n"
        # content+="dy_1_0\ndy_1_10\n"
        return content

    def set_init_diff(self):
        content = "#设置初始差分\n"
        for i in range(16):
            # if self.x_know_diff_state[0][i]==0 or self.x_know_diff_state[0][i]==-1:
            if self.x_know_diff_state[0][i] == 0:
                content += f"{self.x_diff_state[0][i]}\n"
        for n in range(self.n_inbound - 1):
            tmp = sum(self.inbound_cover_round[: n + 1]) - 1
            # print(tmp)
            # print(self.z_know_diff_state[tmp])
            for i in range(16):
                if self.z_know_diff_state[tmp][i] == 0:
                    content += f"{self.z_diff_state[tmp][i]}\n"
        # for i in range(16):
        #     if self.z_know_diff_state[2][i]==0:
        #         content +=f"{self.z_diff_state[2][i]}\n"

        for i in range(16):
            if self.y_know_diff_state[-1][i] == 0:
                content += f"{self.y_diff_state[-1][i]}\n"
        # content+="dx_0_5\ndx_0_10\ndx_0_15\n"
        # content+="dy_1_0\ndy_1_10\n"
        return content

    # def set_target(self):
    #     content="target\n"
    #     # for r in range(self.rounds-1):
    #     #     for i in range(16):
    #     #         if self.z_know_diff_state[r][i]==0:
    #     #             content+=f"{self.key_state[r][i]}\n"
    #     #             content+=f"{self.x_diff_state[r+1][i]}\n"

    #     for r in range(self.rounds-1):
    #         for i in range(16):
    #             content+=f"{self.x_value_state[r][i]}\n"
    #             content+=f"{self.y_value_state[r][i]}\n"
    #             content+=f"{self.z_value_state[r][i]}\n"

    #     return content

    def not_guessed(self):
        content = "not guessed\n"
        for r in range(self.rounds):
            for i in range(16):
                if self.x_know_diff_state[r][i] == -1:
                    content += f"{self.x_value_state[r][i]}\n"
            for i in range(16):
                if self.y_know_diff_state[r][i] == -1:
                    content += f"{self.y_value_state[r][i]}\n"

        for r in range(self.rounds - 1):
            for i in range(16):
                # if self.z_know_diff_state[r][i]
                content += f"{self.z_value_state[r][i]}\n"

        # for i in range(16):
        #     content+=f"{self.x_value_state[-1][i]}\n"
        #     content+=f"{self.y_value_state[-1][i]}\n"

        # for i in range(16):
        #     if self.y_know_diff_state[1][i]==0:
        #         content+=f"{self.y_diff_state[2][i]}\n"
        #     if self.z_know_diff_state[1][i]==0:
        #         content+=f"{self.z_diff_state[2][i]}\n"

        # for i in range(16):
        #     content+=f"{self.key_state[2][i]}\n"

        # for i in range(16):
        #     if i!=0 or i!=4:
        #         content+=f"{self.key_state[1][i]}\n"

        # for i in range(16):
        #     if i!=6:
        #         content+=f"{self.key_state[0][i]}\n"

        # for r in range(len(self.key_state)-1):
        #     for i in range(4):
        #         content += f"s{self.key_state[r][12+i]}\n"

        return content

    def make_model(self):
        ## 设置初始状态差分
        self.init_diff_state()
        ## 生成各个关系
        # content=self.generate_relations()
        content = "connection relations\n"

        content += self.sbox_value()
        ## 添加轮密钥之间的关系
        content += self.add_key_sch_relations()
        content += self.value_mds()

        ## 添加已知差分和值
        content += "known\n"
        content += self.set_know_value()
        # content+=self.add_know_vars()
        # content+=self.set_init_diff()
        # content+=self.set_target()
        content += self.not_guessed()

        # content+="target\n"
        # contetn+="x_2_4\nx_2_9\nx_2_12\n"
        content += "end"

        folder_path = self.folder_path
        # folder_path="Test"
        self.filename = f"inputfile.txt"
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)
        with open(f"{folder_path}/{self.filename}", "w+") as file:
            file.write(content)

    def solver(self):
        file_path = os.getcwd()
        # print(file_path)
        # command=["python3","autoguess.py",f"-i",f"{self.folder_path}/{self.filename}",
        #          "-o",f"{self.folder_path}/outputfile",
        #         # f"-mg","6",f"-ms", "4","-s", "sat","-sats" ,"cadical153"]
        #          f"-mg",f"{self.maxguess}",f"-ms", f"{self.maxstep}","-s", "sat","-sats" ,"cadical153","-log","1","-logf",f"{self.folder_path}/temp"]
        #         # f"-mg",f"{self.maxguess}",f"-ms", f"{self.maxstep}","-s", "sat","-sats" ,"cadical153"]
        # print(command)
        gdsat = ReduceGDtoSAT(
            inputfile_name=f"{self.folder_path}/{self.filename}",
            outputfile_name=f"{self.folder_path}/outputfile",
            max_guess=self.maxguess,
            max_steps=self.maxstep,
            sat_solver="cadical153",
            # tikz=parameters['tikz'],
            # preprocess=parameters['preprocess'],
            # D=parameters['D'],
            # dglayout=parameters['dglayout'],
            log=1,
            logf=f"{self.folder_path}/temp",
        )
        gdsat.make_model()
        # gdsat.time_limit = parameters['timelimit']
        result = gdsat.solve_via_satsolver()
        # return subprocess.run(command,cwd="/home/minions/tools/autoguess-main/",capture_output=True, text=True),self.folder_path
        return result, self.folder_path

    def remove_foler(self):
        shutil.rmtree(self.folder_path)

    def check_output_file(self):
        # print(os.getcwd())
        with open(f"{self.folder_path}/outputfile.txt", "r") as file:
            # with open(f"Test/outputfile.txt",'r') as file:
            lines = file.readlines()
            for line in lines:
                # if "The following variables can be deduced from multiple paths:" in line:
                if "k" in line and "can be deduced from:" in line:
                    return False
                if "v" in line and "can be deduced from:" in line:
                    return False
            return True


# solution1=[[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# active_column1=[[1,0,0,0]]
# solution2=[[0,1,0,1,0,0,1,1,1,1,0,1,0,1,1,0],[0,0,0,0,1,0,1,0,0,1,0,1,1,0,1,0]]
# active_column2=[[0,1,1,1]]
# solution3=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,1,0,1,0,0,1,1,1,1,0,1,0,1,1,0],[0,0,0,0,1,0,1,0,0,1,0,1,1,0,1,0]]
# active_column3=[[1,1,1,1],[0,1,1,1]]

# Test1=KeySolveSuperSB(3,solution3,active_column3,14,20)

# Test1.make_model()
# Test1.solver()
