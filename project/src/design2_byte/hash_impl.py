import logging
from sage.rings.finite_rings import finite_field_constructor
from sage.all import matrix
from random import shuffle
from numpy import array
from copy import deepcopy
import sys
import misc
import importlib

importlib.reload(finite_field_constructor)

F = finite_field_constructor.GF(misc.NUM_SIZE, modulus=(1, 0, 0, 0, 1, 1, 0, 1, 1), name='x')

class State(object):
    """
        The state is stored as a column.
        index order: z, y, x.
    """

    def __init__(self, input):
        """
            input: Slice[[Row], [Row], [Row], [Row], ...], Slice[[Row], [Row], [Row], [Row], ...], ...
        """
        t = len(input)
        if t != misc.LANE_LENGTH:
            raise TypeError(f'l is {t} long rather than {misc.LANE_LENGTH}!')
        t = len(input[0])
        if t != misc.COLUMN_LENGTH:
            raise TypeError(f'l[0] is {t} long rather than {misc.COLUMN_LENGTH}!')
        t = len(input[0][0])
        if t != misc.ROW_LENGTH:
            raise TypeError(
                f'l[0][0] is {t} long rather than {misc.ROW_LENGTH}!')
        self.__storage = [matrix(ll) for ll in input]

    def xor_with_message(self, message, use_fore):
        zstart = 0 if use_fore else misc.LANE_LENGTH // 2
        zend = misc.LANE_LENGTH // 2 if use_fore else misc.LANE_LENGTH
        m_i = 0
        for z in range(zstart, zend):
            for y in range(0, misc.COLUMN_LENGTH):
                for x in range(0, misc.ROW_LENGTH):
                    self[z, y, x] = self[z, y, x] ^ message[m_i]
                    m_i += 1

    def turncate_to_first_n_slice(self, n):
        """
            (slice0row0, slice0row1, slice0row2, slice0row3, slice1row0, ...)
        """
        return tuple(num for i in range(n) for num in self.__slice_to_tuple(i))

    def map(self, f):
        for z in range(misc.LANE_LENGTH):
            self[z] = f(self[z])

    def lane(self, y, x):
        return tuple(self[z, y, x] for z in range(misc.LANE_LENGTH))

    def set_lane(self, y, x, t):
        if len(t) != misc.LANE_LENGTH:
            raise ValueError(
                f'lane should be {misc.LANE_LENGTH} long but got {len(t)}!')
        for z in range(misc.LANE_LENGTH):
            self[z, y, x] = t[z]

    def __getitem__(self, pos):
        """
            z,y,x
        """
        if isinstance(pos, tuple):
            if len(pos) == 3:
                z, y, x = pos
                return self.__storage[z][y][x]
            elif len(pos) == 2:
                z, y = pos
                return self.__storage[z][y]
            else:
                raise TypeError(f'Invalid subscription length {len(pos)}')
        else:
            z = pos
            return self.__storage[z]

    def __setitem__(self, pos, value):
        """
            z,y,x
        """
        if isinstance(pos, tuple):
            if len(pos) == 3:
                z, y, x = pos
                self.__storage[z][y, x] = value
            elif len(pos) ==  2:
                z, y = pos
                self.__storage[z][y] = value
            else:
                raise TypeError(f'Invalid subscription length {len(pos)}')
        else:
            z = pos
            self.__storage[z] = value

    def __slice_to_tuple(self, z):
        return tuple(i for r in self.__storage[z].rows() for i in r)

    def __iter__(self):
        for matrix in self.__storage:
            yield matrix
        return None

    def __str__(self):
        lane_transform_constant = tuple(f'z = {z}:\n{self[z]}'
                                        for z in range(misc.LANE_LENGTH))
        return f'Matrix:\n{"|".join(lane_transform_constant)}\n\n '

    def __repr__(self):
        return str(self.turncate_to_first_n_slice(misc.LANE_LENGTH))

class SBox(object):

    BASE = 16

    def __init__(self, raw, prob_of_diff_path= 6):
        self.__storage = raw
        self.__prob_of_diff_path = prob_of_diff_path

    @property
    def prob_of_diff_path(self):
        return self.__prob_of_diff_path

    def __getitem__(self, pos):
        if isinstance(pos, int):
            return self.__storage[pos]
        if len(pos) == 2:
            x,y = pos
            return self.__storage[x][y]
        raise TypeError('Too many dimensions for SBox!')

    def __str__(self):
        return str(self.__storage)


