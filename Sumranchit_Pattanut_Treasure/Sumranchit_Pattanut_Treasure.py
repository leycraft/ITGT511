from collections import deque
from tree_node import TreeNode

def BFS_find_value(root, target):
    if not root.is_root():
        return []
    
    result = []
    queue = deque([root])
    path = deque([])
    node_tracing = None

    while(queue):
        node = queue.popleft()
        result.append(node.value)

        if(node == target):
            node_tracing = node

            while node_tracing != None:
                path.append(node_tracing)

                if not node_tracing.is_root():
                    node_tracing = node_tracing.parent[0]
                else:
                    node_tracing = None

            path.reverse()
            return path

        for child in node.children:
            queue.append(child)

def DFS_find_value(root, target):
    if not root.is_root():
        return []
    
    result = []
    stack = deque([root])
    path = deque([])
    node_tracing = None

    while(stack):
        node = stack.pop()
        result.append(node.value)

        if(node == target):
            node_tracing = node

            while node_tracing != None:
                path.append(node_tracing)

                if not node_tracing.is_root():
                    node_tracing = node_tracing.parent[-1]
                else:
                    node_tracing = None
            
            path.reverse()
            return path

        for child in reversed(node.children):
            stack.append(child)



# build map

a = TreeNode("A")
b = TreeNode("B")
c = TreeNode("C")
d = TreeNode("D")

a.add_child(b)
a.add_child(c)
b.add_child(d)
c.add_child(d)

# assign nodes

start_node = a
target_node = d

# search withh BFS and DFS

BFS_path = BFS_find_value(start_node, target_node)
DFS_path = DFS_find_value(start_node, target_node)

# print results

print("--- Treasure Hunt Results ---")
print("Start Node: " + str(start_node))
print("Treasure Location: " + str(target_node) + "\n")
print("Path found by BFS (Shortest Path): ", end="")

for i in BFS_path:
    print(i, end="")

    if i != BFS_path[-1]:
        print(" -> ", end="")
print("")

print("Path found by DFS (A Path): ", end="")
for i in DFS_path:
    print(i, end="")

    if i != DFS_path[-1]:
        print(" -> ", end="")