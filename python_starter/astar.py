import heapq
from hlt.positionals import Direction
import logging

class AStarNode:
    def __init__(self, position, g_cost = 0, h_cost = 0, parent = None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class AStar:
    def __init__(self, map):
        self.game_map = map

    def cal_h(self, pos1, pos2):
        return self.game_map.calculate_distance(pos1, pos2)

    def reconstruct_path(self, node):
        path = []
        current = node
        while current.parent is not None:
            parent_pos = current.parent.position
            current_pos = current.position
            dx = (current_pos.x - parent_pos.x)
            dy = (current_pos.y - parent_pos.y)

            if dx == 1 and dy == 0:
                direction = Direction.East
            elif dx == -1 and dy == 0:
                direction = Direction.West
            elif dx == 0 and dy == 1:
                direction = Direction.South
            elif dx == 0 and dy == -1:
                direction = Direction.North
            else:
                direction = Direction.Still

            path.append(direction)
            current = current.parent

        return path

    def get_next_move(self, ship, target_pos):
        path = self.find_path(ship.position, target_pos)

        if path:
            return path[0]
        else:
            return Direction.Still

    def find_path(self, start_pos, target_pos):
        open_list = []
        close_list = set()
        best_costs = {}
        best_costs[start_pos] = 0
        
        start_node = AStarNode(start_pos, 0, self.cal_h(start_pos, target_pos), None)
        # target_node = target

        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            close_list.add(current_node.position)

            if current_node.position == target_pos:
                return self.reconstruct_path(current_node)

            for dir in [Direction.North, Direction.South, Direction.East, Direction.West]:
                neigbor_pos = current_node.position.directional_offset(dir)

                if neigbor_pos in close_list:
                    continue

                move_cost = self.game_map[current_node.position].halite_amount / 100
                if self.game_map[neigbor_pos].is_occupied:
                    move_cost = 1000.0

                tentative_g_cost = current_node.g_cost + move_cost
                if neigbor_pos not in best_costs or tentative_g_cost < best_costs[neigbor_pos]:
                    h_cost = self.cal_h(neigbor_pos, target_pos)
                    neigbor_node = AStarNode(neigbor_pos, tentative_g_cost, h_cost, current_node)
                    heapq.heappush(open_list, neigbor_node)

