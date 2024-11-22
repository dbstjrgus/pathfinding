from math import sqrt
from pyvis.network import Network
import heapq
import random
import streamlit as st


# Node class
class Node:
    def __init__(self, id, x=0, y=0, label=None):
        self.id = id
        self.x = x
        self.y = y
        self.fscore = float('inf')  # Initialize to infinity
        self.gscore = float('inf')  # Initialize to infinity
        self.previous = None
        self.label = label

    # manhattan distance
    def distance(self, node):
        return sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)


# Heuristic function, also manhattan distance
def heuristic(node, goal):
    return sqrt((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2)


# Path reconstruction
def reconstruct_path(goal):
    path = []
    current = goal
    while current:
        path.append(current.id)
        current = current.previous
    path.reverse()
    return path


# A* Search Algorithm
def a_star_search(start, goal, network, same_nodes, edge_weights):
    startNode = same_nodes[start]
    goalNode = same_nodes[goal]

    # start node
    startNode.gscore = 0
    startNode.fscore = heuristic(startNode, goalNode)

    # Priority queue with (fscore, Node), basically the higher the f_score, the more likely it is to be explored
    open_set = [(startNode.fscore, startNode)]
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        # If the goal is reached
        if current.id == goalNode.id:
            print("Goal reached")
            return reconstruct_path(goalNode)

        visited.add(current.id)

        # Explore neighbors
        for neighbor_id in network.neighbors(current.id):  # this method gets all the neighbors for a certain node
            if neighbor_id in visited:
                continue

            weight = edge_weights.get((current.id, neighbor_id), float('inf'))
            if weight == float('inf'):
                continue
            neighbor = same_nodes[neighbor_id]
            tentative_g_score = current.gscore + weight
            if tentative_g_score < neighbor.gscore:
                neighbor.gscore = tentative_g_score
                neighbor.fscore = tentative_g_score + heuristic(neighbor, goalNode)
                neighbor.previous = current
                heapq.heappush(open_set, (neighbor.fscore, neighbor))

                # Mark neighbors
                network.get_node(neighbor.id)["color"] = "orange"

        # Mark current node as processed
        network.get_node(current.id)["color"] = "blue"

    print("No path found")
    return None


# Graph setup
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
same_nodes = []

# Add nodes to the graph and initialize Node objects
for idx, name in enumerate(nodes):
    net.add_node(idx, label=str(name))
    n = Node(idx)
    same_nodes.append(n)

# Assign coordinates to nodes
coordinates = [
    (7, -1), (0, 0), (-2, -2), (1, 5), (11, -1),
    (3, -1), (10, 3), (15, 5), (13, 6), (5, 3)
]

for idx, (x, y) in enumerate(coordinates):
    same_nodes[idx].x = x
    same_nodes[idx].y = y

# Add edges with random weights
# selecting nodes and add up to three edges for every node
edge_weights = {}
sample = nodes[:]
for s in sample:
    modify = sample.copy()
    modify.remove(s)
    for _ in range(3):
        neighbor = modify[random.randint(0, len(modify) - 1)]
        weight = random.randint(1, 10)
        net.add_edge(s, neighbor, weight=weight)
        edge_weights[(s, neighbor)] = weight
        edge_weights[(neighbor, s)] = weight
        # adding it to the dictionary where we can easily look up the weights given to and from nodes

# supplementary nodes and edges, i added this later
extra_nodes = [
    Node(10, x=3, y=4),
    Node(11, x=4, y=6),
    Node(12, x=12, y=8)
]
for node in extra_nodes:
    same_nodes.append(node)
    net.add_node(node.id, label=str(node.id))

extra_edges = [
    (10, 9), (10, 3), (11, 3), (11, 9), (11, 10), (12, 8)
]

for src, dst in extra_edges:
    weight = random.randint(1, 10)
    net.add_edge(src, dst, weight=weight)
    edge_weights[(src, dst)] = weight
    edge_weights[(dst, src)] = weight

# return the path
path = a_star_search(1, 12, network=net, same_nodes=same_nodes, edge_weights=edge_weights)

# Highlight the path in green
if path:
    for node_id in path:
        net.get_node(node_id)["color"] = "green"
        print(node_id)

# Save and display the network, always use write_html
net.toggle_physics(False)
net.write_html("a_star_visualization.html")
#
# stream lit integration
st.title("Interactive A* Pathfinding Visualization")

start_node = st.selectbox("Select Start Node", options=range(len(same_nodes)))
goal_node = st.selectbox("Select Goal Node", options=range(len(same_nodes)))

if st.button("Run A* Algorithm"):
    path_1 = a_star_search(start_node, goal_node, net, same_nodes=same_nodes, edge_weights=edge_weights)
    print(start_node)
    print(goal_node)

    # edit ltr
    if path_1:
        st.success(f"Path found: {' -> '.join(map(str, path_1))}")
    else:
        st.success("this path")

path_html = net.generate_html()
st.components.v1.html(path_html, height=750)

# streamlit run pathfinding.py


# st.error("No path found.")
