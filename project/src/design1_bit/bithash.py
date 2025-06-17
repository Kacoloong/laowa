import numpy as np

def rotate_left(value, k):
    # 左循环移位
    if k == 0:
        return value
    # 将 value 转换为 Python 的整数进行位运算
    return ((value << k) | (value >> (64 - k))) & 0xFFFFFFFFFFFFFFFF
        
def get_bit(n, k):
    # 提取整数 n 的第 k 个比特
    return (n >> k) & 1

def set_bit(n, k, bit):
    # 设置整数 n 的第 k 个比特为 1
    if bit == 1:
        return n | (1 << k)
    elif bit == 0:
        return  n & ~(1 << k)

def string_to_bitstring(pt):
    # 将字符串转换为比特串
    bitstring = ''.join(format(ord(char), '08b') for char in pt)
    return bitstring

def bitstring_to_int_array(bitstring):
    num_int_elements = len(bitstring) // 64  # 计算需要的整数数组的长度
    int_array = [0] * num_int_elements  # 初始化一个整数数组

    for i in range(num_int_elements):
        bit_segment = bitstring[i * 64:(i + 1) * 64]  # 获取n位的比特串
        int_array[i] = int(bit_segment, 2)  # 转换为整数并存储

    return int_array

def pad_bitstring(bitstring):
    # 当前比特串长度
    current_length = len(bitstring)
        
    # 计算需要填充的长度，使其为 512 的倍数
    target_length = ((current_length + 512 + 1) // 512) * 512
        
    # 计算填充的位数
    padding_length = target_length - current_length
        
    # 填充中间的0的数量
    middle_zeros_length = padding_length - 2
        
    # 构造填充后的比特串
    padded_bitstring = bitstring + '1' + '0' * middle_zeros_length + '1'
        
    return padded_bitstring

class StateArray:

    def __init__(self, S):  #初始化各参数
        self.m = 16
        self.n = 64
        self.md = 512
        self.r = 512
        self.c = 512
        self.S = S  #状态
        self.num = 4
        self.round = 8
        self.Rconj = [2595709825822620522, 4894077267194782684, 8260147699090264013, 6394437455305068203]  #轮常数
        self.Ldiff = [[4, 22], [27, 35], [13, 55], [42, 48]]  #线性扩散的参数[a,b]
        self.Sbox = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] #选用的S盒

    def round_constant_addition(self):  #轮常数加
        for i in range(self.m // self.num):
            self.S[self.num*i + 2] ^=  self.Rconj[i]

    def linear_diffusion(self):   # 循环移位异或
        for i in range(self.m):
            self.S[i] = self.S[i] ^ rotate_left(self.S[i], self.Ldiff[i%4][0]) ^ rotate_left(self.S[i], self.Ldiff[i%4][1])

    def Subword(self, round):  # S盒置换
        temp = 0
        for i in range(self.n):
            for j in range(self.m // self.num):  #一列中的分组数
                temp = 8 * get_bit(self.S[(j*self.num + round - 1 + i) % self.m], self.n - i - 1) + 4 * get_bit(self.S[(j*self.num + 1 + round - 1 + i) % self.m], self.n - i - 1) + 2 * get_bit(self.S[(j*self.num + 2 + round - 1 + i) % self.m], self.n - i - 1) + get_bit(self.S[(j*self.num + 3 + round - 1 + i) % self.m], self.n - i - 1)
                temp = self.Sbox[temp]
                for k in range(self.num):
                    self.S[(j*self.num + k + round - 1 + i) % self.m] = set_bit(self.S[(j*self.num + k + round - 1 + i) % self.m], self.n - i - 1, get_bit(temp, self.num - k - 1))

    def P(self):  #置换函数p(迭代进行round轮)
        for i in range(self.round):
            self.round_constant_addition()
            self.Subword(i+1)
            self.linear_diffusion()


def sponge(pt):  #整体海绵结构(明文为输入，哈希摘要值为输出)
    pt = bitstring_to_int_array(pad_bitstring(string_to_bitstring(pt)))  #填充并转换为 int 数组
    iv = 2306405963466276864
    S = [iv] + [0] * (16 - 1)  #初始化
    state = StateArray(S)

    for i in range (64 * len(pt) // state.r):  #吸收
        for j in range (state.r // 64):
            state.S[j] ^= pt[i * state.r // 64 + j]
        state.P()

    bit_string = ''
    for i in range (min(state.md, state.r) // 64):
        bit_string += format(state.S[i], '064b')  # 64 位二进制格式

    for i in range((state.md - 1) // state.r):  #挤出
        state.P()
        for j in range (state.r // 64):
            bit_string += format(state.S[j], '064b')  # 继续添加比特串

    hex_output = ''.join(format(int(bit_string[i:i + 4], 2), 'x') for i in range(0, len(bit_string), 4))
    return hex_output
