import zmq

import cube


def validate_cube_state(cube: cube.Cube, faces_dict: dict[str, str]):
    if not my_cube.compare_state(faces):
        print("Error: Local cube state does not match server state.")
        print("Local Cube State:")
        print(my_cube)
        print("Server Cube State:")
        print("\n".join([f"{name}:\n{face}\n" for name, face in faces.items()]))
        exit(1)


class Client:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
    
    def send_json(self, data: dict):
        self.socket.send_json(data)
        return self.socket.recv_json()
    
    def get_state(self):
        return self.send_json({"action": "get_state"})
    
    def perform_move(self, move_code: str):
        return self.send_json({"action": "move", "code": move_code})
    
    def shuffle(self):
        return self.send_json({"action": "shuffle"})


print("\n--- Rubik's Cube Controller ---")
print("Commands: U, R, L, D, F, B, state, shuffle, exit")
print("-------------------------------\n")

client = Client()

my_cube = None
response = client.get_state()
if response.get("status") != "ok":
    print(f"Error: {response}")
    exit(1)

faces = response.get("faces")
print("\nCURRENT CUBE STATE:")

for face_name in ['U', 'R', 'F', 'D', 'L', 'B']:
    print(f"{face_name}: {faces[face_name]}")

my_cube = cube.Cube(faces, echo_move=lambda move: client.perform_move(move))

validate_cube_state(my_cube, faces)

while True:
    cmd = input("> ").strip()
    if not cmd: continue
    if cmd.lower() == 'exit': break
    response = None
    if cmd.lower() == 'state':
        response = client.get_state()
        if response.get("status") == "ok":
            faces = response.get("faces")
            print("\nCURRENT CUBE STATE:")
            # Виводимо кожну грань з нового рядка
            for face_name in ['U', 'R', 'F', 'D', 'L', 'B']:
                print(f"{face_name}: {faces[face_name]}")
            
            validate_cube_state(my_cube, faces)
        else:
            print(f"Error: {response}")
    elif cmd.lower() == 'shuffle':
        response = client.shuffle()
        new_state_response = client.get_state()
        if response.get("status") != "ok":
            print(f"Error: {response}")
            exit(1)
        my_cube = cube.Cube(new_state_response.get("faces"), echo_move=lambda move: client.perform_move(move))
        print("Cube shuffled.")
    elif cmd.lower() == "solve":
        from up_cross_solver import UpCrossSolver
        from up_corners_solver import UpCornersSolver
        from middle_layer_solver import MiddleLayerSolver
        from oll_solver import OLLSolver
        UpCrossSolver.solve(my_cube)
        UpCornersSolver.solve(my_cube)
        MiddleLayerSolver.solve(my_cube)
        OLLSolver.solve(my_cube)
    else:
        my_cube.perform_move(cmd)

        response = client.get_state()
        if response.get("status") != "ok":
            print(f"Error: {response}")
            exit(1)
        faces = response.get("faces")
        validate_cube_state(my_cube, faces)
    print(f"Response: {response}\n")