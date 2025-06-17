import json


class MitmSolutionToTikz:
    def __init__(self, filepath):
         # 使用 with 语句安全打开并读取 JSON 文件
        with open(filepath, 'r') as file:
            self.mitm_solution = json.load(file)
        self.WhiteColor = "white"
        self.GrayColor = "lightgray"
        self.BlueColor = "blue"
        self.RedColor = "red"
        self.PurpleColor = "green!60"
        self.rho = [
            [0, 36, 3, 41, 18],
            [1, 44, 10, 45, 2],
            [62, 6, 43, 15, 61],
            [28, 55, 25, 21, 56],
            [27, 20, 39, 8, 14]
        ]

    def generate(self):
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
            for k in range(64):
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
                for k in range(64):
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
                    for i in range (5):
                        if self.mitm_solution["DC1"][round][i][k] == 1:
                            consumered += 1
                            output += f"\\draw[line width=2pt, color=yellow] ({6 * k + i},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                   
                output += f"\\fill[color={self.RedColor}] ({6 * 63 + 4 + 4},{25 * (rounds - round) + 15})  rectangle ++(1,1);\n"
                output += f"\\draw({6 * 63 + 4 + 4},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                output += f"\\node[align=center] at ({6 * 63 + 4 + 2.5},{25 * (rounds - round) + 15.4}) {{\\textbf{{\\huge - {consumered}}}}};\n"

                # DP2
                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 13.5})[scale=1.5]{{\\textbf{{\\huge $D^{{({round + 1})}}$}}}};\n"
                print(f"Drawing D for Round {round + 1}")
                consumered = 0
                for k in range(64):
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
                output += f"\\fill[color={self.RedColor}] ({6 * 63 + 4 + 4},{25 * (rounds - round) + 13})  rectangle ++(1,1);\n"
                output += f"\\draw({6 * 63 + 4 + 4},{25 * (rounds - round) + 13})  grid ++(1,1);\n"
                output += f" \\node[align=center] at ({6 * 63 + 4 + 2.5},{25 * (rounds - round) + 13.4}) {{\\textbf{{\\huge - {consumered}}}}};\n"

                # DB after theta
                
                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 9.5})[scale=1.5]{{\\textbf{{\\huge $\\theta^{{({round + 1})}}$}}}};\n"
                print(f"Drawing theta for Round {round + 1}")
                for k in range(64):
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
                            output += f"\\fill[color={color}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + 64) % 64) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 7}) rectangle ++(1,1);\n"
                for k in range(64):
                    output += f"\\draw({6 * k},{25 * (rounds - round) + 7}) grid ++(5,5);\n"

                consumered = 0
                for k in range(64):
                    for i in range(5):
                        for j in range(5):
                            if self.mitm_solution["DC2"][round][i][j][k] == 1:
                                consumered += 1
                                output += f"\\draw[line width=2pt, color=yellow] ({6 * k + i},{25 * (rounds - round) + (4 - j) + 7}) grid ++(1,1);\n"
                output += f"\\fill[color={self.RedColor}] ({6 * 63 + 4 + 4},{25 * (rounds - round) + 9})  rectangle ++(1,1);\n"
                output += f"\\draw({6 * 63 + 4 + 4},{25 * (rounds - round) + 9})  grid ++(1,1);\n"
                output += f" \\node[align=center] at ({6 * 63 + 4 + 2.5},{25 * (rounds - round) + 9.4}) {{\\textbf{{\\huge - {consumered}}}}};\n"

                # DB
                output += f" \\node[align=center] at ({-2},{25 * (rounds - round) + 2.5})[scale=1.5]{{\\textbf{{\\huge $\\pi^{{({round + 1})}}$}}}};\n"
                print(f"Drawing pai for Round {round + 1}")
                for k in range(64):
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
            for k in range(64):
                if self.mitm_solution["dom"][0][k] == 1:
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[3][0] + 64) % 64) + 3 + 0.5},{18 + 4 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[3][0] + 64) % 64) + 3 + 0.5},{18 + 1 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[0][2] + 64) % 64) + 0 + 0.5},{18 + 2 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[0][2] + 64) % 64) + 0 + 0.5},{18 + 4 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                if self.mitm_solution["dom"][1][k] == 1:
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[4][1] + 64) % 64) + 4 + 0.5},{18 + 3 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[4][1] + 64) % 64) + 4 + 0.5},{18 + 0 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[1][3] + 64) % 64) + 1 + 0.5},{18 + 1 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
                    output += f"\\node[align=center] at ({6 * ((k - self.rho[1][3] + 64) % 64) + 1 + 0.5},{18 + 3 + 0.5}){{\\textbf{{\\Large $m$}}}};\n"
            output += "\n"            
        # 处理 round == -1 的情况
        round = -1
        if round == -1:
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 20.5}) [scale=1.5]{{\\textbf{{\\huge $A^{{({round + 1})}}$}}}};\n"
            for k in range(64):
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
                            output += f"\\fill[color={color}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + 64) % 64) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 18}) rectangle ++(1,1);\n"
                        else:
                            output += f"\\fill[color={self.GrayColor}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + 64) % 64) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 18}) rectangle ++(1,1);\n"
            for k in range(64):
                output += f"\\draw({6 * k},{25 * (rounds - round) + 18}) grid ++(5,5);\n"
                output += f" \\node[align=center] at ({6 * k + 2},{25 * (rounds - round) + 17})[scale=2] {{\\Large z={k}}};\n"
            
            allred = 0
            allblue = 0
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 15.5})[scale=1.5]{{\\textbf{{\\huge $C^{{({round + 1})}}$}}}};\n"
            for k in range(64):
                for i in range(5):
                    output += f"\\fill[color={self.GrayColor}] ({6 * k + i},{25 * (rounds - round) + 15}) rectangle ++(1,1);\n"
                output += f"\\draw({6 * k},{25 * (rounds - round) + 15}) grid ++(5,1);\n"
            for k in range(64):
                if self.mitm_solution["DA"][round + 1][0][0][k] == [0, 1, 1]:
                    allred += 1
                    output += f"\\draw[line width=2pt, color=yellow]({6 * k},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                if self.mitm_solution["DA"][round + 1][0][0][k] == [1, 1, 0]:
                    allblue += 1
                    output += f"\\draw[line width=2pt, color=black]({6 * k},{25 * (rounds - round) + 15}) grid ++(1,1);\n"
                if self.mitm_solution["DA"][round + 1][1][0][k] == [0, 1, 1]:
                    allred += 1
                    output += "\\draw[line width=2pt, color=yellow](" + str(6 * ((k - self.rho[1][1] + 64) % 64) + 1) + "," + str(25 * (rounds - round) + 15) + ") grid ++(1,1);\n"
                if self.mitm_solution["DA"][round + 1][1][0][k] == [1, 1, 0]:
                    allblue += 1
                    output += "\\draw[line width=2pt, color=black](" + str(6 * ((k - self.rho[1][1] + 64) % 64) + 1) + "," + str(25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][1][2][k] == [0, 1, 1]:
                    allred += 1
                    output += "\\draw[line width=2pt, color=yellow](" + str(6 * ((k - self.rho[2][1] + 64) % 64) + 2) + "," + str(25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][1][2][k] == [1, 1, 0]:
                    allblue += 1
                    output += "\\draw[line width=2pt, color=black](" + str(6 * ((k - self.rho[2][1] + 64) % 64) + 2) + "," + str(25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][0][1][k] == [0, 1, 1]:
                    allred += 1
                    output += "\\draw[line width=2pt, color=yellow](" + str(6 * ((k - self.rho[3][0] + 64) % 64) + 3) + "," + str(25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

                if self.mitm_solution["DA"][round + 1][0][1][k] == [1, 1, 0]:
                    allblue += 1
                    output += "\\draw[line width=2pt, color=black](" + str(6 * ((k - self.rho[3][0] + 64) % 64) + 3) + "," + str(25 * (rounds - round) + 15) + ") grid ++(1,1);\n"

            output += f"\\fill[color={self.RedColor}] ({6 * 63 + 4 + 2},{25 * (rounds - round) + 21})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * 63 + 4 + 2},{25 * (rounds - round) + 21})  grid ++(1,1);\n"
            
            output += f" \\node[align=center] at ({6 * 63 + 4 + 4.2},{25 * (rounds - round) + 21.4}){{\\textbf{{\\huge = {allred * 2}}}}};\n"
            output += f"\\fill[color={self.BlueColor}] ({6 * 63 + 4 + 2},{25 * (rounds - round) + 19})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * 63 + 4 + 2},{25 * (rounds - round) + 19}) grid ++(1,1);\n"
            output += f" \\node[align=center] at ({6 * 63 + 4 + 4.1},{25 * (rounds - round) + 19.4}){{\\textbf{{\\huge = {allblue * 2}}}}};\n"
            
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 13.5}) [scale=1.5]{{\\textbf{{\\huge $D^{{({round + 1})}}$}}}};\n"
            for k in range(64):
                for i in range(5):
                    output += f"\\fill[color={self.GrayColor}] ({6 * k + i},{25 * (rounds - round) + 13}) rectangle ++(1,1);\n"
                output += f"\\draw({6 * k},{25 * (rounds - round) + 13}) grid ++(5,1);\n"
            output += f"\\fill[color={self.RedColor}] ({6 * 63 + 4 + 4},{25 * (rounds - round) + 16})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * 63 + 4 + 4},{25 * (rounds - round) + 16})  grid ++(1,1);\n"
            output += f" \\node[align=center] at ({6 * 63 + 4 + 2.5},{25 * (rounds - round) + 16.4}){{\\textbf{{\\huge - {allred}}}}};\n"
            output += f"\\fill[color={self.BlueColor}] ({6 * 63 + 4 + 4},{25 * (rounds - round) + 14.5})  rectangle ++(1,1);\n"
            output += f"\\draw({6 * 63 + 4 + 4},{25 * (rounds - round) + 14.5}) grid ++(1,1);\n"
            output += f" \\node[align=center] at ({6 * 63 + 4 + 2.7},{25 * (rounds - round) + 14.9}){{\\textbf{{\\huge - {allblue}}}}};\n"

            # DB after theta
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 9.5})[scale=1.5]{{\\huge $\\theta^{{({round + 1})}}$}};\n"
            for k in range(64):
                for i in range(5):
                    for j in range(5):
                        if(i == 0 or i == 1):
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
                            output += f"\\fill[color={color}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + 64) % 64) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 7}) rectangle ++(1,1);\n"
                        else:
                            output += f"\\fill[color={self.GrayColor}] ({6 * ((k - self.rho[(i + 3 * j) % 5][i] + 64) % 64) + ((i + 3 * j) % 5)},{25 * (rounds - round) + (4 - i) + 7}) rectangle ++(1,1);\n"
                if(i == 0 and j == 0):
                    if(self.DA[round+1][0][0][k][0]==0 and self.DA[round+1][0][0][k][1]==1 and self.DA[round+1][0][0][k][2]==1 and self.DA[round+1][1][0][k][0]==0 and self.DA[round+1][1][0][k][1]==1 and self.DA[round+1][1][0][k][2]==1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";              
                    if(self.DA[round+1][0][0][k][0]==1 and self.DA[round+1][0][0][k][1]==1 and self.DA[round+1][0][0][k][2]==0 and self.DA[round+1][1][0][k][0]==1 and self.DA[round+1][1][0][k][1]==1 and self.DA[round+1][1][0][k][2]==0):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";              
                    if(self.DA[round+1][0][0][k][0]==0 and self.DA[round+1][0][0][k][1]==1 and self.DA[round+1][0][0][k][2]==1 and self.DA[round+1][1][0][k][0]==1 and self.DA[round+1][1][0][k][1]==1 and self.DA[round+1][1][0][k][2]==1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";              
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";              
                    if(self.DA[round+1][0][0][k][0]==1 and self.DA[round+1][0][0][k][1]==1 and self.DA[round+1][0][0][k][2]==1 and self.DA[round+1][1][0][k][0]==0 and self.DA[round+1][1][0][k][1]==1 and self.DA[round+1][1][0][k][2]==1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";              
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";              
                    if(self.DA[round+1][0][0][k][0]==1 and self.DA[round+1][0][0][k][1]==1 and self.DA[round+1][0][0][k][2]==0 and self.DA[round+1][1][0][k][0]==1 and self.DA[round+1][1][0][k][1]==1 and self.DA[round+1][1][0][k][2]==1):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";              
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";              
                    if(self.DA[round+1][0][0][k][0]==1 and self.DA[round+1][0][0][k][1]==1 and self.DA[round+1][0][0][k][2]==1 and self.DA[round+1][1][0][k][0]==0 and self.DA[round+1][1][0][k][1]==1 and self.DA[round+1][1][0][k][2]==0):
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n";              
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5}, {25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n";              
                if i == 0 and j == 1:
                    if self.DA[round + 1][0][1][k][0] == 0 and self.DA[round + 1][0][1][k][1] == 1 and self.DA[round + 1][0][1][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][1][k][0] == 1 and self.DA[round + 1][0][1][k][1] == 1 and self.DA[round + 1][0][1][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                if i == 0 and j == 2:
                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                    if i == 0 and j == 3:
                        if self.DA[round + 1][1][3][k][0] == 0 and self.DA[round + 1][1][3][k][1] == 1 and self.DA[round + 1][1][3][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][1][3][k][0] == 1 and self.DA[round + 1][1][3][k][1] == 1 and self.DA[round + 1][1][3][k][2] == 0:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if i == 0 and  j == 4:
                        if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 0 and self.DA[round + 1][1][4][k][0] == 1 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 0:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 1 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 0 and self.DA[round + 1][1][4][k][0] == 1 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                        if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 1 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 0:
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 2) % 5 + 3 * j) % 5][(i + 2) % 5] + 64) % 64) + (((i + 2) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 2) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                            output += f"\\node[align=center] at ({6 * ((k - self.rho[((i) % 5 + 3 * j) % 5][(i) % 5] + 64) % 64) + (((i) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i) % 5) + 7 + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                
                # for i in range(5):
                #     for j in range(5):
                #         if self.mitm_solution["DA"][round + 1][i][j][k] == [0, 1, 1]:
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n"
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n"
                #         if self.mitm_solution["DA"][round + 1][i][j][k] == [1, 1, 0]:
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 1) % 5 + 3 * j) % 5][(i + 1) % 5] + 64) % 64) + (((i + 1) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 1) % 5) + 7 + 0.5}){{\\textbf{{\\Large 0}}}};\n"
                #             output += f"\\node[align=center] at ({6 * ((k - self.rho[((i + 4) % 5 + 3 * j) % 5][(i + 4) % 5] + 64) % 64) + (((i + 4) % 5 + 3 * j) % 5) + 0.5},{25 * (rounds - round) + (4 - (i + 4) % 5) + 7 + 0.5}){{\\textbf{{\\Large 1}}}};\n"
            for k in range(64):
                output += f"\\draw({6 * k},{25 * (rounds - round) + 7}) grid ++(5,5);\n"

            # DB
            output += f" \\node[align=center] at (-2,{25 * (rounds - round) + 2.5}) [scale=1.5]{{\\textbf{{\\huge $\\pi^{{({round + 1})}}$}}}};\n"
            for k in range(64):
                for i in range(5):
                    for j in range(5):
                        if i==0 or i == 1:
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
                    if self.DA[round + 1][0][0][k][0] == 0 and self.DA[round + 1][0][0][k][1] == 1 and self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and self.DA[round + 1][0][0][k][2] == 0 and self.DA[round + 1][1][0][k][0] == 1 and self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 0 and self.DA[round + 1][0][0][k][1] == 1 and self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 1 and self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 0 and self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and self.DA[round + 1][0][0][k][2] == 0 and self.DA[round + 1][1][0][k][0] == 1 and self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][0][k][0] == 1 and self.DA[round + 1][0][0][k][1] == 1 and self.DA[round + 1][0][0][k][2] == 1 and self.DA[round + 1][1][0][k][0] == 1 and self.DA[round + 1][1][0][k][1] == 1 and self.DA[round + 1][1][0][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                if i == 0 and j == 1:
                    if self.DA[round + 1][0][1][k][0] == 0 and self.DA[round + 1][0][1][k][1] == 1 and self.DA[round + 1][0][1][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][1][k][0] == 1 and self.DA[round + 1][0][1][k][1] == 1 and self.DA[round + 1][0][1][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                if i == 0 and j == 2:
                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 0 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 0 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 0 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 1:
                        output += "\\node[align=center] at (" + str(6 * k + (i + 1) % 5 + 0.5) + "," + str(25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 0}};\n"
                        output += "\\node[align=center] at (" + str(6 * k + (i + 4) % 5 + 0.5) + "," + str(25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 1}};\n"

                    if self.DA[round + 1][0][2][k][0] == 1 and self.DA[round + 1][0][2][k][1] == 1 and self.DA[round + 1][0][2][k][2] == 1 and self.DA[round + 1][1][2][k][0] == 1 and self.DA[round + 1][1][2][k][1] == 1 and self.DA[round + 1][1][2][k][2] == 0:
                        output += "\\node[align=center] at (" + str(6 * k + i % 5 + 0.5) + "," + str(25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 1}};\n"
                        output += "\\node[align=center] at (" + str(6 * k + (i + 2) % 5 + 0.5) + "," + str(25 * (rounds - round) + (4 - j) + 0.5) + ") {\\textbf{\\Large 0}};\n"
                if i == 0 and j == 3:
                    if self.DA[round + 1][1][3][k][0] == 0 and self.DA[round + 1][1][3][k][1] == 1 and self.DA[round + 1][1][3][k][2] == 1:
                        output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                    if self.DA[round + 1][1][3][k][0] == 1 and self.DA[round + 1][1][3][k][1] == 1 and self.DA[round + 1][1][3][k][2] == 0:
                        output += f"\\node[align=center] at ({6 * k + i % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 2) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"

                    i = 0; j = 4
                    if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 0 and self.DA[round + 1][1][4][k][0] == 1 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 0:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][4][k][0] == 0 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 1 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
                        self.output += f"\\node[align=center] at ({6 * k + (i + 1) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 0}}}};\n"
                        self.output += f"\\node[align=center] at ({6 * k + (i + 4) % 5 + 0.5},{25 * (rounds - round) + (4 - j) + 0.5}) {{\\textbf{{\\Large 1}}}};\n"

                    if self.DA[round + 1][0][4][k][0] == 1 and self.DA[round + 1][0][4][k][1] == 1 and self.DA[round + 1][0][4][k][2] == 1 and self.DA[round + 1][1][4][k][0] == 0 and self.DA[round + 1][1][4][k][1] == 1 and self.DA[round + 1][1][4][k][2] == 1:
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
# 创建类的实例
tikz_generator = MitmSolutionToTikz("../mitm_solution.json")

# 生成 TikZ 代码
tikz_code = tikz_generator.generate()

# 将生成的代码写入文件
with open("output.tex", "w") as file:
    file.write(tikz_code)
print("TikZ code has been saved to output.tex")
# 创建类的实例
tikz_generator = MitmSolutionToTikz("../mitm_solution.json")

# 生成 TikZ 代码
tikz_code = tikz_generator.generate()

# 将生成的代码写入文件
with open("output.tex", "w") as file:
    file.write(tikz_code)
print("TikZ code has been saved to output.tex")
