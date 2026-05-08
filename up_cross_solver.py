from cube import Cube


class UpCrossSolver:
    @classmethod
    def make_cross_on_D(cls, cube: Cube):
        moved = True
        while moved:
            moved = False
            for face in cube.faces.values():
                if face.center == 'D':
                    continue
                row_ind = -1
                col_ind = -1
                for i in range(3):
                    row = face.get_row(i)
                    for j in range(3):
                        if row[j] == 'U' and ((i == 1) ^ (j == 1)):
                            row_ind = i
                            col_ind = j
                            break
                    if row_ind != -1:
                        break
                if row_ind == -1:
                    continue
                moved = True
                # print(f"[DEBUGGING ALO] Found U edge on face {face.center} at row {row_ind}, col {col_ind}")
                if face.center == 'U':
                    another_face = cube.get_another_face_on_edge(face.center, row=row_ind, col=col_ind)
                    while cube.get_another_color_on_edge(another_face, row=2, col=1) == 'U':
                        cube.perform_move_on_face(another_face, "D")
                    
                    if row_ind == 0:
                        cube.perform_moves_on_face(face.center, "U U")
                    elif row_ind == 2:
                        cube.perform_moves_on_face(face.center, "D D")
                    else:
                        if col_ind == 0:
                            cube.perform_moves_on_face(face.center, "L L")
                        else:
                            cube.perform_moves_on_face(face.center, "R R")
                else:
                    while cube.get_another_color_on_edge(face.center, row=2, col=1) == 'U':
                        cube.perform_move_on_face(face.center, "D")
                    if row_ind == 0:
                        cube.perform_moves_on_face(face.center, "F D R'")
                    elif row_ind == 2:
                        cube.perform_moves_on_face(face.center, "F' D R'")
                    elif col_ind == 0:
                        cube.perform_moves_on_face(face.center, "D' L")
                    else:
                        cube.perform_moves_on_face(face.center, "D R'")
                break

    @classmethod
    def solve(cls, cube: Cube):
        cls.make_cross_on_D(cube)
        for _, face in cube.faces.items():
            if face.center in ['U', 'D']:
                continue
            while face.get_row(2)[1] != face.center or cube.get_another_color_on_edge(face.center, row=2, col=1) != 'U':
                cube.perform_moves_on_face(face.center, "D")
            cube.perform_moves_on_face(face.center, "F F")
