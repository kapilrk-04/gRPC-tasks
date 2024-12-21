from concurrent import futures
import logging
import random

import grpc

# import sys
# sys.path.append('../')
# from protofiles import labyrinth_pb2, labyrinth_pb2_grpc

import labyrinth_pb2, labyrinth_pb2_grpc

# def update_grid(grid, player, coin_tiles, wall_tiles):

def generate_coin_tiles(width, height, num_coins):
    coin_tiles = []
    while len(coin_tiles) < num_coins:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if (x, y) not in coin_tiles and (x, y) != (0, 0) and (x, y) != (width - 1, height - 1):
            coin_tiles.append((x, y))
    return coin_tiles

def generate_wall_tiles(width, height, num_walls, coin_tiles):
    wall_tiles = []
    while len(wall_tiles) < num_walls:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if (x, y) not in wall_tiles and (x, y) not in coin_tiles and (x, y) != (0, 0) and (x, y) != (width - 1, height - 1):
            wall_tiles.append((x, y))
    return wall_tiles


class LabyrinthServicer(labyrinth_pb2_grpc.LabyrinthServiceServicer):
    def __init__(self):
        self.width = random.randint(3, 5)
        self.height = random.randint(3, 5)

        self.grid = [['*' for _ in range(self.width)] for _ in range(self.height)]

        self.grid[0][0] = 'O'

        self.num_coins = random.randint(3, 7)
        self.num_walls = random.randint(3, 7)

        self.coin_tiles = generate_coin_tiles(self.width, self.height, self.num_coins)
        self.wall_tiles = generate_wall_tiles(self.width, self.height, self.num_walls, self.coin_tiles)

        logging.info(f"Width: {self.width}, Height: {self.height}")
        logging.info(f"Coins: {self.coin_tiles}")
        logging.info(f"Walls: {self.wall_tiles}")

        self.player = {
            'x': 0,
            'y': 0,
            'hp': 3,
            'rem_spells': 3,
            'score': 0,
        }

    def GetGrid(self, request, context):
        return labyrinth_pb2.Grid(
            gridrow=[labyrinth_pb2.GridRow(val=row) for row in self.grid]
        )

    def GetLabyrinthInfo(self, request, context):
        return labyrinth_pb2.LabyrinthInfo(
            width=self.width,
            height=self.height,
        )
    
    def GetPlayerStatus(self, request, context):
        return labyrinth_pb2.PlayerStatus(
            x=self.player['x'],
            y=self.player['y'],
            hp=self.player['hp'],
            rem_spells=self.player['rem_spells'],
            score=self.player['score'],
        )
    
    def RegisterMove(self, request, context):
        mapping = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0),
        }
        dx, dy = mapping[request.direction.upper()]
        new_x = self.player['x'] + dx
        new_y = self.player['y'] + dy

        # moved to winnning tile
        if (new_x, new_y) == (self.width - 1, self.height - 1):
            return labyrinth_pb2.MoveResponse(
                status=3
            )
        
        # moved to wall or out of bounds
        if ((new_x, new_y) in self.wall_tiles) or (new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height):
            self.player['hp'] -= 1
            if self.player['hp'] <= 0:
                return labyrinth_pb2.MoveResponse(
                    status=4
                )
            
            if (new_x, new_y) in self.wall_tiles:
                logging.info(f"Wall encountered at {new_x}, {new_y}")
                self.grid[new_y][new_x] = 'W'

            return labyrinth_pb2.MoveResponse(
                status=2
            )
        
        
        # moved to coin
        if (new_x, new_y) in self.coin_tiles:
            self.player['score'] += 1
            self.coin_tiles.remove((new_x, new_y))

        self.grid[self.player['y']][self.player['x']] = 'E'

        # normal move (also includes coin move)
        self.player['x'] = new_x
        self.player['y'] = new_y
        
        self.grid[self.player['y']][self.player['x']] = 'O'

        return labyrinth_pb2.MoveResponse(
            status=1
        )
        
    def Revelio(self, request, context):
        if self.player['rem_spells'] > 0:
            self.player['rem_spells'] -= 1
            store = [[],[],[]]
            # iterate over target tile and all surrounding tiles
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = request.x + i
                    y = request.y + j
                    if (x, y) in self.coin_tiles:
                        store[0].append((x, y))
                    elif (x, y) in self.wall_tiles:
                        store[1].append((x, y))
                    else:
                        store[2].append((x, y))

            logging.info(f"Revelio: {request.tile_type} around {request.x}, {request.y}")
            logging.info(f"Coins: {store[0]}")
            logging.info(f"Walls: {store[1]}")
            logging.info(f"Empty: {store[2]}")

            mp = {
                1 : 'C',
                2 : 'W',
                3 : 'E',
            }

            for ij in store[request.tile_type - 1]:
                self.grid[ij[1]][ij[0]] = mp[request.tile_type]

                yield labyrinth_pb2.TilePosition(
                    x=ij[0],
                    y=ij[1],
                )
        else:
            yield labyrinth_pb2.TilePosition(
                x=-1,
                y=-1,
            )

    def Bombarda(self, request_iterator, context):
        if self.player['rem_spells'] > 0:

            self.player['rem_spells'] -= 1
            for tile in request_iterator:

                logging.info(f"Bombarda: {tile.x}, {tile.y}")

                if tile.x < 0 or tile.x >= self.width or tile.y < 0 or tile.y >= self.height:
                    continue

                if (tile.x, tile.y) in self.wall_tiles:
                    self.wall_tiles.remove((tile.x, tile.y))
                    logging.info(f"Wall destroyed at {tile.x}, {tile.y}")

                elif (tile.x, tile.y) in self.coin_tiles:
                    self.coin_tiles.remove((tile.x, tile.y))
                    logging.info(f"Coin destroyed at {tile.x}, {tile.y}")

                self.grid[tile.y][tile.x] = 'E'

        else:
            return labyrinth_pb2.BombardaResponse(
                status='Failure - No spells left'
            )
        
        return labyrinth_pb2.BombardaResponse(
                status='Success'
            )

    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    labyrinth_pb2_grpc.add_LabyrinthServiceServicer_to_server(LabyrinthServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(
        filename="labyrinth.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    serve()

             

