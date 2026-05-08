# CubeSim

A comprehensive Rubik's Cube simulator and solver implemented in Python, featuring a 3D visual interface and automated solving algorithms.

## Features

- **3D Visual Simulation**: Interactive 3D cube visualization using VPython
- **Command-Line Control**: Manual cube manipulation through a text-based interface
- **Automated Solvers**: Step-by-step solving algorithms for:
  - Up Cross
  - Up Corners
  - Middle Layer
  - OLL (Orient Last Layer)
- **ZMQ Communication**: Seamless communication between the visual simulator and control interface
- **State Validation**: Ensures synchronization between local and server cube states

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cubesim.git
   cd cubesim
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Visual Simulator

Start the 3D simulator in one terminal:
```bash
python simulator.py
```

You can specify a custom port (default is 5555):
```bash
python simulator.py --port 8080
```

### Using the Command-Line Controller

In another terminal, run the client for manual control:
```bash
python client.py
```

You can specify a custom port to connect to the simulator (default is 5555):
```bash
python client.py --port 8080
```

Available commands:
- `U`, `R`, `L`, `D`, `F`, `B`: Rotate faces (clockwise)
- `U'`, `R'`, etc.: Counter-clockwise rotations
- `state`: Display current cube state
- `shuffle`: Randomly scramble the cube
- `exit`: Quit the controller

### Using the Solvers

The solvers can be imported and used programmatically:

```python
from cube import Cube
from solvers.up_cross_solver import UpCrossSolver
from solvers.up_corners_solver import UpCornersSolver
from solvers.middle_layer_solver import MiddleLayerSolver
from solvers.oll_solver import OLLSolver

# Create a cube instance
cube = Cube({...})  # Initialize with face colors

# Solve step by step
UpCrossSolver.solve(cube)
UpCornersSolver.solve(cube)
MiddleLayerSolver.solve(cube)
OLLSolver.solve(cube)
```

## Project Structure

```
RubicksCubeSolver/
├── cube.py                            # Core cube representation and manipulation logic
├── simulator.py                       # 3D visual simulator using VPython and ZMQ
├── client.py                          # Command-line interface for cube control
├── solvers/                           # Solving algorithms package
│   ├── __init__.py
│   ├── up_cross_solver.py             # Solver for the white cross on the bottom face
│   ├── up_corners_solver.py           # Solver for positioning white corners
│   ├── middle_layer_solver.py         # Solver for the middle layer edges
│   └── oll_solver.py                  # Orient Last Layer solver
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
└── .venv/                             # Virtual environment (optional)
```

**Core Modules:**
- `cube.py`: Defines the `Cube` and `Face` classes for cube representation, state management, and move execution
- `simulator.py`: Runs the 3D visualization server using VPython with ZMQ for network communication
- `client.py`: Provides an interactive command-line interface to control the cube simulator

**Solvers Package:**
All solving algorithms are organized in the `solvers/` subpackage, implementing the CFOP (Fridrich) method:
1. `UpCrossSolver`: Creates the white cross on the bottom layer
2. `UpCornersSolver`: Positions and orients white corner pieces
3. `MiddleLayerSolver`: Solves the middle layer edges
4. `OLLSolver`: Orients the last layer pieces

## Requirements

- Python 3.6+
- VPython
- PyZMQ
- Additional dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source. Please check the license file for details.
