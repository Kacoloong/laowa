import os

def getConstant(start, end, length):
    w = end + 10  # 考虑精度，位数增加 k，结果减少 k 位
    b = 10 ** w   # 用整数计算pi

    x1 = b * 4 // 5            # 第一项前半部分
    x2 = b // -239             # 第一项后半部分
    total_sum = x1 + x2       # 第一项的值

    end *= 2
    for i in range(3, end, 2):
        x1 //= -25
        x2 //= -239 * 239
        x = (x1 + x2) // i
        total_sum += x

    mpi = total_sum * 4
    mpi //= 10 ** 10           # 向右移动10位以调整小数点位置

    mpi_str = str(mpi)
    mpi_str = mpi_str[:1] + '.' + mpi_str[1:]  # 在小数点前后拼接

    # 获取圆周率的小数部分
    decimal_part = mpi_str[2:]  # 取小数部分

    # 生成结果数组
    result = []
    for i in range(start, end, length):
        segment = decimal_part[i - 1:i + length - 1]
        if segment:  # 确保 segment 不为空
            result.append(int(segment))

    return result

def generate_bit_hash(params):
    b = params['param_b']
    c = params['param_c']
    r = b - c
    md = params['param_hlen']
    m = params['param_m']
    n = b // m
    round = params['param_r']
    num = 4 if params['param_w'] == 4 else 5
    Sbox = params['sboxMatrix']
    iv = (int)(md << 52) + (int)(r << 40) + (int)(m << 28) + (int)(n << 16)
    rc = getConstant(2025, (int)(2025+19*m/(num)-1), 19)

    # 要写入的函数内容
    written_code = """import numpy as np

"""
        
    written_code += """def rotate_left(value, k):
    # 左循环移位
    if k == 0:
        return value
    # 将 value 转换为 Python 的整数进行位运算
    return ((value << k) | (value >> ({n} - k))) & 0xFFFFFFFFFFFFFFFF
        
""".format(n = n)

    written_code += """def get_bit(n, k):
    # 提取整数 n 的第 k 个比特
    return (n >> k) & 1

"""

    written_code += """def set_bit(n, k, bit):
    # 设置整数 n 的第 k 个比特为 1
    if bit == 1:
        return n | (1 << k)
    elif bit == 0:
        return  n & ~(1 << k)

"""

    written_code += """def string_to_bitstring(pt):
    # 将字符串转换为比特串
    bitstring = ''.join(format(ord(char), '08b') for char in pt)
    return bitstring

"""

    written_code += """def bitstring_to_int_array(bitstring):
    num_int_elements = len(bitstring) // {n}  # 计算需要的整数数组的长度
    int_array = [0] * num_int_elements  # 初始化一个整数数组

    for i in range(num_int_elements):
        bit_segment = bitstring[i * {n}:(i + 1) * {n}]  # 获取n位的比特串
        int_array[i] = int(bit_segment, 2)  # 转换为整数并存储

    return int_array

""".format(n = n)

    written_code += """def pad_bitstring(bitstring):
    # 当前比特串长度
    current_length = len(bitstring)
        
    # 计算需要填充的长度，使其为 {r} 的倍数
    target_length = ((current_length + {r} + 1) // {r}) * {r}
        
    # 计算填充的位数
    padding_length = target_length - current_length
        
    # 填充中间的0的数量
    middle_zeros_length = padding_length - 2
        
    # 构造填充后的比特串
    padded_bitstring = bitstring + '1' + '0' * middle_zeros_length + '1'
        
    return padded_bitstring

""".format(r = r)

    written_code += """class StateArray:

    def __init__(self, S):  #初始化各参数
        self.m = {m}
        self.n = {n}
        self.md = {md}
        self.r = {r}
        self.c = {c}
        self.S = S  #状态
        self.num = {num}
        self.round = {round}
""".format(m = m, n = n, md = md, r = r, c = c, num = num, round = round)

    written_code += """        self.Rconj = ["""
    for i in range (m // num):
        written_code += str(rc[i])
        if i != m // num - 1:
            written_code += """, """
    written_code += """]  #轮常数"""

    if num == 5:
        written_code += """
        self.Ldiff = [[9, 16], [12, 33], [11, 4], [20, 27], [39, 49]]  #线性扩散的参数[a,b]
"""
    else:
        if b == 1536:
            written_code += """
        self.Ldiff = [[12, 29], [3, 41], [20, 46], [34, 57]]  #线性扩散的参数[a,b]
"""
        else:
             written_code += """
        self.Ldiff = [[4, 22], [27, 35], [13, 55], [42, 48]]  #线性扩散的参数[a,b]
"""
        written_code += """        self.Sbox = {Sbox} #选用的S盒

""".format(Sbox = Sbox)

    written_code += """    def round_constant_addition(self):  #轮常数加
        for i in range(self.m // self.num):
            self.S[self.num*i + 2] ^=  self.Rconj[i]

"""

    written_code += """    def linear_diffusion(self):   # 循环移位异或
        for i in range(self.m):
            self.S[i] = self.S[i] ^ rotate_left(self.S[i], self.Ldiff[i%{num}][0]) ^ rotate_left(self.S[i], self.Ldiff[i%{num}][1])

""".format(num = num)

    written_code += """    def Subword(self, round):  # S盒置换
        temp = 0
        for i in range(self.n):
            for j in range(self.m // self.num):  #一列中的分组数
"""
    if num == 4:
        written_code += """                temp = 8 * get_bit(self.S[(j*self.num + round - 1 + i) % self.m], self.n - i - 1) + 4 * get_bit(self.S[(j*self.num + 1 + round - 1 + i) % self.m], self.n - i - 1) + 2 * get_bit(self.S[(j*self.num + 2 + round - 1 + i) % self.m], self.n - i - 1) + get_bit(self.S[(j*self.num + 3 + round - 1 + i) % self.m], self.n - i - 1)
    """
    else:
        written_code += """                temp = 16 * get_bit(self.S[(j*self.num + round - 1 + i) % self.m], self.n - i - 1) + 8 * get_bit(self.S[(j*self.num + 1 + round - 1 + i) % self.m], self.n - i - 1) + 4 * get_bit(self.S[(j*self.num + 2 + round - 1 + i) % self.m], self.n - i - 1) + 2 * get_bit(self.S[(j*self.num + 3 + round - 1 + i) % self.m], self.n - i - 1) + get_bit(self.S[(j*self.num + 4 + round - 1 + i) % self.m], self.n - i - 1)
    """

    written_code +="""            temp = self.Sbox[temp]
                for k in range(self.num):
                    self.S[(j*self.num + k + round - 1 + i) % self.m] = set_bit(self.S[(j*self.num + k + round - 1 + i) % self.m], self.n - i - 1, get_bit(temp, self.num - k - 1))

"""               

    written_code += """    def P(self):  #置换函数p(迭代进行round轮)
        for i in range(self.round):
            self.round_constant_addition()
            self.Subword(i+1)
            self.linear_diffusion()

"""

    written_code += """
def sponge(pt):  #整体海绵结构(明文为输入，哈希摘要值为输出)
    pt = bitstring_to_int_array(pad_bitstring(string_to_bitstring(pt)))  #填充并转换为 int 数组
    iv = {iv}
    S = [iv] + [0] * ({m} - 1)  #初始化
    state = StateArray(S)

    for i in range ({n} * len(pt) // state.r):  #吸收
        for j in range (state.r // {n}):
            state.S[j] ^= pt[i * state.r // {n} + j]
        state.P()

    bit_string = ''
    for i in range (min(state.md, state.r) // {n}):
        bit_string += format(state.S[i], '0{n}b')  # 64 位二进制格式

    for i in range((state.md - 1) // state.r):  #挤出
        state.P()
        for j in range (state.r // {n}):
            bit_string += format(state.S[j], '0{n}b')  # 继续添加比特串

    hex_output = ''.join(format(int(bit_string[i:i + 4], 2), 'x') for i in range(0, len(bit_string), 4))
    return hex_output
""".format(iv = iv, m = m, n = n)

    output_path = "/home/ninini/51Hash/backend/backend/src/design1_bit/bithash.py"

    # 强制覆盖写入
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(written_code)
        f.close()