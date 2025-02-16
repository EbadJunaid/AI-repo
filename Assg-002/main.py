import heapq

graph = {
    'a': [('b', 9), ('c', 4),('d',7)],
    'b': [('a', 9), ('e', 11)],
    'c': [('a', 4), ('e', 17),('f',12)],
    'd': [('a', 7),('f',14)],
    'e': [('b', 11),('c',17),('z',5)],
    'f': [('c', 12),('d',14),('z',9)],
    'z': [('e',5),('f',9)]
}


heuristics = {
    'a': 21, 'b': 14, 'c': 18,
    'd': 18, 'e': 5, 'f': 8,'z': 0
}



def a_star_search(graph, heuristics, start, goal):
    # Priority queue: (f(n), g(n), current_node, path_taken)
    priority_queue = []
    heapq.heappush(priority_queue, (heuristics[start], 0, start, [start]))
    
    # Track visited nodes and their lowest g(n) (cost so far)
    visited = {node: float('inf') for node in graph}
    visited[start] = 0
    
    while priority_queue:
        f_current, g_current, current_node, path = heapq.heappop(priority_queue)
        
        # Goal check
        if current_node == goal:
            return path, g_current
        
        # Skip if a better path to this node already exists
        if g_current > visited[current_node]:
            continue
        
        # Expand current node's neighbors
        for neighbor, edge_cost in graph[current_node]:
            new_g = g_current + edge_cost
            # Update if this path to neighbor is better
            if new_g < visited[neighbor]:
                visited[neighbor] = new_g
                new_f = new_g + heuristics[neighbor]
                new_path = path + [neighbor]
                heapq.heappush(priority_queue, (new_f, new_g, neighbor, new_path))
    
    return "No path found", -1


path, total_cost = a_star_search(graph, heuristics, 'a', 'z')

print(f"Path: {path}\nTotal Cost: {total_cost}")