from collections import deque

game_tree = {
    # Non-leaf nodes
    "A": ["B", "C"],
    "B": ["D", "E", "F"],
    "C": ["G", "H", "I"],
    "D": ["J", "K"],
    "E": ["L", "M"],
    "F": ["N", "O"],
    "G": ["P", "Q"],
    "H": ["R", "S"],
    "I": ["T", "U"],

    # Leaf nodes with values
    "J": 10, "K": 20, "L": 30, "M": 15,
    "N": 15, "O": 30, "P": 25, "Q": 35,
    "R": 5, "S": 10, "T": 35, "U": 40
}


def print_tree_levelwise(root):

    queue = deque([(root, 0)])
    current_level = -1
    
    while queue:
        node, level = queue.popleft()
        
        if level != current_level:
            print(f"\nLevel {level}: ", end="")
            current_level = level
            
        if isinstance(game_tree[node], list):
            print(f"{node}(*) ", end="")
            for child in game_tree[node]:
                queue.append((child, level+1))
        else:
            print(f"{node}[{game_tree[node]}] ", end="")


def alphabeta(node, alpha, beta, is_maximizing):
    
    global evaluated_nodes
    evaluated_nodes += 1
    
    # Base case: leaf node
    if not isinstance(game_tree[node], list):
        return game_tree[node], [node]
    
    if is_maximizing:
        max_val = -float('inf')
        best_path = []
        for child in game_tree[node]:
            child_val, child_path = alphabeta(child, alpha, beta, False)
            if child_val > max_val:
                max_val = child_val
                best_path = [node] + child_path
            alpha = max(alpha, max_val)
            if beta <= alpha:
                break  #Don't consider the remaining child's 
        return max_val, best_path
    else:
        min_val = float('inf')
        best_path = []
        for child in game_tree[node]:
            child_val, child_path = alphabeta(child, alpha, beta, True)
            if child_val < min_val:
                min_val = child_val
                best_path = [node] + child_path
            beta = min(beta, min_val)
            if beta <= alpha:
                break  # Don't consider the remaining child's
        return min_val, best_path



if __name__ == "__main__":
    evaluated_nodes = 0
    
    print("Game Tree Structure:")
    print_tree_levelwise("A")
    
    optimal_value, optimal_path = alphabeta("A", -float('inf'), float('inf'), True)
    
    print("\n\nResults:")
    print(f"Optimal value for root node A: {optimal_value}")
    print(f"Optimal path: {' → '.join(optimal_path)}")
    print(f"Total nodes evaluated: {evaluated_nodes}")