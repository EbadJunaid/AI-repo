import random
import copy
from collections import deque

class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.children = []
        self.selected_child = None

def generate_binary_tree(depth, current_depth=0):
    node = TreeNode()
    if current_depth == depth:
        node.value = random.randint(1, 20)
    else:
        node.children = [
            generate_binary_tree(depth, current_depth + 1),
            generate_binary_tree(depth, current_depth + 1)
        ]
    return node


def print_tree_level_order(root):
    if not root:
        return

    queue = deque([root]) 

    while queue:
        level_size = len(queue) 
        for _ in range(level_size): 
            node = queue.popleft()
            value_str = str(node.value) if node.value is not None else "[None]"
            print(value_str, end=" ")

            if node.children:  
                for child in node.children:
                    queue.append(child)
        print()





def get_path(node):
    path = []
    current = node
    while current.children:
        path.append(current.value)
        current = current.selected_child
    path.append(current.value)
    return path

# Task 1: Minimax Implementation

minimax_iterations = 0

def minimax(node, is_maximizing):
    global minimax_iterations
    minimax_iterations += 1

    if not node.children:
        return node.value

    if is_maximizing:
        max_val = -float('inf')
        for child in node.children:
            val = minimax(child, False)
            if val > max_val:
                max_val = val
                node.selected_child = child
        node.value = max_val
        return max_val
    else:
        min_val = float('inf')
        for child in node.children:
            val = minimax(child, True)
            if val < min_val:
                min_val = val
                node.selected_child = child
        node.value = min_val
        return min_val



# Task 2: Alpha-Beta Pruning Implementation
alphabeta_iterations = 0

def alphabeta(node, alpha, beta, is_maximizing):
    global alphabeta_iterations
    alphabeta_iterations += 1

    if not node.children:
        return node.value

    if is_maximizing:
        max_val = -float('inf')
        for child in node.children:
            val = alphabeta(child, alpha, beta, False)
            if val > max_val:
                max_val = val
                node.selected_child = child
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        node.value = max_val
        return max_val
    else:
        min_val = float('inf')
        for child in node.children:
            val = alphabeta(child, alpha, beta, True)
            if val < min_val:
                min_val = val
                node.selected_child = child
            beta = min(beta, val)
            if beta <= alpha:
                break
        node.value = min_val
        return min_val

# Main execution
original_tree = generate_binary_tree(3)
print("\nInitially the tree is \n")
print("-----------------------------------------")
print_tree_level_order(original_tree)
print("-----------------------------------------")


tree_task1 = copy.deepcopy(original_tree)
minimax_iterations = 0
optimal_value = minimax(tree_task1, True)
path_task1 = get_path(tree_task1)


tree_task2 = copy.deepcopy(original_tree)
alphabeta_iterations = 0
optimal_value_ab = alphabeta(tree_task2, -float('inf'), float('inf'), True)
path_task2 = get_path(tree_task2)

pruned_nodes = minimax_iterations - alphabeta_iterations


print("Task 1 - Minimax Results:")
print(f"Optimal Value: {optimal_value}")
print(f"Path: {path_task1}")
print(f"Nodes Evaluated: {minimax_iterations}\n")


print("Task 2 - Alpha-Beta Results:")
print(f"Optimal Value: {optimal_value_ab}")
print(f"Path: {path_task2}")
print(f"Nodes Evaluated: {alphabeta_iterations}")
print(f"Pruned Nodes: {pruned_nodes}")


print("\nNow the tree becomes \n")
print("-----------------------------------------")
print_tree_level_order(tree_task1)
print("-----------------------------------------")