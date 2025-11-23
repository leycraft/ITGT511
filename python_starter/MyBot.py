import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging
from astar import AStar

""" <<<Game Begin>>> """

game = hlt.Game()

game.ready("Boseley")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

def get_move_direction(game_map, ship, target):
    pass



def get_direction(dx, dy):
    go_to = ship.stay_still()

    x = dx % 2
    y = dy % 2

    if dx > 0:
        if not game_map[ship.position + Position(1,0)].is_occupied:
            go_to = ship.move(Direction.East)
        else:
            go_to = ship.move(random.choice([Direction.South, Direction.North]))
    elif dx < 0:
        if not game_map[ship.position + Position(-1,0)].is_occupied:
            go_to = ship.move(Direction.West)
        else:
            go_to = ship.move(random.choice([Direction.South, Direction.North]))
    elif dy > 0:
        if not game_map[ship.position + Position(0,1)].is_occupied:
            go_to = ship.move(Direction.South)
        else:
            go_to = ship.move(random.choice([Direction.East, Direction.West]))
    elif dy < 0:
        if not game_map[ship.position + Position(0,-1)].is_occupied:
            go_to = ship.move(Direction.North)
        else:
            go_to = ship.move(random.choice([Direction.East, Direction.West]))

    return go_to

""" <<<Game Loop>>> """

ship_states = {}
ship_target = {}

astar = AStar(game.game_map)

while True:
    game.update_frame()

    me = game.me
    game_map = game.game_map

    command_queue = []

    home_base = me.shipyard.position

    # ship AI
    for ship in me.get_ships():
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:             
            if ship.id not in ship_states:
                ship_states[ship.id] = "finding"
            if ship.id not in ship_target:
                ship_target[ship.id] = ship.position

            # ------------------------------------------
            
            halite_num = 0
            halite_x = 0
            halite_y = 0

            ship_pos = ship.position

            dx = ship_target[ship.id].x - ship_pos.x
            dy = ship_target[ship.id].y - ship_pos.y

            move_to = ship.stay_still()

            if ship_states[ship.id] == "finding":
                # target = ship_target[ship.id]

                for i in range(32):
                    for j in range(32):
                        if game_map[Position(i,j)].halite_amount > halite_num and Position(i,j) not in ship_target.values():
                            halite_num = game_map[Position(i,j)].halite_amount
                            halite_x = i
                            halite_y = j
                            ship_target[ship.id] = Position(i,j)

                ship_states[ship.id] = "seeking"
                move_to = get_direction(dx, dy)




            elif ship_states[ship.id] == "seeking":
                move_to = get_direction(dx, dy)

                if game_map[ship.position].halite_amount > 500 or ship.position == ship_target[ship.id]:
                    ship_states[ship.id] = "collecting"

                if ship.is_full:
                    ship_states[ship.id] = "returning"

            elif ship_states[ship.id] == "collecting":
                move_to = ship.stay_still()

                if ship.is_full:
                    ship_states[ship.id] = "returning"
                elif game_map[ship.position].halite_amount < 100:
                    ship_states[ship.id] = "finding"

            elif ship_states[ship.id] == "returning": 
                ship_target[ship.id] = home_base

                # move_to = get_direction(dx, dy)
                move_to = ship.move(astar.get_next_move(ship, ship_target[ship.id]))

                if ship.position == home_base:
                    ship_states[ship.id] = "finding"
                

                # target = me.shipyard.position
                # direction = astar.get_next_move(ship, target)


            command_queue.append(move_to)


        else:
            command_queue.append(ship.stay_still())


    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)

