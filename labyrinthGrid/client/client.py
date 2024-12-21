import logging
import random

import grpc

# import sys
# sys.path.append('../')
# from protofiles import labyrinth_pb2, labyrinth_pb2_grpc

import labyrinth_pb2, labyrinth_pb2_grpc

def gen_tiles_iterator(tiles):
    for tile in tiles:
        yield labyrinth_pb2.TargetPosition(x=tile[0], y=tile[1])

def get_labyrinth_info(stub):
    response = stub.GetLabyrinthInfo(labyrinth_pb2.Empty())
    print(f"Width: {response.width}, Height: {response.height}")

def get_player_status(stub):
    response = stub.GetPlayerStatus(labyrinth_pb2.Empty())
    print(f"Player status: x={response.x}, y={response.y}, hp={response.hp}, rem_spells={response.rem_spells}, score={response.score}")

def revelio(stub,x,y,tile_type):
    responses = stub.Revelio(labyrinth_pb2.RevelioRequest(x=x, y=y, tile_type=tile_type))
    print(f"Revelio: {tile_type} around {x}, {y}")
    for response in responses:
        if response.x == -1 and response.y == -1:
            print("You have no more spells left!")
        else:
            print(f"{response.x}, {response.y}")

def bombarda(stub,tiles):
    # generate an iterator from tiles array
    target_iter = gen_tiles_iterator(tiles)
    response = stub.Bombarda(target_iter)
    print(f"Bombarda Status: {response.status}")

def register_move(stub, direction):
    if direction.upper() not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        print("Invalid direction")
        return
    response = stub.RegisterMove(labyrinth_pb2.MoveRequest(direction=direction))
    if response.status == 2:
        print("Invalid move")
    elif response.status == 3:
        print("You have won")
    elif response.status == 4:
        print("You have lost")
    else:
        print("Valid move")

    return response.status

def get_grid(stub):
    response = stub.GetGrid(labyrinth_pb2.Empty())
    for row in response.gridrow:
        for val in row.val:
            print(val, end=' ')
        print()


def run():
    with grpc.insecure_channel('localhost:50051') as channel:        
        # CREATE A COMMAND LINE INTERFACE FOR THE CLIENT
        stub = labyrinth_pb2_grpc.LabyrinthServiceStub(channel)
        print("Welcome to Labyrinth Game")
        print("Commands:")
        print("1. GetLabyrinthInfo")
        print("2. GetPlayerStatus")
        print("3. RegisterMove")
        print("4. Revelio")
        print("5. Bombarda")
        while True:
            print("\n")
            get_grid(stub)

            command = input("Enter command: ")
            if command == '1':
                get_labyrinth_info(stub)
            elif command == '2':
                get_player_status(stub)
            elif command == '3':
                direction = input("Enter direction: ")
                res = register_move(stub, direction)
                if res >= 3:
                    break
            elif command == '4':
                # REVELIO
                x = int(input("Enter target x: "))
                y = int(input("Enter target y: "))
                print("\nTile types:")
                print("1. Coin\t2. Wall\t3. Exit\n")
                tile_type = int(input("Enter tile type: "))
                revelio(stub, x, y, tile_type)
            elif command == '5':
                # BOMBARDA
                print("Enter 3 tiles to bombarda")
                tiles = []
                for _ in range(3):
                    x = int(input("Enter x: "))
                    y = int(input("Enter y: "))
                    tiles.append((x, y))
                    print("\n")
                bombarda(stub, tiles)
            else:
                print("Invalid command")

if __name__ == '__main__':
    logging.basicConfig()
    run()