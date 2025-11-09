import heapq

class AStarAlgorithm:
    @staticmethod
    def h_dist_square(node1, node2):
        return (node1.x - node2.x)**2 + (node1.y - node2.y)**2

    @staticmethod
    def find_shortest_path(graph, start_value, end_value):
        graph.reset_nodes()

        start_node = graph.get_node(start_value)
        end_node = graph.get_node(end_value)

        priority_queue = [(0, start_node)]

        while priority_queue:
            current_distance, current_node = heapq. heappop(priority_queue)

            current_node.visited = True

            if(current_node == end_node):
                break

            for neighbor, weight in current_node.neighbors.items():
                if neighbor.visited:
                    continue

                h = AStarAlgorithm.h_dist_square(neighbor, end_node)
                print(h)

                # cost function
                new_distance = current_distance + weight + h

                if new_distance < neighbor.distance:
                    neighbor.distance = new_distance
                    neighbor.previous = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        path = []
        current = end_node
        while current:
            path.append(current.value)
            current = current.previous

        path.reverse()

        if path[0] == start_value:
            return path, end_node.distance
        else:
            return None, float('inf')