class HashFunction(object):

    @staticmethod
    def block_to_hash(b):
        """
            (00,01,02,ff) -> 000102ff
        """
        lane_transform_constant = [int(byte_).to_bytes() for byte_ in b]
        return hex(int.from_bytes(b''.join(lane_transform_constant)))

    @staticmethod
    def fill_and_block_message(raw):
        message = list(raw)
        message.append(1)
        parts = list(message[i:i + misc.BLOCK_SIZE]
                     for i in range(0, len(message), misc.BLOCK_SIZE))
        while len(parts[-1]) < misc.BLOCK_SIZE:
            parts[-1].append(0)
        return tuple(map(lambda line: tuple(line), parts))

    # @staticmethod
    # def gen_state():
    #     length = misc.LANE_LENGTH * misc.ROW_LENGTH * misc.COLUMN_LENGTH
    #     st = list(range(misc.NUM_SIZE))
    #     shuffle(st)
    #     st = array( st[:length]).reshape( (misc.LANE_LENGTH, misc.ROW_LENGTH, misc.COLUMN_LENGTH)).tolist()
    #     return State(st)

    @staticmethod
    def __str_to_message(s):
        if isinstance(s, str):
            return tuple(bytes(s, 'utf-8'))
        return s

    @staticmethod
    def tuple_to_mds(t):
        return matrix(tuple(tuple(map(lambda x: F.fetch_int(int(x)), l)) for l in t))

    def __init__(self, round, round_constant, mds, shift_column_constants, lane_transform_constants, sbox):
        self.__ROUND = round
        self.__ROUND_CONSTANT = round_constant
        self.__MDS = self.tuple_to_mds(mds)
        self.__SBOX = SBox(sbox)
        self.__LINE_TRANSITION_CONSTANTS = matrix(lane_transform_constants)
        self.__INIT_STATE = State([[[102, 89, 200, 212],
  [46, 130, 96, 85],
  [26, 100, 115, 79],
  [134, 216, 139, 231]],
 [[43, 214, 106, 179],
  [92, 98, 67, 126],
  [232, 31, 204, 186],
  [229, 42, 14, 255]],
 [[182, 29, 38, 254],
  [132, 147, 133, 240],
  [135, 105, 101, 146],
  [3, 168, 172, 184]],
 [[151, 9, 234, 81],
  [137, 114, 167, 238],
  [162, 174, 187, 220],
  [236, 201, 80, 193]],
 [[37, 175, 62, 195],
  [219, 178, 112, 145],
  [59, 180, 150, 36],
  [140, 158, 107, 190]],
 [[117, 203, 192, 153],
  [39, 169, 34, 185],
  [152, 64, 171, 223],
  [241, 118, 165, 149]],
 [[141, 73, 252, 199],
  [242, 53, 19, 208],
  [191, 48, 196, 161],
  [233, 108, 77, 25]],
 [[213, 15, 123, 131],
  [127, 156, 88, 142],
  [173, 22, 75, 166],
  [58, 144, 181, 183]]])
        self.__SHIFT_COLUMN_CONSTANTS = shift_column_constants

    def __call__(self, input_):
        state = deepcopy(self.init_state)
        message = self.__str_to_message(input_)
        blocks = self.fill_and_block_message(message)
        for block in blocks:
            state.xor_with_message(block, True)
            for r in range(self.round):
                state = self.__permutation(state, r)
            state.xor_with_message(block, False)
        return self.block_to_hash(
            state.turncate_to_first_n_slice(misc.FINAL_USE_SLICE))

    def __str__(self) -> str:
        return f'''
--------------------杂凑函数--------------------
轮数: {self.round}
轮常数: {self.round_constant}

列移位常数: {self.shift_column_constants}

Lane变换常矩阵:
{self.line_transform_constants}

MDS矩阵:
{self.mds}

S盒:
{self.sbox}
------------------------------------------------
'''

    @property
    def round(self):
        return self.__ROUND

    @property
    def round_constant(self):
        return self.__ROUND_CONSTANT

    @property
    def mds(self):
        return self.__MDS

    @property
    def shift_column_constants(self):
        return self.__SHIFT_COLUMN_CONSTANTS

    @property
    def line_transform_constants(self):
        return self.__LINE_TRANSITION_CONSTANTS

    @property
    def sbox(self):
        return self.__SBOX

    @property
    def field(self):
        return self.mds[0, 0].parent()

    @property
    def init_state(self):
        return self.__INIT_STATE

    def __permutation(self, s, r):
        s = self.__add_constant(s, r)
        s = self.__substitute_bytes(s, r)
        s = self.__shift_column(s, r)
        s = self.__mix_row(s, r)
        s = self.__lane_transform(s, r)
        return s

    def __add_constant(self, s, _):
        s.map(lambda mds: mds.apply_map(lambda x: x ^ self.round_constant))
        return s

    def __substitute_bytes(self, s, _):
        s.map(lambda m: m.apply_map(lambda x: self.sbox[x // SBox.BASE, x % SBox.BASE]))
        return s

    def __mix_row_auxiliary(self, m):
        m = m.apply_map(lambda x: self.field.fetch_int(x))
        m = m * self.mds
        return m.apply_map(lambda x: x.integer_representation())

    def __mix_row(self, s, _):
        s.map(self.__mix_row_auxiliary)
        return s

    def __shift_column(self, s, _):
        for z in range(misc.LANE_LENGTH):
            slice = s[z]
            for x in range(misc.ROW_LENGTH):
                shift_pad = self.shift_column_constants[x]
                column = list(slice.column(x))
                column = column[shift_pad:] + column[:shift_pad]
                slice.set_column(x, column)
        return s

    def __lane_transform(self, s, _):
        for x in range(misc.ROW_LENGTH):
            for y in range(misc.COLUMN_LENGTH):
                shift_pad = self.line_transform_constants[y, x]
                lane = list(s.lane(y, x))
                lane = lane[shift_pad:] + lane[:shift_pad]
                s.set_lane(y, x, lane)
        return s



if __name__ == '__main__':
    lane_transform_constants = ((2, 7, 2, 3), (0, 4, 3, 6), (4, 3, 1, 4), (1, 1, 5, 0))
    f = HashFunction(14, 247, misc.mdses[6][0], (3, 2, 1, 2), lane_transform_constants, misc.sboxes[0])
    test_cases = (
        tuple(bytes(16)),
        (0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f),
        tuple(bytes(4)),
        (0xd3, 0x60, 0xfc, 0x16, 0x01, 0x75, 0x55, 0x39, 0xf2, 0x64, 0xdf, 0x53, 0x65, 0x59, 0xb8, 0x56),
    )
    for test_case in test_cases:
        print('Test Case:', test_case)
        print('Result:', f(test_case))
