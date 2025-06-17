from collections.abc import Iterator, Sequence, Iterable, Callable
from itertools import combinations
from types import FrameType
from sage.rings.finite_rings.finite_field_constructor import GF
from sage.rings.finite_rings.element_givaro import FiniteField_givaroElement
from sage.rings.finite_rings.finite_field_givaro import FiniteField_givaro
from sage.all import matrix
from signal import signal, SIGINT
from pickle import load, dump
import logging
from sys import exit, stdout

logging.basicConfig(level = logging.DEBUG)

class Search(object):

    def __init__(self, order: int, field_dimension: int,
                 polynomials: Sequence[int], xor_table_file: str, modulus: int,
                 matrix_geneator: Callable[[FiniteField_givaro, int],
                 Iterable[matrix]], xor_filter: Callable[[int], bool] | None):
        self.__ORDER = order
        self.__POLYNOMIALS = tuple(polynomials)
        with open(xor_table_file, 'r') as f:
            self.__XOR_TABLE: tuple[dict[int, int], ...] = tuple(
                dict(zip(polynomials, map(lambda x: int(x),
                                          r.strip().split())))
                for r in f.readlines())
        degree = 2**field_dimension
        self.__FIELD = GF(degree,
                          modulus=tuple(int(i) for i in bin(modulus)[2:]),
                          name='x')
        self.__MODULUS = modulus
        self.__MATRIX_GENEATOR = matrix_geneator(self.field, order)
        self.__ITERATOR = iter(self.matrix_geneator)
        self.__XOR_FILTER = xor_filter or (lambda _: True)
        self.__matrix_counter = 1

    def __calculate_xor(self, matrix_: Sequence[int]) -> int:
        lookups = 0
        for e in matrix_:
            lookups += self.xor_table[e][self.modulus]
        return lookups

    def __check_mds(self, matrix_: matrix) -> bool:
        for size in range(1, self.order + 1):
            comb = tuple(combinations(range(self.order), size))
            for i in range(len(comb)-1):
                a = comb[i]
                b = comb[i + 1]
                for submatrix in (matrix_[a,b], matrix_[b,a], matrix_[a,a], matrix_[b,b],):
                    if submatrix.det() == self.field.from_integer(0):
                        return False
        return True

    def __next__(self) -> tuple[matrix, int]:
        while True:
            self.__matrix = next(self.iterator)
            if self.__matrix_counter ^ (2 << 32):
                stdout.flush()
            self.__matrix_counter += 1
            count = self.__calculate_xor(self.__matrix)
            if self.xor_filter(count):
                self.__matrix = self.__MATRIX_GENEATOR.generate_permutation_matrix(self.__matrix)
                if self.__check_mds(self.__matrix):
                    return (self.__matrix.apply_map(lambda x: x.to_integer()), count)

    def __iter__(self):
        return self

    @property
    def order(self) -> int:
        return self.__ORDER

    @property
    def polynomials(self) -> tuple[int, ...]:
        return self.__POLYNOMIALS

    @property
    def field(self):
        return self.__FIELD

    @property
    def modulus(self) -> int:
        return self.__MODULUS

    @property
    def xor_table(self) -> tuple[dict[int, int], ...]:
        return self.__XOR_TABLE

    @property
    def xor_filter(self) -> Callable[[int], bool]:
        return self.__XOR_FILTER

    @property
    def matrix_(self) ->  matrix:
        return self.__matrix

    @property
    def matrix_counter(self) -> int:
        return self.__matrix_counter

    @property
    def matrix_geneator(self) -> Callable:
        return self.__MATRIX_GENEATOR

    @property
    def iterator(self) -> Iterator:
        return self.__ITERATOR

class SearchSession(object):

    FILE = './saved'

    def __init__(self, search: Search | None = None):
        if search:
            self.__search = search
        else:
            with open(type(self).FILE, 'rb') as f:
                self.__search = load(f)
                if type(self.__search) != Search:
                    raise RuntimeError(f'File {type(self).FILE} does not exist or is corruptted!')
        signal(SIGINT, self.__save)
        for (matrix_, xor_count) in self.__search:
            print(f'{matrix_} with {xor_count}')

    def __save(self, _: int, __: FrameType | None):
        with open(type(self).FILE, 'wb') as f:
            search = self.__search
            dump((search.matrix_counter, search.matrix_), f)
        exit(127)

class PermutationArray(object):

    def __init__(self, field: FiniteField_givaro, order: int):
        self.__field = field
        self.__order = order
        self.__all_nums = tuple(range(1, 2 ** self.field.degree()))
        self.__permutations = tuple(list(range(1, order)) + [0])
        filt = lambda x: abs(x[0] - x[1]) != 2 # TODO: apply filt 2.
        type1 = tuple(filter(filt, combinations(range(self.order), 2)))
        type2 = tuple() # TODO:
        type3 = tuple() # TODO:
        type4 = tuple() # TODO:
        self.__repeat_choices = (type1, type2,  type3,  type4, )

    def __permutate_array(
        self,
        coefficients: Sequence[FiniteField_givaroElement],
    ) -> tuple[FiniteField_givaroElement]:
        length = len(coefficients)
        if len(self.permutations) != length:
            raise ValueError(
                f'The length of coefficients ({length}) is not equal to the length to permutations {len(self.permutations)}'
            )
        lookups = [self.field.from_integer(0) for _ in range(length)]
        for i in range(length):
            lookups[i] = coefficients[self.permutations[i]]
        return tuple(lookups)

    def generate_permutation_matrix(self, raw_coefficients: Sequence[int]) -> matrix:
        coefficients: tuple[FiniteField_givaroElement] = tuple(
            map(lambda x: self.field.from_integer(x), raw_coefficients))
        length = len(coefficients)
        raw_result: list[tuple[FiniteField_givaroElement]] = [
            (self.field.from_integer(0), ) for _ in range(length)
        ]
        t = coefficients
        raw_result[0] = t
        for i in range(1, length):
            t = self.__permutate_array(t)
            raw_result[i] = t
        return matrix(raw_result)

    @property
    def order(self) -> int:
        return self.__order

    @property
    def field(self) -> FiniteField_givaro:
        return self.__field

    @property
    def permutations(self) -> tuple[int, ...]:
        return self.__permutations

    def __iter__(self) -> Iterator:
        for nums in combinations(self.__all_nums, 4):
            # yield self.__generate_permutation_matrix(nums)
            yield tuple(nums)
        for nums in combinations(self.__all_nums, 3):
            for pair in self.__repeat_choices[0]:
                nums_ = list(nums)
                nums_.insert(pair[1], nums[pair[0]])
                # yield self.__generate_permutation_matrix(nums)
                yield tuple(nums_)
        return self

order = 4
field_dimension = 8
polynomials = (0b100011101, 0b101110111, 0b111110011, 0b101101001, 0b110111101,
               0b111100111, 0b100101011, 0b111010111, 0b101100101, 0b110001011,
               0b101100011, 0b100011011, 0b100111111, 0b101011111, 0b111000011,
               0b100111001)
xor_table_file = 'xor_table'
modulus = polynomials[11]
# co, pu = (2, 3, 1, 1), (3, 0, 1, 2)


s = Search(order, field_dimension, polynomials, xor_table_file, modulus, PermutationArray, lambda c: c < 18) # minus (non_zero - 1) * degree = 24
SearchSession(s)
