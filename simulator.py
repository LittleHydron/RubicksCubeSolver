from vpython import *
import zmq

# --- Налаштування сцени ---
scene.title = "Rubik's Cube Simulator (VPython) - Fixed State"
scene.width = 1200
scene.height = 800
scene.background = color.gray(0.1)

# --- Налаштування ZMQ ---
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Кольорова схема (L/R та F/B налаштовані за твоїм запитом)
colors = {
    'U': color.white,       # Top
    'D': color.yellow,      # Bottom
    'L': color.red,         # Left
    'R': vector(1, 0.5, 0),  # Right (Orange)
    'F': color.blue,        # Front (ТЕПЕР СИНІЙ)
    'B': color.green        # Back (ТЕПЕР ЗЕЛЕНИЙ)
}

pieces = []

def create_cube():
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                p = box(pos=vec(x, y, z), size=vec(0.95, 0.95, 0.95), color=color.black)
                p.stickers = []
                s_size, s_thick = 0.8, 0.05
                
                if y == 1: 
                    s = box(pos=vec(x, y+0.48, z), size=vec(s_size, s_thick, s_size), color=colors['U'])
                    s.face_id = 'U'; s.my_piece = p; p.stickers.append(s)
                if y == -1: 
                    s = box(pos=vec(x, y-0.48, z), size=vec(s_size, s_thick, s_size), color=colors['D'])
                    s.face_id = 'D'; s.my_piece = p; p.stickers.append(s)
                if x == 1: 
                    s = box(pos=vec(x+0.48, y, z), size=vec(s_thick, s_size, s_size), color=colors['R'])
                    s.face_id = 'R'; s.my_piece = p; p.stickers.append(s)
                if x == -1: 
                    s = box(pos=vec(x-0.48, y, z), size=vec(s_thick, s_size, s_size), color=colors['L'])
                    s.face_id = 'L'; s.my_piece = p; p.stickers.append(s)
                if z == 1: # Front
                    s = box(pos=vec(x, y, z+0.48), size=vec(s_size, s_size, s_thick), color=colors['F'])
                    s.face_id = 'F'; s.my_piece = p; p.stickers.append(s)
                if z == -1: # Back
                    s = box(pos=vec(x, y, z-0.48), size=vec(s_size, s_size, s_thick), color=colors['B'])
                    s.face_id = 'B'; s.my_piece = p; p.stickers.append(s)
                pieces.append(p)

create_cube()

def rotate_side(side, direction=1):
    angle = -(pi / 2) * direction 
    if side == 'U': axis = vec(0,1,0); cond = lambda p: p.pos.y > 0.5
    elif side == 'D': axis = vec(0,1,0); cond = lambda p: p.pos.y < -0.5; angle *= -1
    elif side == 'L': axis = vec(1,0,0); cond = lambda p: p.pos.x < -0.5; angle *= -1
    elif side == 'R': axis = vec(1,0,0); cond = lambda p: p.pos.x > 0.5
    elif side == 'F': axis = vec(0,0,1); cond = lambda p: p.pos.z > 0.5
    elif side == 'B': axis = vec(0,0,1); cond = lambda p: p.pos.z < -0.5; angle *= -1
    else: return

    targets = [p for p in pieces if cond(p)]
    steps = 10
    for _ in range(steps):
        rate(150)
        for p in targets:
            p.rotate(angle=angle/steps, axis=axis, origin=vec(0,0,0))
            for s in p.stickers:
                s.rotate(angle=angle/steps, axis=axis, origin=vec(0,0,0))

def get_sticker_at(pos_vec):
    closest_sticker = None
    min_dist = 999
    for p in pieces:
        for s in p.stickers:
            dist = mag(s.pos - pos_vec)
            if dist < min_dist:
                min_dist = dist
                closest_sticker = s
    # Повертаємо назву кольору (id), а не об'єкт
    return closest_sticker.face_id if closest_sticker else "?"

def get_cube_state_structured():
    faces_data = {}
    # ВАЖЛИВО: точки сканування (1.5) знаходяться ПЕРЕД гранями
    scan_configs = [
        # U: y=1.5 | Рядки по Z (від -1 до 1), Стовпці по X (від -1 до 1)
        ('U', [vec(x, 1.5, z) for z in [-1, 0, 1] for x in [-1, 0, 1]]),
        # R: x=1.5 | Рядки по Y (від 1 до -1), Стовпці по Z (від 1 до -1)
        ('R', [vec(1.5, y, z) for y in [1, 0, -1] for z in [1, 0, -1]]),
        # F: z=1.5 | Рядки по Y (від 1 до -1), Стовпці по X (від -1 до 1)
        ('F', [vec(x, y, 1.5) for y in [1, 0, -1] for x in [-1, 0, 1]]),
        # D: y=-1.5| Рядки по Z (від 1 до -1), Стовпці по X (від -1 до 1)
        ('D', [vec(x, -1.5, z) for z in [1, 0, -1] for x in [-1, 0, 1]]),
        # L: x=-1.5| Рядки по Y (від 1 до -1), Стовпці по Z (від -1 до 1)
        ('L', [vec(-1.5, y, z) for y in [1, 0, -1] for z in [-1, 0, 1]]),
        # B: z=-1.5| Рядки по Y (від 1 до -1), Стовпці по X (від 1 до -1)
        ('B', [vec(x, y, -1.5) for y in [1, 0, -1] for x in [1, 0, -1]])
    ]
    
    for face_name, points in scan_configs:
        face_str = ""
        for pt in points:
            face_str += get_sticker_at(pt)
        faces_data[face_name] = face_str
    return faces_data

# Керування мишею та клавішами
scene.bind('mousedown', lambda e: rotate_side(scene.mouse.pick.face_id, -1 if e.shift else 1) if hasattr(scene.mouse.pick, 'face_id') else None)
scene.bind('keydown', lambda e: rotate_side(e.key.upper(), -1 if e.shift else 1) if e.key.upper() in 'URLDFB' else None)

while True:
    rate(60)
    try:
        msg = socket.recv_json(flags=zmq.NOBLOCK)
        action = msg.get("action")
        if action == "move":
            m = msg.get("code", "U").upper()
            direction = -1 if "'" in m else 1
            rotate_side(m[0], direction)
            if "2" in m: rotate_side(m[0], direction)
            socket.send_json({"status": "ok"})
        elif action == "get_state":
            socket.send_json({"status": "ok", "faces": get_cube_state_structured()})
        elif action == "shuffle":
            import random
            for _ in range(10): rotate_side(random.choice('URLDFB'), random.choice([1, -1]))
            socket.send_json({"status": "ok"})
    except zmq.Again: pass