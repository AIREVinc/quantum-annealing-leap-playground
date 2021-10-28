# Copyright 2019 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import typer

from puzzle import get_matrix, is_correct
from models import build_bqm
from solvers import solve_sudoku


def main(
        filename: str = "problem.txt",
        solver_name: str = "qpu",
):
    mat = get_matrix(filename)
    bqm = build_bqm(mat)
    result, energy = solve_sudoku(bqm, mat, solver_name)

    for line in result:
        print(*line, sep=" ")   # Print list without commas or brackets

    print("bqm energy: ", energy)

    # Verify
    if is_correct(result):
        print("The solution is correct")
    else:
        print("The solution is incorrect")


if __name__ == "__main__":
    typer.run(main)
