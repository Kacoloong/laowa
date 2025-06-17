import json
from src.analyze1_rebound.milp_rebound_friendly_trunted_diff_path import MILPFindReboundPath
from src.analyze1_rebound.trunted_diff_path2_tex import sol2tex, sols2tex
from src.analyze1_rebound.cipher_analy import Cipher
from src.analyze1_rebound.ulity import *
import os
import subprocess
import math

class Worker:

    def __init__(
        self,
        cipher_feature,
        input_rounds,
        inbound_begin,
        inbound_end,
        num_subinbound,
        inbound_cover,
        num_solution,
        current_dir,
        # file_path,
    ):
        self.cipher_feature = cipher_feature
        self.input_rounds = input_rounds
        self.inbound_begin = inbound_begin
        self.inbound_end = inbound_end
        self.num_subinbound = num_subinbound
        self.inbound_cover = inbound_cover
        self.num_solution = num_solution
        # self.file_path = file_path
        self.current_dir = current_dir
        self.results = []

    def generate_cipher(self):
        # cipher_feature = []
        # with open(self.file_path, "r", encoding="utf-8") as file:
        #     file_content = file.readlines()
        #     for line in file_content:
        #         cipher_feature.append(line.strip().split(":")[1])
        cipher_feature = self.cipher_feature
        # print(cipher_feature)

        # self.cipher_name = cipher_feature[0]
        self.cipher_name = cipher_feature["cipher_name"]
        # print(self.cipher_name)
        # print(type(self.cipher_name))
        # self.cipher_state = list(map(lambda x: int(x), cipher_feature[1].split(",")))

        self.cipher_state=cipher_feature["cipher_state"]
        # print(self.cipher_state)
        # print(type(self.cipher_state))
        # print(type(self.cipher_state[0]))
        # self.cipher_sbox = list(map(lambda x: int(x), cipher_feature[2].split(",")))
        self.cipher_sbox=cipher_feature["cipher_sbox"]
        # print(self.cipher_sbox)
        # print(type(self.cipher_sbox))
        # print(type(self.cipher_sbox[0]))
        self.cipher_state_size = int(math.log2(len(self.cipher_sbox)))
        # print(self.cipher_state_size)
        # print(type(self.cipher_state_size))
        # cipher_mds_list = list(map(lambda x: int(x), cipher_feature[3].split(",")))
        # cipher_mds_list=cipher_feature["cipher_mds"]
        # cipher_mds_list=list(map(lambda x: int(x), cipher_feature["cipher_mds"].split(",")))
        cipher_mds_list=cipher_feature["cipher_mds"]
        # print(cipher_mds_list)
        # print(type(cipher_mds_list[0]))
        self.cipher_mds = [
            cipher_mds_list[i : i + self.cipher_state[1]]
            for i in range(0, len(cipher_mds_list), self.cipher_state[0])
        ]
        # print(self.cipher_mds)
        # self.cipher_shift = list(map(lambda x: int(x), cipher_feature[4].split(",")))
        self.cipher_shift=cipher_feature["cipher_shift"]
        # print(self.cipher_shift)
        # print(type(self.cipher_shift))
        # print(type(self.cipher_shift[0]))
        # if cipher_feature[5] == "列混淆行移位":
        if cipher_feature["cipher_mrmc"] == "列混淆行移位":
            self.cipher_mc_mr =0
        else:
            self.cipher_mc_mr =1
        # self.cipher_key_size = int(cipher_feature[6])
        self.cipher_key_size=cipher_feature["cipher_rcsize"]

        # if cipher_feature[7]=="最后一轮不含线性变换":
        if cipher_feature["cipher_lastround"]=="最后一轮不含线性变换":
            self.cipher_last_mix=0
        else:
            self.cipher_last_mix=1

        # print(self.cipher_mc_mr,self.cipher_last_mix)
        self.cipher = Cipher(
            self.cipher_name,
            self.cipher_state,
            self.cipher_state_size,
            self.cipher_sbox,
            self.cipher_mds,
            self.cipher_shift,
            self.cipher_mc_mr,
            self.cipher_last_mix,
            self.cipher_key_size,
        )
        # print(self.cipher)

    def analyze_without_super_sbox(self):
        results = []
        for i in range(self.input_rounds):
            self.inbound_begin = i
            self.inbound_end = i
            self.num_subinbound = 1
            self.inbound_cover = [1]
            result = self.get_truncated_diff_path()
            results.append(result)
            self.results.append(result)
        return results

    def analyze_with_super_sbox(self):
        results = []
        for i in range(self.input_rounds - 1):
            self.inbound_begin = i
            self.inbound_end = i + 1
            self.num_subinbound = 1
            self.inbound_cover = [2]
            result = self.get_truncated_diff_path()
            results.append(result)
            self.results.append(result)
        return results

    def get_truncated_diff_path(self):
        self.generate_cipher()
        # print("worker path:", self.current_dir)
        os.chdir(self.current_dir)
        os.makedirs(f"./ciphers/{self.cipher_name}", exist_ok=True)
        os.chdir(f"./ciphers/{self.cipher_name}")

        # content_rebound_para = {
        #     "Rebound分析轮数": self.input_rounds,
        #     "Rebound分析Inbound阶段": f"从第{self.inbound_begin}轮开始到第{self.inbound_end}轮结束",
        #     "SubInbound个数": self.num_subinbound,
        #     "SubInbound轮数分布": self.inbound_cover,
        # }

        td_path = MILPFindReboundPath(
            self.cipher.cipher_name,
            self.cipher.cipher_state,
            self.cipher.cipher_state_size,
            self.cipher.cipher_mds,
            self.cipher.cipher_shift,
            self.cipher.cipher_mc_mr,
            self.cipher.cipher_last_mix,
            self.cipher.cipher_key_size,
            self.input_rounds,
            self.inbound_begin,
            self.inbound_end,
        )

        if self.num_solution == 1:
            result = td_path.solver()
            # print(result)
            if result is not None:
                solution, mds_solution, pr, c_model_time, s_model_time = result
                analysis_result = {
                    # "input_rounds":self.input_rounds,
                    # "inbound_begin":self.inbound_begin,
                    # "inbound_end":self.inbound_end,
                    # "num_subinbound":self.num_subinbound,
                    # "inbound_cover":self.inbound_cover,
                    "c_model_time": c_model_time,
                    "s_model_time": s_model_time,
                    "solution": solution,
                    "pr": f"2^{{-{pr}}}",
                    "start_point": f"2^{{{pr}}}",
                }
                if self.num_subinbound == 1:
                    if self.inbound_cover[0] == 1:
                        analysis_result["time"] = f"2^{{{pr}}}"
                        analysis_result["memory"] = f"2^{{{self.cipher_state_size * 2}}}"
                    if self.inbound_cover[0] == 2:
                        analysis_result["time"] = f"2^{{{pr}}}"
                        if all(x == 1 for x in mds_solution[self.inbound_begin]):
                            analysis_result["memory"] = f"2^{{{self.cipher_state_size * self.cipher_state[0]}}}"
                        else:
                            analysis_result["memory"] = f"2^{{{self.cipher_state_size * 2}}}"
                else:
                    analysis_result["time"] = f"2^{{{pr}}}"

                folder_path = sol2tex(
                    solution,
                    self.cipher,
                    self.input_rounds,
                    self.inbound_begin,
                    self.inbound_end,
                    self.num_subinbound,
                    self.inbound_cover,
                    1,
                    self.current_dir,
                )
                # print("folder_path:",folder_path)
                output_pdf_path=os.path.join(os.getcwd(),folder_path)
                # print("output_pdf_path:",output_pdf_path)
                command = [
                    "pdflatex",
                    f"-output-directory={output_pdf_path}",
                    f"{output_pdf_path}/main.tex",
                ]
                # print(command)
                result = subprocess.run(command, capture_output=True, text=True)

                pdf_file = f"{os.getcwd()}/{folder_path}/main.pdf"
                analysis_result["pdf_file"] = pdf_file

                return analysis_result
                # return {
                #     # "success": True,
                #     # "cipher_name": self.cipher_name,
                #     # "content_rebound_para": content_rebound_para,
                #     "analysis_result": analysis_result,
                #     # "pdf_file": pdf_file,
                # }
            else:
                return {
                    # "success": False,
                    "error": "未找到满足条件的截断差分路径，请选择其他轮数进行输入。",
                }
        else:
            result = td_path.solvers(self.num_solution)
            if result is not None:
                solution, mds_solution, pr, c_model_time, s_model_time, number_sol = result
                analysis_result = {
                    # "input_rounds":self.input_rounds,
                    # "inbound_begin":self.inbound_begin,
                    # "inbound_end":self.inbound_end,
                    # "num_subinbound":self.num_subinbound,
                    # "inbound_cover":self.inbound_cover,
                    "c_model_time": c_model_time,
                    "s_model_time": s_model_time,
                    # "number_of_solutions": number_sol,
                    "solutions": [],
                }
                for i in range(number_sol):
                    solution_details = {
                        "path": i + 1,
                        "solution": solution[i],
                        "pr": f"2^{{-{pr}}}",
                        "start_point": f"2^{{{pr}}}个",
                    }
                    if self.num_subinbound == 1:
                        if self.inbound_cover[0] == 1:
                            solution_details["time"] = f"2^{{{pr}}}"
                            solution_details["memory"] = f"2^{{{self.cipher_state_size}}}"
                        if self.inbound_cover[0] == 2:
                            if all(x == 1 for x in mds_solution[self.inbound_begin]):
                                solution_details["memory"] = f"2^{{{self.cipher_state_size * self.cipher_state[0]}}}"
                            else:
                                solution_details["memory"] = f"2^{{{self.cipher_state_size * 2}}}"
                    else:
                        solution_details["time"] = f"2^{{{pr}}}，还需要考虑连接多个Inbound阶段的时间复杂度。"

                    analysis_result["solutions"].append(solution_details)

                folder_paths = sols2tex(
                    solution,
                    self.cipher,
                    self.input_rounds,
                    self.inbound_begin,
                    self.inbound_end,
                    self.num_subinbound,
                    self.inbound_cover,
                    self.current_dir,
                    number_sol,
                )

                pdf_files = []
                for p in folder_paths:
                    command = [
                        "pdflatex",
                        f"-output-directory={os.getcwd()}/{p}",
                        f"{os.getcwd()}/{p}/main.tex",
                    ]
                    subprocess.run(command, capture_output=True, text=True)
                    pdf_files.append(f"{os.getcwd()}/{p}/main.pdf")

                analysis_result["pdf_files"] = pdf_files

                return analysis_result
                # return {
                    # "success": True,
                    # "cipher_name": self.cipher_name,
                    # "content_rebound_para": content_rebound_para,
                    # "analysis_result": analysis_result,
                    # "pdf_files": pdf_files,
                # }
            else:
                return {
                    # "success": False,
                    "error": "未找到满足条件的截断差分路径，请选择其他轮数进行输入。",
                }
