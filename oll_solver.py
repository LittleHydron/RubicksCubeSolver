from cube import Cube

class OLLSolver:
    PIF_PAF = "R' D' R D"

    @classmethod
    def build_cross_on_D(cls, cube: Cube):
        cnt_D_edges_on_D = 0
        for i in range(3):
            for j in range(3):
                if not ((i == 1) ^ (j == 1)):
                    continue
                if cube.get_face('D').get_row(i)[j] == 'D':
                    cnt_D_edges_on_D += 1
        if cnt_D_edges_on_D == 4:
            return
        elif cnt_D_edges_on_D == 0:
            cube.perform_moves_on_face('F', "F' " + cls.PIF_PAF + " F D D F' " + cls.PIF_PAF + " F")
            print("OLL 1")
            return
        if cube.get_face('D').get_row(1)[0] == 'D' and cube.get_face('D').get_row(1)[2] == 'D':
            cube.perform_moves_on_face('F', "F' " + cls.PIF_PAF + " F")
            print("OLL 2")
            return
        if cube.get_face('D').get_row(0)[1] == 'D' and cube.get_face('D').get_row(2)[1] == 'D':
            cube.perform_moves_on_face('R', "F' " + cls.PIF_PAF + " F")
            print("OLL 3")
            return
        while cube.get_face('D').get_row(1)[0] != 'D' or cube.get_face('D').get_row(2)[1] != 'D':
            cube.perform_moves_on_face('F', "D")
        cube.perform_moves_on_face('F', "F' " + cls.PIF_PAF + " " + cls.PIF_PAF + " F")
        print("OLL 4")
        

    @classmethod
    def solve(cls, cube: Cube):
        cls.build_cross_on_D(cube)

