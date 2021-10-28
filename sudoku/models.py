from __future__ import annotations
import math
import itertools

import dimod
from dimod.generators import combinations

from puzzle import var_repr


def build_original_bqm(matrix: list[list[int]]):
    """ Build BQM using Sudoku constraints """
    # Set up
    n = len(matrix)          # Number of rows/columns in sudoku
    m = int(math.sqrt(n))    # Number of rows/columns in sudoku subsquare
    digits = range(1, n+1)

    bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)

    # Constraint: Each node can only select one digit
    for row in range(n):
        for col in range(n):
            node_digits = [var_repr(row, col, digit) for digit in digits]
            one_digit_bqm = combinations(node_digits, 1)
            bqm.update(one_digit_bqm)

    # Constraint: Each row of nodes cannot have duplicate digits
    for row in range(n):
        for digit in digits:
            row_nodes = [var_repr(row, col, digit) for col in range(n)]
            row_bqm = combinations(row_nodes, 1)
            bqm.update(row_bqm)

    # Constraint: Each column of nodes cannot have duplicate digits
    for col in range(n):
        for digit in digits:
            col_nodes = [var_repr(row, col, digit) for row in range(n)]
            col_bqm = combinations(col_nodes, 1)
            bqm.update(col_bqm)

    # Constraint: Each sub-square cannot have duplicates
    # Build indices of a basic subsquare
    subsquare_indices = [(row, col) for row in range(m) for col in range(m)]

    # Build full sudoku array
    for r_scalar in range(m):
        for c_scalar in range(m):
            for digit in digits:
                # Shifts for moving subsquare inside sudoku matrix
                row_shift = r_scalar * m
                col_shift = c_scalar * m

                # Build the labels for a subsquare
                subsquare = [var_repr(row + row_shift, col + col_shift, digit)
                             for row, col in subsquare_indices]
                subsquare_bqm = combinations(subsquare, 1)
                bqm.update(subsquare_bqm)

    # Constraint: Fix known values
    for row, line in enumerate(matrix):
        for col, value in enumerate(line):
            if value > 0:
                # Recall that in the "Each node can only select one digit"
                # constraint, for a given cell at row r and column c, we
                # produced 'n' labels. Namely,
                # ["r,c_1", "r,c_2", ..., "r,c_(n-1)", "r,c_n"]
                #
                # Due to this same constraint, we can only select one of these
                # 'n' labels (achieved by 'generators.combinations(..)').
                #
                # The 1 below indicates that we are selecting the label
                # produced by 'get_label(row, col, value)'. All other labels
                # with the same 'row' and 'col' will be discouraged from being
                # selected.
                bqm.fix_variable(var_repr(row, col, value), 1)

    return bqm


def build_bqm(matrix: list[list[int]]):
    # Set up
    n = len(matrix)  # Number of rows/columns in sudoku
    m = int(math.sqrt(n))  # Number of rows/columns in sudoku subsquare
    digits = list(range(1, n + 1))

    bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)

    # 各セルには digits のいずれかの値が入る
    for i, j in itertools.product(range(n), range(n)):
        node_digits = [var_repr(i, j, v) for v in digits]
        bqm.update(combinations(node_digits, 1))

    # 各行で値は重複しない
    for i, v in itertools.product(range(n), digits):
        row_nodes = [var_repr(i, j, v) for j in range(n)]
        bqm.update(combinations(row_nodes, 1))

    # 各列で値は重複しない
    for j, v in itertools.product(range(n), digits):
        col_nodes = [var_repr(i, j, v) for i in range(n)]
        bqm.update(combinations(col_nodes, 1))

    # 各ブロックで値は重複しない
    for digit in digits:
        for mi, mj in itertools.product(range(m), range(m)):
            ij = itertools.product(
                range(mi * m, (mi + 1) * m),
                range(mj * m, (mj + 1) * m),
            )
            square_nodes = [var_repr(i, j, digit) for i, j in ij]
            bqm.update(combinations(square_nodes, 1))

    # 既知の値については +1 にし、
    # 数独の制約上取りえない値については 0 で値を固定する
    fixed_labels: set[tuple[str, int]] = set()
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val > 0:
                # セル(i,j) は既知なので 1 にする
                fixed_labels |= {(var_repr(i, j, val), 1)}

                # ----------------------------------------------
                # NOTE:
                # 以下の制約上取りえない値について0で固定することで
                # 最適化する変数の数を減らすことができる。
                # その場合は以下の行のコメントを外す
                # ----------------------------------------------
                # # 行i のセルは 値 val をとらない
                # fixed_labels |= {(var_repr(i, jj, val), 0) for jj in range(n) if matrix[i][jj] == 0}
                # # 列j のセルは 値 val をとらない
                # fixed_labels |= {(var_repr(ii, j, val), 0) for ii in range(n) if matrix[ii][j] == 0}
                # # (i, j)があるブロックの他のセルは値 val をとらない
                # mi = i // m
                # mj = j // m
                # iijj = list(itertools.product(
                #     range(mi * m, (mi + 1) * m),
                #     range(mj * m, (mj + 1) * m),
                # ))
                # fixed_labels |= {(var_repr(ii, jj, val), 0) for ii, jj in iijj if matrix[ii][jj] == 0}
    bqm.fix_variables(list(fixed_labels))

    return bqm
