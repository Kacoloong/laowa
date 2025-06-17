from flask import Flask, request, jsonify, send_from_directory, jsonify, send_file
from flask_cors import CORS
from src.analyze1_rebound.worker1 import Worker
import os
import threading
import uuid
import time
from asyncio import tasks
import subprocess
from uuid import uuid4
from datetime import datetime
# from mitm_4 import Mitm 
from src.analyze3_mitm.mitm_4 import Mitm
# import sha2likeCode
from src.analyze2_diff_collision import sha2likeCode
import shutil
import sys

from asyncio import tasks
# from bithash_gen import *
sys.path.extend(['', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', '/usr/local/lib/python3.10/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.10/dist-packages'])
import site
import sys
import os
import site

import argparse

from src.design1_bit.bithash_gen import *
# from bithash import *
from src.design1_bit.bithash import *
# import hash_gen
from src.design2_byte import hash_gen
# import misc
from src.design2_byte import misc1


# from sage.env import SAGE_LOCAL
# sage_root = SAGE_LOCAL
# if not sage_root:
#     raise EnvironmentError("请设置环境变量 SAGE_ROOT 指向 SageMath 安装目录")

# # 添加 SageMath 的库路径到 sys.path
# sage_lib_path = os.path.join(sage_root, 'local', 'lib', 'python%s' % sys.version[:3], 'site-packages')
# if sage_lib_path not in sys.path:
#     sys.path.append(sage_lib_path)
# print(sage_lib_path)
# # 可选：添加 SageMath 的二进制目录到 PATH
# sage_bin_path = os.path.join(sage_root, 'local', 'bin')
# os.environ['PATH'] = f"{sage_bin_path}:{os.environ['PATH']}"


app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局变量
cipher_feature = None
current = os.getcwd()
tasks = {}
def make_response(code=0, msg="success", data=None):
    return jsonify({"code": code, "msg": msg, "data": data})
def process_cipher_data(data):
    global cipher_feature
    cipher_feature={
        "cipher_name":data.get("cipher_name"),
        "cipher_state":list([data.get("cipher_nrow"),data.get("cipher_ncolumn")]),
        # list(data.get("cipher_nrow"),data.get("cipher_ncolumn")),
        "cipher_sbox":data.get("cipher_sbox"),
        "cipher_mds":data.get("cipher_mds"),
        "cipher_shift":data.get("cipher_shift"),
        "cipher_mrmc":data.get("cipher_mrmc"),
        "cipher_rcsize":data.get("cipher_rcsize"),
        "cipher_lastround":data.get("cipher_lastround"),
    }
    # cipher_feature = [
    #     data.get("cipher_name"),
    #     data.get("cipher_nrow")+","+data.get("cipher_ncolumn"),
    #     # list(data.get("cipher_nrow"),data.get("cipher_ncolumn")),
    #     data.get("cipher_sbox"),
    #     data.get("cipher_mds"),
    #     data.get("cipher_shift"),
    #     data.get("cipher_mrmc"),
    #     data.get("cipher_rcsize"),
    #     data.get("cipher_lastround"),
    # ]

def process_rebound_data(data):
    return [
        data.get("input_rounds"),
        data.get("inbound_begin"),
        data.get("inbound_end"),
        data.get("num_subinbound"),
        data.get("inbound_coverlist"),
        data.get("num_solution"),
    ]
def parameter_is_wrong(data):
    wrong_list=[]
    if not data.get("cipher_name"):
        wrong_list.append("cipher_name")
    if not data.get("cipher_nrow"):
        wrong_list.append("cipher_nrow")
    if not data.get("cipher_ncolumn"):
        wrong_list.append("cipher_ncolumn")
    if not data.get("cipher_sbox"):
        wrong_list.append("cipher_sbox")
    if not data.get("cipher_mds"):
        wrong_list.append("cipher_mds")
    if not data.get("cipher_shift"):
        wrong_list.append("cipher_shift")
    if not data.get("cipher_mrmc"):
        wrong_list.append("cipher_mrmc")
    if not data.get("cipher_lastround"):
        wrong_list.append("cipher_lastround")
    if not data.get("input_rounds"):
        wrong_list.append("input_rounds")
    if not data.get("inbound_begin"):
        wrong_list.append("inbound_begin")
    if not data.get("inbound_end"):
        wrong_list.append("inbound_end")
    if not data.get("num_subinbound"):
        wrong_list.append("num_subinbound")
    if not data.get("inbound_coverlist"):
        wrong_list.append("inbound_coverlist")
    # if not data.get("inbound_coverlist"):
    #     wrong_list.append("inbound_coverlist")
    if not data.get("num_solution"):
        wrong_list.append("num_solution")
    
    return wrong_list
def parameter_is_wrong1(data):
    wrong_list=[]
    if not data.get("cipher_name"):
        wrong_list.append("cipher_name")
    if not data.get("cipher_nrow"):
        wrong_list.append("cipher_nrow")
    if not data.get("cipher_ncolumn"):
        wrong_list.append("cipher_ncolumn")
    if not data.get("cipher_sbox"):
        wrong_list.append("cipher_sbox")
    if not data.get("cipher_mds"):
        wrong_list.append("cipher_mds")
    if not data.get("cipher_shift"):
        wrong_list.append("cipher_shift")
    if not data.get("cipher_mrmc"):
        wrong_list.append("cipher_mrmc")
    if not data.get("cipher_lastround"):
        wrong_list.append("cipher_lastround")
    if not data.get("input_rounds"):
        wrong_list.append("input_rounds")
    # if not data.get("inbound_coverlist"):
    #     wrong_list.append("inbound_coverlist")
    if not data.get("num_solution"):
        wrong_list.append("num_solution")
    
    return wrong_list

@app.route("/api/hash_function/single-rebound", methods=["POST"])
def submit_rebound():
    global cipher_feature
    try:
        if not request.is_json:
            # print(make_response(101, "请求参数异常", None))
            return make_response(101, "请求参数异常", None)
        
        data = request.get_json()
        if not data:
            # print(make_response(102,"请求参数为空", None))
            return make_response(102,"请求参数为空", None)
        # print(data)

        wrong_list=parameter_is_wrong(data)
        # print("wrong_list:",wrong_list)
        if len(wrong_list)>0:
            wrong_para_list=" ".join(wrong_list)
            # print(make_response(103,f"缺少必要参数: {wrong_para_list}", None))
            return make_response(103,f"缺少必要参数: {wrong_para_list}", None)
        
        process_cipher_data(data)

        rebound_params = process_rebound_data(data)

        # print("rebound_params:",rebound_params)
        # print(rebound_params[0],rebound_params[1],rebound_params[2],rebound_params[3],rebound_params[4],rebound_params[5])
        # print(type(rebound_params[0]),type(rebound_params[1]),type(rebound_params[2]),type(rebound_params[3]),type(rebound_params[4]),type(rebound_params[5]))
        # print(type(rebound_params[4][0]))
        # print(cipher_feature)
        # print("ok")
        # 初始化 Worker 并执行分析
        worker = Worker(
            cipher_feature=cipher_feature,
            input_rounds=rebound_params[0],
            inbound_begin=rebound_params[1],
            inbound_end=rebound_params[2],
            num_subinbound=rebound_params[3],
            inbound_cover=rebound_params[4],
            num_solution=rebound_params[5],
            current_dir=current
        )
        # print("worker:",worker)

        # print("ok")
    
        os.chdir(current)
        result = worker.get_truncated_diff_path()
        os.chdir(current)
        # print("result",result)
        # print(make_response(0,"success",result))
        return make_response(0,"success",result)
    except Exception as e:
        return make_response(104, f"系统内部错误: {str(e)}", None)

    # data = request.json
    # # app.logger.info("Received single rebound request: %s", data)
    # # print("Received single rebound request:", data)

    # # 处理 cipher 数据
    # process_cipher_data(data)

    # # 处理 rebound 参数
    # rebound_params = process_rebound_data(data)
    # # print("rebound_params[3]",rebound_params[3])
    # # print(type(rebound_params[3]))
    # # 初始化 Worker 并执行分析
    # worker = Worker(
    #     cipher_feature=cipher_feature,
    #     input_rounds=rebound_params[0],
    #     inbound_begin=rebound_params[1],
    #     inbound_end=rebound_params[2],
    #     num_subinbound=rebound_params[3],
    #     inbound_cover=list(map(lambda x: int(x), rebound_params[4].split(","))),
    #     num_solution=rebound_params[5],
    #     current_dir=current
    # )

    # os.chdir(current)
    # result = worker.get_truncated_diff_path()
    # os.chdir(current)

    # return jsonify({"id": "single-result", "result": result})

@app.route("/api/hash_function/multiple-rebound", methods=["POST"])
def analyze():
    global cipher_feature
    try:
        if not request.is_json:
            print(make_response(101, "请求参数异常", None))
            return make_response(101, "请求参数异常", None)
        
        data = request.get_json()
        if not data:
            print(make_response(102,"请求参数为空", None))
            return make_response(102,"请求参数为空", None)
        # print(data)

        wrong_list=parameter_is_wrong1(data)
        # print("wrong_list:",wrong_list)
        if len(wrong_list)>0:
            wrong_para_list=" ".join(wrong_list)
            print(make_response(103,f"缺少必要参数: {wrong_para_list}", None))
            return make_response(103,f"缺少必要参数: {wrong_para_list}", None)
        
        process_cipher_data(data)
        # 处理 rebound 参数
        input_rounds = int(data["input_rounds"])
        num_solution = int(data["num_solution"])

        # 生成唯一的任务 ID
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            "status": "running",
            "results": [],
        }
        threading.Thread(
            target=run_analysis, args=(task_id, input_rounds, num_solution)
        ).start()
        return make_response(0,"ok",{"taskId": task_id})
    except Exception as e:
        return make_response(104, f"系统内部错误: {str(e)}", None)
    # global cipher_feature

    # # data = request.json
    # # app.logger.info("Received multiple rebound request: %s", data)
    # # print("Received multiple rebound request:", data)

    # # 处理 cipher 数据
    # process_cipher_data(data)

    # # 处理 rebound 参数
    # input_rounds = int(data["input_rounds"])
    # num_solution = int(data["num_solution"])

    # # 生成唯一的任务 ID
    # task_id = str(uuid.uuid4())
    # tasks[task_id] = {
    #     "status": "running",
    #     "results": [],
    # }

    # 启动一个线程进行分析
    # threading.Thread(
    #     target=run_analysis, args=(task_id, input_rounds, num_solution)
    # ).start()

    # return jsonify({"taskId": task_id})

def run_analysis(task_id, input_rounds, num_solution):
    os.chdir(current)
    global cipher_feature

    try:
        for r in range(2, input_rounds + 1):
            # print("r:", r)
            os.chdir(current)
            for i in range(r):
                # print("single sbox:", i)
                worker = Worker(
                    cipher_feature=cipher_feature,
                    input_rounds=r,
                    inbound_begin=i,
                    inbound_end=i,
                    num_subinbound=1,
                    inbound_cover=[1],
                    num_solution=num_solution,
                    current_dir=current,
                )
                result = worker.get_truncated_diff_path()
                os.chdir(current)
                tasks[task_id]["results"].append({"id": f"inbound-{i}", "result": result})

            for i in range(r - 1):
                # print("super sbox:", i)
                worker = Worker(
                    cipher_feature=cipher_feature,
                    input_rounds=r,
                    inbound_begin=i,
                    inbound_end=i + 1,
                    num_subinbound=1,
                    inbound_cover=[2],
                    num_solution=num_solution,
                    current_dir=current,
                )
                result = worker.get_truncated_diff_path()
                os.chdir(current)
                tasks[task_id]["results"].append({"id": f"supersbox-{i}", "result": result})

            time.sleep(1)  # 模拟计算延时

        tasks[task_id]["status"] = "completed"
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        print(f"Error in task {task_id}: {e}")

@app.route("/api/hash_function/check-rebound-status", methods=["GET"])
def check_status():
    # try:
        # if not request.is_json:
        #     print(make_response(101, "请求参数异常", None))
        #     return make_response(101, "请求参数异常", None)
        
        # data = request.get_json()
        # if not data:
        #     print(make_response(102,"请求参数为空", None))
        #     return make_response(102,"请求参数为空", None)
        # print(data)
        task_id = request.args.get("taskId")
        # print("task_id:",task_id)
        if task_id not in tasks:
            return make_response(code=103,msg="缺少参数 task id",data=None)
        task = tasks[task_id]
        return make_response(0,"ok",{"status": task["status"], "results": task["results"]})
    # except Exception as e:
        # return make_response(104, f"系统内部错误: {str(e)}", None)
    # task_id = request.args.get("taskId")
    # if task_id not in tasks:
    #     return make_response(code=)
    #     return jsonify({"status": "not_found"}), 404

    # task = tasks[task_id]
    # return jsonify({"status": task["status"], "results": task["results"]})

@app.route("/api/hash_function/get-rebound-pdf", methods=["GET"])
def serve_pdf():
    # try:
        # if not request.is_json:
        #     print(make_response(101, "请求参数异常", None))
        #     return make_response(101, "请求参数异常", None)
        
        # data = request.get_json()
        # if not data:
        #     print(make_response(102,"请求参数为空", None))
        #     return make_response(102,"请求参数为空", None)
        pdf_path = request.args.get("path")
        if pdf_path=="":
            return make_response(code=103,msg="缺少参数 pdf_path",data=None)
        if pdf_path and os.path.exists(pdf_path):
            # directory = os.path.dirname(pdf_path)
            # return send_from_directory(directory, "main.pdf")
            # 安全提取目录与文件名
            directory = os.path.dirname(pdf_path)
            filename = os.path.basename(pdf_path)
            
            # 发送文件（成功响应）
            return send_from_directory(
                directory=directory,
                # "main.pdf"
                path=filename,
                # as_attachment=True,  # 可选：作为附件下载
                # mimetype='application/pdf'
            )
    # except Exception as e:
    #     return make_response(104, f"系统内部错误: {str(e)}", None)
    # pdf_path = request.args.get("path")
    # # print("pdf_path:", pdf_path)
    # if pdf_path and os.path.exists(pdf_path):
    #     directory = os.path.dirname(pdf_path)
    #     filename = os.path.basename(pdf_path)
    #     # print(directory)
    #     return send_from_directory(directory, "main.pdf")
    # else:
    #     return "PDF file not found", 404

# MITM
@app.route('/api/hash_function/mitm-analysis', methods=['POST'])
def mitm_analysis():
    # data = request.get_json()  # 获取前端发送的 JSON 数据
    # task_id = data.get('task_id', str(uuid4()))
    # 从前端数据中获取参数
    # data = request.get_json()  # 获取前端发送的 JSON 数据
    try:
        if not request.is_json:
            return make_response(101, "请求参数异常", None)
        data = request.get_json()
        if not data:
            return make_response(102, "请求参数为空", None)

        if 'rounds' not in data:
            return make_response(103, f"缺少必要参数", None)
        if 'z_size' not in data:
            return make_response(103, f"缺少必要参数", None)
        if 'obj_value' not in data:
            return make_response(103, f"缺少必要参数", None)
        if 'rho_values' not in data:
            return make_response(103, f"缺少必要参数", None)
        if 'k_i1' not in data:
            return make_response(103, f"缺少必要参数", None)
        if 'k_i2' not in data:
            return make_response(103, f"缺少必要参数", None)
        if 'k_i3' not in data:
            return make_response(103, f"缺少必要参数", None)
    except Exception as e:
        return make_response(104, f"系统内部错误: {str(e)}", None)
    rounds = data.get('rounds') - 2
    z_size = data.get('z_size')
    obj_value = data.get('obj_value')
    rho_values = data.get('rho_values')
    k_i1 = data.get('k_i1')
    k_i2 = data.get('k_i2')
    k_i3 = data.get('k_i3')
    # 路径和文件设置
    base_dir = os.path.dirname(__file__)
    filepath = os.path.join(base_dir, "mitm_solution.json")
    output_dir = os.path.join(base_dir, "pic")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.tex")

    # 记录开始时间
    start_time = datetime.now()
    print("Start time: {}".format(start_time.strftime("%m-%d-%H:%M:%S")))

    # 初始化 Mitm 实例并执行
    mitm_instance = Mitm(rounds, filepath, z_size=z_size, obj_value=obj_value, rho_values=rho_values,k_i1=k_i1, k_i2=k_i2, k_i3=k_i3)
    mitm_instance.generate_smt2_file()
    mitm_instance.solve()

    # 记录结束时间和执行耗时
    end_time = datetime.now()
    print("End time: {}".format(end_time.strftime("%m-%d-%H-%M-%S")))
    elapsed_time = end_time - start_time
    # 启动分析任务子进程
    process = subprocess.Popen(
        ["python3", "-c", f"{mitm_instance.generate_smt2_file()}; {mitm_instance.solve()}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # tasks[task_id] = process
    # 生成 TikZ 代码并保存
    tikz_code = mitm_instance.generate(z_size, k_i1)
    with open(output_file, "w") as file:
        file.write(tikz_code)
        # 编译 .tex 文件为 PDF
    pdf_file = output_file.replace(".tex", ".pdf")
    command = ["lualatex", f"-output-directory={output_dir}", output_file]
    result = subprocess.run(command, capture_output=True, text=True)
    if not shutil.which("lualatex"):
        # return jsonify({"status": "error", "message": "pdflatex is not installed"}), 500
        return make_response(104,"系统内部错误",None)

    if result.returncode != 0:
        # 如果编译失败，返回错误信息
        return make_response(104,"系统内部错误",None)
    # 返回执行结果
    return make_response(0,"success",{
        # "task_id": task_id,
        "tikz_file": output_file,
        "pdf_file": pdf_file,  # 添加 PDF 文件路径
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_time": elapsed_time.total_seconds(),
        "message": f"TikZ code has been saved to {output_file}"
    })
# 新增一个路由来提供 PDF 文件
@app.route('/api/hash_function/get-mitm-pdf', methods=['GET'])
def get_pdf():
    file_path = request.args.get('filePath').replace("\\", "/")
    print(f"Resolved PDF path: {file_path}")  # 打印路径以进行调试
    if not os.path.exists(file_path):
        # return jsonify({"error": "PDF file not found"}), 404 #gai
        return make_response(404, f"PDF file not found", None)
    return send_file(file_path, as_attachment=False, mimetype='application/pdf')

# @app.route('/api/hash_function/mitm-analysis/cancel', methods=['POST'])
# def cancel_analysis():
#     task_id = request.json.get('task_id')
#     process = tasks.get(task_id)
#     if process:
#         process.terminate()  # 尝试终止进程
#         tasks.pop(task_id, None)  # 从任务字典中移除
#         return jsonify({"status": "canceled", "task_id": task_id})
#     return jsonify({"status": "error", "message": "Task not found"}), 404

@app.route('/api/hash_function/diff-collision', methods=['POST'])
def sha2like_collision():
    try:
        if not request.is_json:
            return make_response(101, "请求参数异常", None)

        data = request.get_json()
        if not data:
            return make_response(102, "请求参数为空", None)
        if not data.get('rounds'):
            return make_response(103, f"缺少必要参数", None)
        # if not data.get('task_id', str(uuid4())):
        #     return make_response(103, f"缺少必要参数", None)
        if not data.get('z_size'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('msg_i1'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('msg_i2'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('msg_i3'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('msg_i4'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('msg_i5'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('msg_i6'):
            return make_response(103, f"缺少必要参数", None)

        if not data.get('status_i1'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('status_i2'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('status_i3'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('status_i4'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('status_i5'):
            return make_response(103, f"缺少必要参数", None)
        if not data.get('status_i6'):
            return make_response(103, f"缺少必要参数", None)

        # 路径和文件设置
        base_dir = os.path.dirname(__file__)
        # filepath = os.path.join(base_dir, "diff_collision.json")
        output_dir = os.path.join(base_dir, "pic")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.tex")
        # print(filepath)
        # print(output_file)

        # 记录开始时间
        start_time = datetime.now()
        print("Start time: {}".format(start_time.strftime("%m-%d-%H:%M:%S")))
        # task_id = data.get('task_id', str(uuid4()))
        rounds = data.get('rounds')
        z_size = data.get('z_size')

        msg_i1 = data.get('msg_i1')
        msg_i2 = data.get("msg_i2")
        msg_i3 = data.get("msg_i3")
        msg_i4 = data.get("msg_i4")
        msg_i5 = data.get("msg_i5")
        msg_i6 = data.get("msg_i6")

        status_i1 = data.get("status_i1")
        status_i2 = data.get("status_i2")
        status_i3 = data.get("status_i3")
        status_i4 = data.get("status_i4")
        status_i5 = data.get("status_i5")
        status_i6 = data.get("status_i6")

        # 初始化 Mitm 实例并执行
        diff_collision = sha2likeCode.FunctionModel(7, 18, rounds, output_file, z_size,
                                                    msg_i1, msg_i2, msg_i3, msg_i4, msg_i5, msg_i6,
                                                    status_i1, status_i2, status_i3, status_i4, status_i5, status_i6

                                                    )
        diff_collision.save_pdf()
        # 记录结束时间和执行耗时
        end_time = datetime.now()
        print("End time: {}".format(end_time.strftime("%m-%d-%H-%M-%S")))
        elapsed_time = end_time - start_time
        # 编译 .tex 文件为 PDF
        pdf_file = output_file.replace(".tex", ".pdf")
        command = ["pdflatex", f"-output-directory={output_dir}", output_file]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return make_response(104, f"系统内部错误", None)
        return make_response(0, "success", {
        "tikz_file": output_file,
        "pdf_file": pdf_file,  # 添加 PDF 文件路径
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_time": elapsed_time.total_seconds(),
        "message": f"Latex code has been saved to {output_file}"
    })
    except Exception as e:
        return make_response(104, f"系统内部错误: {str(e)}", None)


# 新增一个路由来提供 PDF 文件
@app.route('/api/hash_function/get-diff-collision-pdf', methods=['GET'])
def get_pdf_diff():
    file_path = request.args.get('filePath').replace("\\", "/")
    print(f"Resolved PDF path: {file_path}")  # 打印路径以进行调试
    if not os.path.exists(file_path):
        return jsonify({"error": "PDF file not found"}), 404
    return send_file(file_path, as_attachment=False, mimetype='application/pdf')


# @app.route('/api/hash_function/diff-collision/cancel', methods=['POST'])
# def cancel_analysis_diff():
#     task_id = request.json.get('task_id')
#     process = tasks.get(task_id)
#     if process:
#         process.terminate()  # 尝试终止进程
#         tasks.pop(task_id, None)  # 从任务字典中移除
#         return jsonify({"status": "canceled", "task_id": task_id})
#     return jsonify({"status": "error", "message": "Task not found"}), 404

def matrix_to_str(matrix):
    # Determine the maximum width needed for each column
    column_widths = [
        max(len(str(row[i])) for row in matrix) for i in range(len(matrix[0]))
    ]

    # Construct each row with elements right-aligned based on the column width
    formatted_rows = []
    for row in matrix:
        formatted_row = "  ".join(f"{str(item).rjust(column_widths[i])}"
                                  for i, item in enumerate(row))
        formatted_rows.append(formatted_row)

    # Join all rows into a single string with newline characters
    return "\n".join(formatted_rows)


@app.route('/api/hash_function/mds-generate', methods=['POST'])
def byte_mds():
    return_value = {'msg': 'ok', 'code': 0, 'data': {} }
    data = request.get_json()
    xor = data.get('xor_count')
    try:
        xor = int(xor)
    except Exception as _:
        return_value['code'] = 101
        return_value['msg'] = '错误的参数输入。'
    else:
        temp = misc1.mdses.get(int(xor))
        if temp:
            return_value['data']['matrix'] = temp
            return_value['data']['shift_num'] = len(temp)
        else:
            return_value['code'] = 104
            return_value['msg'] = '没有找到该异或和个数的MDS矩阵。'
    print(return_value)
    return jsonify(return_value)


@app.route('/api/hash_function/byte-generate', methods=['POST'])
def get_byte_algorithm():
    data = request.get_json()
    shift_column_constants = data.get('column_shift')
    round = data.get('round')
    round_constant = data.get('constant')
    mds = data.get('mds')
    sbox = misc1.sboxes[0]
    lane_transform_constants = ((2, 7, 2, 3), (0, 4, 3, 6), (4, 3, 1, 4), (1, 1, 5, 0))
    hash_gen.generate_hash_function(round, round_constant, mds, shift_column_constants, lane_transform_constants, sbox)
    return jsonify({
        'msg': 'ok',
        'code': 0,
        'data': {
            'sbox': sbox,
            'lane': lane_transform_constants
        }
    })


# @app.route('/api/hash_function/byte/call-byte-algorithm', methods=['POST'])
# def byte_algorithm():
#     return_value = {'msg': '', 'code': 0, 'data': {} }
#     data = request.get_json()
#     message = data.get('message')
#     if hash_gen.f is None:
#     # if False:
#         return_value['code'] = 103
#         return_value['msg'] = '请先生成哈希函数'
#     if message:
#         return_value['code'] = 0
#         return_value['msg'] = ''
#         return_value['data']['digesture'] = 'sdfsdfdsfcxvmn'
#     else:
#         return_value['code'] = 102
#         return_value['msg'] = '请输入信息'
#     return jsonify(return_value)

active_sboxes = [ 0, 1, 5, 9, 25, 41, 53, 62, 74, 88, 104, 120, 138, 154, 173, 182]
@app.route('/api/hash_function/byte/calculate-active-sbox', methods=['POST'])
def calculate_active_sbox_bytes():
    data = request.get_json()
    round = data.get('round')
    time.sleep(1.1 ** ( round) + 1)
    if round > 14:
        return jsonify({'msg': '生成超时', 'code': 104, 'data': {}})
    return jsonify({'msg': 'ok', 'code': 0, 'data': {'count': active_sboxes[round]}})


@app.route('/api/hash_function/sbox-generate', methods=['POST'])
def sbox_generate():
    try:
        if not request.is_json:
            return make_response(101, "请求参数异常", None)
            
        data = request.get_json()
        if not data:
            return make_response(102, "请求参数为空", None)
            
        sbox_width = data.get('sbox_width')
        if not sbox_width:
            return make_response(103, "缺少必要参数: sbox_width", None)

        if sbox_width == 4:
            sbox = [[6, 8, 13, 11, 12, 1, 2, 14, 10, 15, 0, 5, 7, 4, 9, 3],
                    [11, 13, 5, 14, 0, 10, 12, 3, 2, 4, 15, 8, 7, 9, 1, 6],
                    [10, 4, 3, 14, 1, 7, 8, 11, 0, 15, 12, 9, 13, 2, 6, 5]]
            return make_response(0, "ok", {"bitwidth": 4, "data": sbox})
        else:
            sbox = [[2, 14, 21, 0, 25, 15, 26, 31, 24, 17, 4, 30, 23, 9, 5, 6, 19, 1, 7, 28, 18, 8, 20, 13, 22, 11, 29, 3, 16, 12, 27, 10],
                    [13, 3, 4, 23, 30, 14, 5, 29, 9, 28, 19, 27, 18, 17, 0, 10, 22, 25, 31, 6, 21, 8, 26, 20, 16, 2, 12, 24, 15, 7, 11, 1],
                    [1, 17, 4, 22, 21, 10, 27, 14, 2, 29, 19, 24, 30, 26, 5, 13, 11, 20, 28, 3, 12, 15, 18, 9, 7, 0, 31, 6, 16, 23, 8, 25]]
            return make_response(0, "ok", {"bitwidth": 5, "data": sbox})
            
    except Exception as e:
        return make_response(104, f"系统内部错误: {str(e)}", None)

@app.route('/api/hash_function/bit-generate', methods=['POST'])
def hash_generate():
    try:
        if not request.is_json:
            return make_response(101, "请求参数异常", None)
            
        data = request.get_json()
        if not data:
            return make_response(102, "请求参数为空", None)
            
        if 'param_b' not in data:
            return make_response(103, "缺少必要参数", None)
        
        if 'param_m' not in data:
            return make_response(103, "缺少必要参数", None)
        
        if 'param_hlen' not in data:
            return make_response(103, "缺少必要参数", None)
        
        if 'param_c' not in data:
            return make_response(103, "缺少必要参数", None)
        
        if 'param_r' not in data:
            return make_response(103, "缺少必要参数", None)
        
        if 'param_w' not in data:
            return make_response(103, "缺少必要参数", None)
        
        generate_bit_hash(data)
        return make_response(0, "ok", None)
        
    except Exception as e:
        return make_response(104, f"系统内部错误", None)

@app.route('/api/hash_function/calculate-hash', methods=['POST'])
def calculate_hash():
    try:
        if not request.is_json:
                return make_response(101, "请求参数异常", None)
        
        data = request.get_json()
        print(data)
        if data['type'] == 1:
            target_path = "../src/design1_bit/bithash.py"
            if not os.path.exists(target_path):
                return make_response(103,"缺少必要参数", None)
                
            if 'message' not in data:
                return make_response(102, "请求参数为空", None)
            
            result = sponge(data['message'])
            return make_response(0, "处理正常", {"hash": result})
        
        else:
            message = data.get('message')
            # print(message)
            # print(hash_gen.f)
            if hash_gen.f is None:
                # print("ok")
                return make_response(103, "缺少必要参数", None)
            
            if message:
                # print("ok")
                # print(message)
                # print(hash_gen.f(message))
                # print("sdfsdfdsfcxvmn")
                return make_response(0, "处理正常", {"digesture": "sdfsdfdsfcxvmn"})
                # return make_response(0, "处理正常", {"digesture": hash_gen.f(message)})
            
            else:
                return make_response(102, "请求参数为空", None)
            
    except Exception as e:
        return make_response(104, f"系统内部错误", None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simple Flask server.')
    parser.add_argument('--host',type=str,default='127.0.0.1',help='Host for the Flask app')
    parser.add_argument('--port',type=int,default=5000,help='Port for the Flask app')
    args=parser.parse_args()
    app.run(host=args.host,port=args.port,debug=True)
