from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from math import sqrt
from collections import Counter



iris = load_iris()
X = iris.data  # Features
y = iris.target  # Labels



# Split into training and testing sets (80/20 split)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def euclidean_distance(point1, point2):
    distance = 0.0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i])**2
    return sqrt(distance)


def get_k_neighbors(X_train, y_train, test_sample, k):
    distances = []
    for i in range(len(X_train)):
        dist = euclidean_distance(test_sample, X_train[i])
        distances.append((dist, y_train[i]))
    distances.sort(key=lambda x: x[0]) 
    neighbors = [distances[i][1] for i in range(k)]  # Extract labels of top k
    return neighbors

# Predict label using majority vote

def predict_classification(X_train, y_train, test_sample, k):
    neighbors = get_k_neighbors(X_train, y_train, test_sample, k)
    most_common = Counter(neighbors).most_common(1)
    return most_common[0][0]


def calculate_accuracy(X_train, y_train, X_test, y_test, k):
    correct = 0
    for i in range(len(X_test)):
        predicted = predict_classification(X_train, y_train, X_test[i], k)
        if predicted == y_test[i]:
            correct += 1
    return correct / len(y_test)


if __name__ == "__main__":
    print("Features shape:", X.shape)  
    print("Labels shape:", y.shape)   
    print("Number of classes:", len(set(y)))  

    for k in range(1, 11,2):
        accuracy = calculate_accuracy(X_train, y_train, X_test, y_test, k)
        print(f"k = {k}: Accuracy = {accuracy:.2f}")

