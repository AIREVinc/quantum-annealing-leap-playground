import math


def get_matrix(filename):
    """Return a list of lists containing the content of the input text file.

    Note: each line of the text file corresponds to a list. Each item in
    the list is from splitting the line of text by the whitespace ' '.
    """
    with open(filename, "r") as f:
        content = f.readlines()

    lines = []
    for line in content:
        new_line = line.rstrip()    # Strip any whitespace after last value

        if new_line:
            new_line = list(map(int, new_line.split(' ')))
            lines.append(new_line)

    return lines


def is_correct(matrix: list[list[int]]):
    """Verify that the matrix satisfies the Sudoku constraints.

    Args:
      matrix(list of lists): list contains 'n' lists, where each of the 'n'
        lists contains 'n' digits.
    """
    n = len(matrix)        # Number of rows/columns
    m = int(math.sqrt(n))  # Number of subsquare rows/columns
    unique_digits = set(range(1, n+1))  # Digits in a solution

    # Verifying rows
    for row in matrix:
        if set(row) != unique_digits:
            print("Error in row: ", row)
            return False

    # Verifying columns
    for j in range(n):
        col = [matrix[i][j] for i in range(n)]
        if set(col) != unique_digits:
            print("Error in col: ", col)
            return False

    # Verifying subsquares
    subsquare_coords = [(i, j) for i in range(m) for j in range(m)]
    for r_scalar in range(m):
        for c_scalar in range(m):
            subsquare = [matrix[i + r_scalar * m][j + c_scalar * m] for i, j
                         in subsquare_coords]
            if set(subsquare) != unique_digits:
                print("Error in sub-square: ", subsquare)
                return False

    return True


def var_repr(row, col, digit):
    """Returns a string of the cell coordinates and the cell value in a
    standard format.
    """
    return f'{row},{col}_{digit}'


def parse_label(label) -> tuple[int, int, int]:
    """parse label string and get row index, col index and cell's value """
    row_col, digit = label.split('_')
    row, col = row_col.split(',')
    return int(row), int(col), int(digit)
