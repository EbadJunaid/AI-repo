import numpy as np
from collections import Counter


X = np.array([
    [0, 2, 1],  # Young, High Income, Prior Purchase=Yes
    [1, 1, 0],  # Middle-aged, Medium Income, Prior Purchase=No
    [2, 2, 1],  # Senior, High Income, Prior Purchase=Yes
    [0, 1, 0],  # Young, Medium Income, Prior Purchase=No
    [1, 2, 1],  # Middle-aged, High Income, Prior Purchase=Yes
])

y = np.array([1, 0, 1, 0, 1])  


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
        if len(np.unique(y)) == 1:
            return {'value': y[0]}
            
        if depth >= self.max_depth:
            return {'value': Counter(y).most_common(1)[0][0]}
            
        feature, threshold = best_split(X, y)
        if feature is None:
            return {'value': Counter(y).most_common(1)[0][0]}
            
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


if __name__ == "__main__":
    dt = DecisionTree(max_depth=3)
    dt.train(X, y)
    

    test_sample = np.array([[0, 2, 0]])
    prediction = predict(dt, test_sample)
    print("Prediction:", prediction)  