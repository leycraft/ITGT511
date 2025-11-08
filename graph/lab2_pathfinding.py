from weighted_node import WeightedNode, WeightedGraph
from DijkstraAlgorithm import DijkstraAlgorithm

graph = WeightedGraph()
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")
graph.add_node("E")

graph.add_edge("A", "B", 1)
graph.add_edge("A", "C", 1)
graph.add_edge("B", "D", 1)
graph.add_edge("C", "D", 1)
graph.add_edge("C", "E", 9)
graph.add_edge("D", "E", 1)

print(graph)

path = DijkstraAlgorithm.find_shortest_path(graph, "A", "E")
print(path)

path = DijkstraAlgorithm.find_shortest_path(graph, "A", "D")
print(path)