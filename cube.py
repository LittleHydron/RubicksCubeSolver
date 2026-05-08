class Face:
    def __init__(self, color_string: str):
        self.layout = list()
        for i in range(3):
            row = color_string[i*3:(i+1)*3]
            self.layout.append(list(row))
        self.center = self.layout[1][1]
    
    def __str__(self):
        return "".join(["".join(row) for row in self.layout])
    
    def get_row(self, idx: int):
        return self.layout[idx]
    
    def get_col(self, idx: int):
        return [self.layout[i][idx] for i in range(3)]
    
    def set_row(self, idx: int, values: list):
        self.layout[idx] = list(values)
    
    def set_col(self, idx: int, values: list):
        for i in range(3):
            self.layout[i][idx] = values[i]
    
    def rotate_cw(self):
        new_layout = [list(row) for row in self.layout]
        for i in range(3):
            for j in range(3):
                new_layout[j][2 - i] = self.layout[i][j]
        self.layout = new_layout
    
    def rotate_ccw(self):
        new_layout = [list(row) for row in self.layout]
        for i in range(3):
            for j in range(3):
                new_layout[2 - j][i] = self.layout[i][j]
        self.layout = new_layout


class Cube:
    def __init__(self, faces_dict: dict[str, str], echo_move=None):
        self.faces = {name: Face(colors) for name, colors in faces_dict.items()}
        self.echo_move = echo_move
        self.face_move = {
            'F': {
                'F': 'F', 'B': 'B', 'U': 'U', 'D': 'D', 'L': 'L', 'R': 'R'
            },
            'B': {
                'F': 'B',
                'B': 'F',
                'U': 'U',
                'D': 'D',
                'L': 'R',
                'R': 'L'
            },
            'U': {
                'F': 'U',
                'B': 'D',
                'U': 'B',
                'D': 'F',
                'L': 'L',
                'R': 'R'
            },
            'D': {
                'F': 'D',
                'B': 'U',
                'U': 'F',
                'D': 'B',
                'L': 'L',
                'R': 'R'
            },
            'L': {
                'F': 'L',
                'B': 'R',
                'U': 'U',
                'D': 'D',
                'L': 'B',
                'R': 'F'
            },
            'R': {
                'F': 'R',
                'B': 'L',
                'U': 'U',
                'D': 'D',
                'L': 'F',
                'R': 'B'
            }
        }

    def __str__(self):
        return "\n".join([f"{name}:\n{face}\n" for name, face in self.faces.items()])
    
    def compare_state(self, faces_dict: dict[str, str]) -> bool:
        for name, colors in faces_dict.items():
            if str(self.faces[name]) != colors:
                return False
        return True
    
    def get_face(self, name: str) -> Face:
        return self.faces[name]
    
    def get_left_face(self, face_name: str) -> str:
        if face_name == 'F': return 'L'
        elif face_name == 'B': return 'R'
        elif face_name == 'L': return 'B'
        elif face_name == 'R': return 'F'
        elif face_name == 'U': return 'L'
        elif face_name == 'D': return 'L'
    
    def get_right_face(self, face_name: str) -> str:
        if face_name == 'F': return 'R'
        elif face_name == 'B': return 'L'
        elif face_name == 'L': return 'F'
        elif face_name == 'R': return 'B'
        elif face_name == 'U': return 'R'
        elif face_name == 'D': return 'R'
    
    def get_upper_face(self, face_name: str) -> str:
        if face_name == 'F': return 'U'
        elif face_name == 'B': return 'U'
        elif face_name == 'L': return 'U'
        elif face_name == 'R': return 'U'
        elif face_name == 'U': return 'B'
        elif face_name == 'D': return 'F'
    
    def get_lower_face(self, face_name: str) -> str:
        if face_name == 'F': return 'D'
        elif face_name == 'B': return 'D'
        elif face_name == 'L': return 'D'
        elif face_name == 'R': return 'D'
        elif face_name == 'U': return 'F'
        elif face_name == 'D': return 'B'
    
    def get_other_colors_for_corner(self, face_name: str, row: int, col: int) -> list:
        colors = []
        if face_name == 'U':
            if row == 0 and col == 0:
                colors.append(self.faces['L'].get_row(0)[0])
                colors.append(self.faces['B'].get_row(0)[2])
            elif row == 0 and col == 2:
                colors.append(self.faces['R'].get_row(0)[2])
                colors.append(self.faces['B'].get_row(0)[0])
            elif row == 2 and col == 0:
                colors.append(self.faces['L'].get_row(0)[2])
                colors.append(self.faces['F'].get_row(0)[0])
            elif row == 2 and col == 2:
                colors.append(self.faces['R'].get_row(0)[0])
                colors.append(self.faces['F'].get_row(0)[2])
        elif face_name == 'D':
            if row == 0 and col == 0:
                colors.append(self.faces['L'].get_row(2)[2])
                colors.append(self.faces['F'].get_row(2)[0])
            elif row == 0 and col == 2:
                colors.append(self.faces['R'].get_row(2)[0])
                colors.append(self.faces['F'].get_row(2)[2])
            elif row == 2 and col == 0:
                colors.append(self.faces['L'].get_row(2)[0])
                colors.append(self.faces['B'].get_row(2)[2])
            elif row == 2 and col == 2:
                colors.append(self.faces['R'].get_row(2)[2])
                colors.append(self.faces['B'].get_row(2)[0])
        elif face_name == 'F':
            if row == 0 and col == 0:
                colors.append(self.faces['U'].get_row(2)[0])
                colors.append(self.faces['L'].get_row(0)[2])
            elif row == 0 and col == 2:
                colors.append(self.faces['U'].get_row(2)[2])
                colors.append(self.faces['R'].get_row(0)[0])
            elif row == 2 and col == 0:
                colors.append(self.faces['D'].get_row(0)[0])
                colors.append(self.faces['L'].get_row(2)[2])
            elif row == 2 and col == 2:
                colors.append(self.faces['D'].get_row(0)[2])
                colors.append(self.faces['R'].get_row(2)[0])
        elif face_name == 'B':
            if row == 0 and col == 0:
                colors.append(self.faces['U'].get_row(0)[2])
                colors.append(self.faces['R'].get_row(0)[2])
            elif row == 0 and col == 2:
                colors.append(self.faces['U'].get_row(0)[0])
                colors.append(self.faces['L'].get_row(0)[0])
            elif row == 2 and col == 0:
                colors.append(self.faces['D'].get_row(2)[2])
                colors.append(self.faces['R'].get_row(2)[2])
            elif row == 2 and col == 2:
                colors.append(self.faces['D'].get_row(2)[0])
                colors.append(self.faces['L'].get_row(2)[0])
        elif face_name == 'L':
            if row == 0 and col == 0:
                colors.append(self.faces['U'].get_row(0)[0])
                colors.append(self.faces['B'].get_row(0)[2])
            elif row == 0 and col == 2:
                colors.append(self.faces['U'].get_row(2)[0])
                colors.append(self.faces['F'].get_row(0)[0])
            elif row == 2 and col == 0:
                colors.append(self.faces['D'].get_row(2)[0])
                colors.append(self.faces['B'].get_row(2)[2])
            elif row == 2 and col == 2:
                colors.append(self.faces['F'].get_row(2)[0])
                colors.append(self.faces['D'].get_row(0)[0])
        elif face_name == 'R':
            if row == 0 and col == 0:
                colors.append(self.faces['U'].get_row(2)[2])
                colors.append(self.faces['F'].get_row(0)[2])
            elif row == 0 and col == 2:
                colors.append(self.faces['U'].get_row(0)[2])
                colors.append(self.faces['B'].get_row(0)[0])
            elif row == 2 and col == 0:
                colors.append(self.faces['D'].get_row(0)[2])
                colors.append(self.faces['F'].get_row(2)[2])
            elif row == 2 and col == 2:
                colors.append(self.faces['B'].get_row(2)[0])
                colors.append(self.faces['D'].get_row(2)[2])
        return colors

    def get_another_face_on_edge(self, face_name: str, row: int, col: int) -> str:
        if row == 0: # Top edge
            if face_name == 'D': return 'F'
            elif face_name == 'U': return 'B'
            else: return 'U'
        elif row == 2: # Bottom edge
            if face_name == 'U': return 'F'
            elif face_name == 'D': return 'B'
            else: return 'D'
        else: # Middle edge
            if face_name == 'F':
                if col == 0: return 'L'
                elif col == 2: return 'R'
            elif face_name == 'B':
                if col == 0: return 'R'
                elif col == 2: return 'L'
            elif face_name == 'L':
                if col == 0: return 'B'
                elif col == 2: return 'F'
            elif face_name == 'R':
                if col == 0: return 'F'
                elif col == 2: return 'B'
            elif face_name == 'U':
                if col == 0: return 'L'
                elif col == 2: return 'R'
            elif face_name == 'D':
                if col == 0: return 'L'
                elif col == 2: return 'R'
    
    def get_another_color_on_edge(self, face_name: str, row: int, col: int) -> str:
        if row == 0: # Top edge
            if face_name == 'F': return self.faces['U'].get_row(2)[1]
            elif face_name == 'B': return self.faces['U'].get_row(0)[1]
            elif face_name == 'L': return self.faces['U'].get_col(0)[1]
            elif face_name == 'R': return self.faces['U'].get_col(2)[1]
        elif row == 2: # Bottom edge
            if face_name == 'F': return self.faces['D'].get_row(0)[1]
            elif face_name == 'B': return self.faces['D'].get_row(2)[1]
            elif face_name == 'L': return self.faces['D'].get_col(0)[1]
            elif face_name == 'R': return self.faces['D'].get_col(2)[1]
        else: # Middle edge
            if face_name == 'F':
                if col == 0: return self.faces['L'].get_col(2)[1]
                elif col == 2: return self.faces['R'].get_col(0)[1]
            elif face_name == 'B':
                if col == 0: return self.faces['R'].get_col(2)[1]
                elif col == 2: return self.faces['L'].get_col(0)[1]
            elif face_name == 'L':
                if col == 0: return self.faces['B'].get_col(2)[1]
                elif col == 2: return self.faces['F'].get_col(0)[1]
            elif face_name == 'R':
                if col == 0: return self.faces['F'].get_col(2)[1]
                elif col == 2: return self.faces['B'].get_col(0)[1]
            elif face_name == 'U':
                if col == 0: return self.faces['L'].get_row(0)[1]
                elif col == 2: return self.faces['R'].get_row(0)[1]
            elif face_name == 'D':
                if col == 0: return self.faces['L'].get_row(2)[1]
                elif col == 2: return self.faces['R'].get_row(2)[1]
    
    def perform_move_on_face(self, face_name: str, move_code: str):
        move_code = move_code.strip()
        if not move_code: return
        base_move = move_code[0].upper()
        modifier = move_code[1:] if len(move_code) > 1 else ""
        self.perform_move(self.face_move[face_name][base_move] + modifier)

    def perform_move(self, move_code: str):
        move_code = move_code.strip()
        if not move_code: return
        base_move = move_code[0].upper()
        modifier = move_code[1:] if len(move_code) > 1 else ""
        if base_move == 'R':
            if modifier == "": self.rotate_r_cw()
            elif modifier == "'": self.rotate_r_ccw()
        elif base_move == 'U':
            if modifier == "": self.rotate_u_cw()
            elif modifier == "'": self.rotate_u_ccw()
        elif base_move == 'F':
            if modifier == "": self.rotate_f_cw()
            elif modifier == "'": self.rotate_f_ccw()
        elif base_move == 'D':
            if modifier == "": self.rotate_d_cw()
            elif modifier == "'": self.rotate_d_ccw()
        elif base_move == 'L':
            if modifier == "": self.rotate_l_cw()
            elif modifier == "'": self.rotate_l_ccw()
        elif base_move == 'B':
            if modifier == "": self.rotate_b_cw()
            elif modifier == "'": self.rotate_b_ccw()
        if self.echo_move:
            self.echo_move(move_code)
    
    def perform_moves(self, moves_str: str):
        moves = moves_str.split()
        for move in moves:
            self.perform_move(move)
    
    def perform_moves_on_face(self, face_name: str, moves_str: str):
        moves = moves_str.split()
        for move in moves:
            self.perform_move_on_face(face_name, move)

    def rotate_u_cw(self):
        self.faces['U'].rotate_cw()
        f, r, b, l = self.faces['F'], self.faces['R'], self.faces['B'], self.faces['L']
        temp = f.get_row(0)
        f.set_row(0, r.get_row(0))
        r.set_row(0, b.get_row(0))
        b.set_row(0, l.get_row(0))
        l.set_row(0, temp)

    def rotate_d_cw(self):
        self.faces['D'].rotate_cw()
        f, r, b, l = self.faces['F'], self.faces['R'], self.faces['B'], self.faces['L']
        temp = f.get_row(2)
        f.set_row(2, l.get_row(2))
        l.set_row(2, b.get_row(2))
        b.set_row(2, r.get_row(2))
        r.set_row(2, temp)

    def rotate_r_cw(self):
        self.faces['R'].rotate_cw()
        u, f, d, b = self.faces['U'], self.faces['F'], self.faces['D'], self.faces['B']
        temp = u.get_col(2)
        u.set_col(2, f.get_col(2))
        f.set_col(2, d.get_col(2))
        d.set_col(2, b.get_col(0)[::-1])
        b.set_col(0, temp[::-1])

    def rotate_l_cw(self):
        self.faces['L'].rotate_cw()
        u, f, d, b = self.faces['U'], self.faces['F'], self.faces['D'], self.faces['B']
        temp = u.get_col(0)
        u.set_col(0, b.get_col(2)[::-1])
        b.set_col(2, d.get_col(0)[::-1])
        d.set_col(0, f.get_col(0))
        f.set_col(0, temp)

    def rotate_f_cw(self):
        self.faces['F'].rotate_cw()
        u, r, d, l = self.faces['U'], self.faces['R'], self.faces['D'], self.faces['L']
        temp = u.get_row(2)
        u.set_row(2, l.get_col(2)[::-1])
        l.set_col(2, d.get_row(0))
        d.set_row(0, r.get_col(0)[::-1])
        r.set_col(0, temp)

    def rotate_b_cw(self):
        self.faces['B'].rotate_cw()
        u, r, d, l = self.faces['U'], self.faces['R'], self.faces['D'], self.faces['L']
        temp = u.get_row(0)
        u.set_row(0, r.get_col(2))
        r.set_col(2, d.get_row(2)[::-1])
        d.set_row(2, l.get_col(0))
        l.set_col(0, temp[::-1])

    def rotate_r_ccw(self):
        for _ in range(3): self.rotate_r_cw()

    def rotate_u_ccw(self):
        for _ in range(3): self.rotate_u_cw()

    def rotate_f_ccw(self):
        for _ in range(3): self.rotate_f_cw()

    def rotate_d_ccw(self):
        for _ in range(3): self.rotate_d_cw()

    def rotate_l_ccw(self):
        for _ in range(3): self.rotate_l_cw()

    def rotate_b_ccw(self):
        for _ in range(3): self.rotate_b_cw()
