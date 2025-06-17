import numpy as np


# @staticmethod
def flatten_state(s):
    state_bits = [s[i][j] for i in range(len(s)) for j in range(len(s[0]))]
    return state_bits


def multiply_elements(lst):
    product = 1
    for number in lst:
        product *= number
    return product


# @staticmethod
def left_rotate(row, n):
    """向左循环移动列表中的元素"""
    return row[n:] + row[:n]


def hamming_weight(vector):
    """Calculate the Hamming weight of a binary vector."""
    return np.sum(vector)


def matrix_vector_multiply(matrix, vector):
    """Multiply a binary matrix with a binary vector (mod 2)."""
    result = np.dot(matrix, vector) % 2
    return result


def min_branch_number(matrix):
    """Calculate the differential branch number of the matrix."""
    rows, cols = matrix.shape
    min_branch = float("inf")

    # Iterate through all non-zero binary vectors of length cols
    for i in range(1, 2**cols):
        # Generate binary vector
        vector = np.array([int(x) for x in bin(i)[2:].zfill(cols)], dtype=int)

        # Calculate wt(a) + wt(M(a))
        weight_a = hamming_weight(vector)
        transformed_vector = matrix_vector_multiply(matrix, vector)
        weight_transformed = hamming_weight(transformed_vector)
        branch_number = weight_a + weight_transformed

        # Update the minimum branch number
        if branch_number < min_branch:
            min_branch = branch_number

    return min_branch
