#### INSTRUCTIONS

- From `Q1` directory, run
```bash
sh protofiles/gen_proto.sh
```
to generate the protobuf files.

Go to `server` directory and run
```bash
python3 server.py
```

Go to `client` directory and run
```bash
python3 client.py
```

# Labyrinth Game gRPC Server

## Overview
The Labyrinth Game is a server-side implementation that allows multiple players to navigate a grid-based labyrinth, collect coins, and encounter walls. The server uses gRPC for communication with client applications.

## Dependencies
- **grpc**: A high-performance RPC framework.
- **random**: Used for generating random numbers for the labyrinth dimensions, coin placement, and wall placement.
- **logging**: For logging server activities.

## Protobuf Definitions
This server relies on the following protobuf definitions (assumed to be defined in `labyrinth_pb2.py` and `labyrinth_pb2_grpc.py`):
- **`Grid`**: Represents the labyrinth grid.
- **`GridRow`**: Represents a row in the grid.
- **`LabyrinthInfo`**: Contains the width and height of the labyrinth.
- **`PlayerStatus`**: Contains player status information.
- **`MoveResponse`**: Response for movement actions.
- **`TilePosition`**: Represents the position of tiles in the grid.
- **`BombardaResponse`**: Response for the Bombarda spell action.

## Class: `LabyrinthServicer`
This class implements the labyrinth game logic and the gRPC service.

Here’s the content formatted in Markdown:

```markdown
# Labyrinth Game gRPC Server

## Constructor
```python
def __init__(self):
    """Initializes the labyrinth with random dimensions, coin tiles, and wall tiles.
    Sets player attributes (position, health points, remaining spells, and score).
    """
```

## Methods

### GetGrid
```python
def GetGrid(self, request, context):
    """Returns the current grid layout of the labyrinth.
    
    Parameters:
    - request: Contains the request details.
    - context: Provides information about the RPC call.
    
    Returns: A Grid object with the current grid representation.
    """
```

### GetLabyrinthInfo
```python
def GetLabyrinthInfo(self, request, context):
    """Provides information about the labyrinth's dimensions.
    
    Parameters:
    - request: Contains the request details.
    - context: Provides information about the RPC call.
    
    Returns: A LabyrinthInfo object containing the width and height.
    """
```

### GetPlayerStatus
```python
def GetPlayerStatus(self, request, context):
    """Returns the current status of the player.
    
    Parameters:
    - request: Contains the request details.
    - context: Provides information about the RPC call.
    
    Returns: A PlayerStatus object with the player's current position, health points, remaining spells, and score.
    """
```

### RegisterMove
```python
def RegisterMove(self, request, context):
    """Processes the player's movement in the labyrinth.
    
    Parameters:
    - request: Contains the direction of movement (UP, DOWN, LEFT, RIGHT).
    - context: Provides information about the RPC call.
    
    Returns: A MoveResponse indicating the result of the movement:
    - status=1: Successful move (normal or coin collection).
    - status=2: Moved to a wall or out of bounds.
    - status=3: Moved to the winning tile.
    - status=4: Player's health has reached zero.
    """
```

### Revelio
```python
def Revelio(self, request, context):
    """Reveals nearby tiles based on the player's spell usage.
    
    Parameters:
    - request: Contains the position and tile type to reveal.
    - context: Provides information about the RPC call.
    
    Returns: Yields TilePosition for the revealed tiles. Returns (-1, -1) if no spells are left.
    """
```

### Bombarda
```python
def Bombarda(self, request_iterator, context):
    """Processes the Bombarda spell, allowing the player to destroy walls or coins.
    
    Parameters:
    - request_iterator: An iterator containing tile positions to target for destruction.
    - context: Provides information about the RPC call.
    
    Returns: A BombardaResponse indicating the success or failure of the action.
    """
```

### Function: serve
```python
def serve():
    """Initializes and starts the gRPC server.
    
    Returns: None; the server runs indefinitely.
    """
```

## Logging
Logs are written to `labyrinth.log`, capturing key events and player actions in the server.

### Example Log Entry
```yaml
2024-10-22 10:00:00 - INFO - Width: 4, Height: 3
2024-10-22 10:00:01 - INFO - Coins: [(1, 2), (2, 0)]
```

## Usage
Ensure that the protobuf definitions are correctly implemented and compiled. Run the server using Python:
```bash
python server.py
```
The server will listen on port 50051 for incoming gRPC requests.


# Labyrinth Game gRPC Client

## Overview
This Python client connects to a gRPC server for a labyrinth game, allowing the player to interact with the game world through various commands. It supports functionalities such as retrieving labyrinth information, player status, registering moves, and using spells.

## Dependencies
- `grpcio`
- `grpcio-tools`
- `labyrinth_pb2`
- `labyrinth_pb2_grpc`

## Functions

### gen_tiles_iterator
```python
def gen_tiles_iterator(tiles):
    """Generates an iterator for target tile positions.

    Args:
        tiles (list of tuples): A list of (x, y) coordinates.

    Yields:
        labyrinth_pb2.TargetPosition: Tile positions.
    """
```

### get_labyrinth_info
```python
def get_labyrinth_info(stub):
    """Retrieves and prints the dimensions of the labyrinth.

    Args:
        stub (LabyrinthServiceStub): The gRPC service stub.
    """
```

### get_player_status
```python
def get_player_status(stub):
    """Retrieves and prints the current status of the player.

    Args:
        stub (LabyrinthServiceStub): The gRPC service stub.
    """
```

### revelio
```python
def revelio(stub, x, y, tile_type):
    """Uses the Revelio spell to reveal nearby tiles.

    Args:
        stub (LabyrinthServiceStub): The gRPC service stub.
        x (int): The x-coordinate of the target.
        y (int): The y-coordinate of the target.
        tile_type (int): The type of tile to reveal (1: Coin, 2: Wall, 3: Exit).
    """
```

### bombarda
```python
def bombarda(stub, tiles):
    """Uses the Bombarda spell to destroy specified tiles.

    Args:
        stub (LabyrinthServiceStub): The gRPC service stub.
        tiles (list of tuples): A list of (x, y) coordinates for tiles to destroy.
    """
```

### register_move
```python
def register_move(stub, direction):
    """Registers a player's movement in the labyrinth.

    Args:
        stub (LabyrinthServiceStub): The gRPC service stub.
        direction (str): The direction to move (UP, DOWN, LEFT, RIGHT).

    Returns:
        int: Status of the move (1: valid move, 2: invalid move, 3: win, 4: lose).
    """
```

### get_grid
```python
def get_grid(stub):
    """Retrieves and prints the current grid layout of the labyrinth.

    Args:
        stub (LabyrinthServiceStub): The gRPC service stub.
    """
```

### run
```python
def run():
    """Main function to run the gRPC client.

    Initializes the gRPC channel and command-line interface for player interaction.
    """
```

## Command Line Interface
The client presents a command line interface with the following commands:

1. **GetLabyrinthInfo**: Retrieve the dimensions of the labyrinth.
2. **GetPlayerStatus**: Retrieve the current status of the player.
3. **RegisterMove**: Move the player in a specified direction.
4. **Revelio**: Reveal nearby tiles.
5. **Bombarda**: Destroy specified tiles.

## Example Usage
To run the client, execute the following command in the terminal:
```bash
python client.py
```

## Logging
The client uses the Python `logging` module for logging events. By default, logs are printed to the console.

## Note
Ensure that the gRPC server is running and listening on `localhost:50051` before starting the client.
```
