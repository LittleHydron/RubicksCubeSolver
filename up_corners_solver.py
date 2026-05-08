from cube import Cube

class UpCornersSolver:
    PIF_PAF = "R' D' R D"

    @classmethod
    def remove_corners_from_U(cls, cube: Cube):
        for _, face in cube.faces.items():
            if face.center in ['U', 'D']:
                continue
            for j in [0, 2]:
                if face.get_row(0)[j] != 'U' and not ('U' in cube.get_other_colors_for_corner(face.center, row=0, col=j)):
                    continue
                face_to_work_with = face.center
                if j == 0:
                    face_to_work_with = cube.get_left_face(face.center)
                while face.get_row(2)[2] == 'U' or 'U' in cube.get_other_colors_for_corner(face.center, row=2, col=2):
                    cube.perform_moves_on_face(face_to_work_with, "D")
                cube.perform_moves_on_face(face_to_work_with, cls.PIF_PAF)

    @classmethod
    def solve(cls, cube: Cube):
        cls.remove_corners_from_U(cube)
        for _, face in cube.faces.items():
            if face.center in ['U', 'D']:
                continue
            right_face = cube.get_right_face(face.center)
            while set([face.get_row(2)[2]] + cube.get_other_colors_for_corner(face.center, row=2, col=2)) != set([face.center, 'U', right_face]):
                cube.perform_moves_on_face(face.center, "D")
            
            while set([face.get_row(0)[2]] + cube.get_other_colors_for_corner(face.center, row=0, col=2)) != set([face.center, 'U', right_face]) \
                    or face.get_row(0)[2] != face.center:
                cube.perform_moves_on_face(face.center, cls.PIF_PAF)
