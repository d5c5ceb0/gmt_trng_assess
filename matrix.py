#!/usr/bin/python3

import copy

MATRIX_FORWARD_ELIMINATION  = 0
MATRIX_BACKWARD_ELIMINATION = 1

def computeRank(M, Q, matrix):
    m = min(M,Q)
	
	#/* FORWARD APPLICATION OF ELEMENTARY ROW OPERATIONS */ 
    for i in range(m-1):
        if  matrix[i][i] == 1:
            perform_elementary_row_operations(MATRIX_FORWARD_ELIMINATION, i, M, Q, matrix)
        else:
            if find_unit_element_and_swap(MATRIX_FORWARD_ELIMINATION, i, M, Q, matrix):
                perform_elementary_row_operations(MATRIX_FORWARD_ELIMINATION, i, M, Q, matrix)

	#/* BACKWARD APPLICATION OF ELEMENTARY ROW OPERATIONS */ 
    for i in range(m-1, 0, -1):
        if matrix[i][i] == 1:
            perform_elementary_row_operations(MATRIX_BACKWARD_ELIMINATION, i, M, Q, matrix)
        else:
            if find_unit_element_and_swap(MATRIX_BACKWARD_ELIMINATION, i, M, Q, matrix):
                perform_elementary_row_operations(MATRIX_BACKWARD_ELIMINATION, i, M, Q, matrix)

    return determine_rank(M, Q, matrix)

def perform_elementary_row_operations(flag, i, M, Q, A):
    if flag == MATRIX_FORWARD_ELIMINATION:
        for j in range(i+1, M):
            if A[j][i] == 1:
                for k in range(i, Q):
                    A[j][k] = (A[j][k] + A[i][k]) % 2
    else:
        for j in range(i-1, -1, -1):
            if  A[j][i] == 1:
                for k in range(Q):
                    A[j][k] = (A[j][k] + A[i][k]) % 2

    return A

def find_unit_element_and_swap(flag, i, M, Q, A):
    row_op = False
    if flag == MATRIX_FORWARD_ELIMINATION:
        index = i + 1
        while (index < M) and (A[index][i] == 0):
            index += 1
        if index < M:
            swap_rows(i, index, Q, A)
            row_op = True
    else:
        index = i - 1
        while (index >= 0) and (A[index][i] == 0):
            index -= 1
        if index >= 0:
            swap_rows(i, index, Q, A)
            row_op = True
	
    return row_op

def swap_rows(i, index, Q, A):
    for p in range(Q):
        temp = A[i][p]
        A[i][p] = A[index][p]
        A[index][p] = temp
	
def determine_rank(M, Q, A):
    m = min(M,Q)
    rank = m
    for i in range(m):
        allZeroes = 1
        for j in range(Q):
            if A[i][j] == 1:
                allZeroes = 0
                break

        if allZeroes == 1:
            rank -= 1

    return rank

def create_matrix(M, Q, input):
    m = list()
    for i in range(Q):
        row = input[i*M : (i+1)*M]
        m.append(row)
    return m


if __name__ == '__main__':
    m = create_matrix(3, 3, [int(v) for v in '011101110'])
    print(computeRank(3, 3, m)) #rand = 2

