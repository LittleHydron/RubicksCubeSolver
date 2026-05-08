from cube import Cube


class MiddleLayerSolver:
    INSERTION_R = "D' R' D R D F D' F'"
    INSERTION_L = "D L D' L' D' F' D F"

    @classmethod
    def remove_D_from_middle(cls, cube: Cube):
        for _, face in cube.faces.items():
            if face.center in ['U', 'D']:
                continue
            if face.get_row(1)[2] == 'D' or cube.get_another_color_on_edge(face.center, row=1, col=2) == 'D':
                continue
            while face.get_row(2)[1] != 'D' and cube.get_another_color_on_edge(face.center, row=2, col=1) != 'D':
                cube.perform_moves_on_face(face.center, "D")
            cube.perform_moves_on_face(face.center, cls.INSERTION_R)

    @classmethod
    def solve(cls, cube: Cube):
        cls.remove_D_from_middle(cube)
        for _, face in cube.faces.items():
            if face.center in ['U', 'D']:
                continue
            wanted_colors = set([face.center, cube.get_right_face(face.center)])
            while set([face.get_row(2)[1], cube.get_another_color_on_edge(face.center, row=2, col=1)]) != wanted_colors:
                cube.perform_moves_on_face(face.center, "D")
            
            if face.get_row(2)[1] == face.center:
                cube.perform_moves_on_face(face.center, cls.INSERTION_R)
            else:
                cube.perform_moves_on_face(face.center, "D")
                cube.perform_moves_on_face(cube.get_right_face(face.center), cls.INSERTION_L)
