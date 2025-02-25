
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter


data = np.array([
    [2, 5, 0],
    [3, 6, 0],
    [5, 6, 1],
    [6, 5, 1],
    [8, 7, 1],
    [1, 4, 0],
    [4, 6, 1],
    [7, 8, 1],
    [2, 6, 0],
    [5, 5, 1]
])

X = data[:, :-1] # the first : saying pick all the rows and then :-1 is saying that pick all the columns except the last one 
y = data[:, -1]  # Similarly : is saying pick all the rows and -1 is saying just pick the last column 

# X is an array which contains only Features (Study Hours, Sleep Hours)
# Y is an array which contains only labels like 0 and 1
 


def entropy(y):
    counts = Counter(y)
    total = len(y)
    entropy_value = 0.0
    for label in counts:
        prob = counts[label] / total
        entropy_value -= prob * np.log2(prob)
    return entropy_value


def best_split(X, y):
    best_feature = None
    best_threshold = None
    lowest_entropy = float('inf')
    
    for feature_idx in range(X.shape[1]):
        feature_values = np.unique(X[:, feature_idx])
        for threshold in feature_values:
            left_mask = X[:, feature_idx] <= threshold
            right_mask = ~left_mask
            
            y_left = y[left_mask]
            y_right = y[right_mask]
            
            if len(y_left) == 0 or len(y_right) == 0:
                continue
                
            weighted_entropy = (len(y_left)/len(y)) * entropy(y_left) + \
                               (len(y_right)/len(y)) * entropy(y_right)
                               
            if weighted_entropy < lowest_entropy:
                lowest_entropy = weighted_entropy
                best_feature = feature_idx
                best_threshold = threshold
                
    return (best_feature, best_threshold)


class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = {}
        
    def fit(self, X, y, depth=0):
        # Base cases
        if len(np.unique(y)) == 1:
            return {'value': y[0]}
            
        if depth >= self.max_depth:
            return {'value': Counter(y).most_common(1)[0][0]}
            
        # Find best split
        feature, threshold = best_split(X, y)
        if feature is None:
            return {'value': Counter(y).most_common(1)[0][0]}
            
        # Recursive splitting
        left_mask = X[:, feature] <= threshold
        right_mask = ~left_mask
        
        node = {
            'feature': feature,
            'threshold': threshold,
            'left': self.fit(X[left_mask], y[left_mask], depth+1),
            'right': self.fit(X[right_mask], y[right_mask], depth+1)
        }
        
        return node
    
    def train(self, X, y):
        self.tree = self.fit(X, y)


def predict_sample(tree, x):
    if 'value' in tree:
        return tree['value']
    feature_val = x[tree['feature']]
    if feature_val <= tree['threshold']:
        return predict_sample(tree['left'], x)
    else:
        return predict_sample(tree['right'], x)

def predict(model, X):
    return np.array([predict_sample(model.tree, x) for x in X])






    

def draw_tree(node, graph=None, parent=None, node_id=0, edge_label=''):
    if graph is None:
        graph = nx.DiGraph()
    
    current_id = node_id
    if 'value' in node:
        label = f'Class: {node["value"]}'
    else:
        label = f'Feature {node["feature"]} <= {node["threshold"]}'
    
    graph.add_node(current_id, label=label)
    
    if parent is not None:
        graph.add_edge(parent, current_id, label=edge_label)
    
    if 'left' in node:
        next_id = node_id + 1
        graph, next_id = draw_tree(node['left'], graph, current_id, next_id, 'Yes')
        graph, next_id = draw_tree(node['right'], graph, current_id, next_id, 'No')
    
    return graph, node_id + 1

def plot_tree(tree):
    graph, _ = draw_tree(tree)
    pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog='dot')
    labels = nx.get_node_attributes(graph, 'label')
    edge_labels = nx.get_edge_attributes(graph, 'label')
    
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000,
            node_color='lightblue', arrows=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()

if __name__ == "__main__":
    # Train model
    dt = DecisionTree(max_depth=3)
    dt.train(X, y)
    
    print("\n the value of the tree is below \n ",dt.tree)

    
    # Test predictions
    #y_pred = predict(dt, X)
    check = np.array([[4, 6]])
    y_pred = predict(dt, check)
    print("Predictions:", y_pred)
    print("Actual labels:", y)
    print("Accuracy:", np.sum(y_pred == y) / len(y))
    
    # Visualize tree
    plot_tree(dt.tree)
