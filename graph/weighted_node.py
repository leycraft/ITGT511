class WeightedNode:
    def __init__(self, value):
        self.value = value
        self.neighbors = {}
        self.visited = False
        self.distance = float('inf')
        self.previous = None

    def add_neighbor(self, neighbor, weight):
        self.neighbors[neighbor] = weight
        
    def __str__(self):
        return f"WeightedNode({self.value})"
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        return self.distance < other.distance
    
class WeightedGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, value):
        if value not in self.nodes:
            self.nodes[value] = WeightedNode(value)

        return self.nodes[value]
    
    def add_edge(self, from_value, to_value, weight):
        from_node = self.add_node(from_value)
        to_node = self.add_node(to_value)
        from_node.add_neighbor(to_node, weight)

    def get_node(self, value):
        return self.nodes.get(value)
    
    def reset_nodes(self):
        for node in self.nodes.values():
            node.visited = False
            node.distance = float('inf')
            node.previous = None

    def __str__(self):
        edges  = []
        for value, node in self.nodes.items():
            for neighbor, weight in node.neighbors.items():
                edges.append(f"{value} --({weight})-- {neighbor.value}")

        print(edges)

        return f"WeightedNode({len(self.nodes)} nodes, {len(edges)} edges)"