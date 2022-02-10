from pysat.solvers import Glucose4


def read_file(path_file: str) -> list:
    file = open(path_file, "r")
    file_list = []
    for line in file:
        line = line.rstrip()
        file_list.append(line)
    file.close()
    return file_list


def get_board_mapping() -> tuple:
    board_mapping = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
    board_mapping_inv = []
    count = 1
    for i in range(9):
        for j in range(9):
            for k in range(9):
                board_mapping[i][j][k] = count
                board_mapping_inv.append([i, j, k])
                count += 1
    return (board_mapping, board_mapping_inv)


def add_clauses(board: list, board_mapping) -> Glucose4:
    solver = Glucose4()

    for i in range(9):
        for j in range(9):
            if board[i][j] != -1:
                solver.add_clause([board_mapping[i][j][board[i][j]]])

    for i in range(9):
        for j in range(9):
            clause = []
            for k in range(9):
                clause += [board_mapping[i][j][k]]
                for x in range(k + 1, 9):
                    solver.add_clause(
                        [-board_mapping[i][j][k], -board_mapping[i][j][x]]
                    )
            solver.add_clause(clause)

    for i in range(9):
        for j in range(9):
            for k in range(9):
                for x in range(k + 1, 9):
                    solver.add_clause(
                        [-board_mapping[k][i][j], -board_mapping[x][i][j]]
                    )

    for i in range(9):
        for j in range(9):
            for k in range(9):
                for x in range(k + 1, 9):
                    solver.add_clause(
                        [-board_mapping[i][k][j], -board_mapping[i][x][j]]
                    )

    for i in range(0, 7, 3):
        for j in range(0, 7, 3):
            for k in range(i, i + 3):
                for x in range(j, j + 3):
                    for m in range(9):
                        for n in range(i, i + 3):
                            for p in range(j, j + 3):
                                if k != n and x != p:
                                    solver.add_clause(
                                        [
                                            -board_mapping[k][x][m],
                                            -board_mapping[n][p][m],
                                        ]
                                    )

    return solver


def print_resolution(resolution, i) -> None:
    counter = 0
    print(f"{i} - solução: ")
    for i in range(9):
        for j in range(9):
            print(resolution[counter][2] + 1, end=" ")
            counter += 1
        print()
    print()


def loading_matrix(lines, board_mapping, board_mapping_inv) -> None:
    board = []
    count = 0
    for i in range(len(lines)):
        if not i % 10 == 9:
            board.append([int(j) - 1 for j in lines[i].split()])
        if i % 10 == 9:
            count += 1
            solver = add_clauses(board, board_mapping)
            if solver.solve():
                resolution = []
                for i in solver.get_model():
                    if i > 0:
                        resolution.append(board_mapping_inv[i - 1])

            print_resolution(resolution, count)
            board.clear()


def exec() -> None:
    boards = read_file("./assets/sudoku.txt")
    board_mapping, board_mapping_inv = get_board_mapping()
    loading_matrix(boards, board_mapping, board_mapping_inv)
