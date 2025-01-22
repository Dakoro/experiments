from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Candidate algorithms:
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

class AutoAlgorithmRecommender:
    def __init__(self, algorithms=None, scoring='accuracy'):
        """
        algorithms: list of tuples (algorithm_name, initialized_model)
        scoring: metric to optimize ('accuracy', 'f1', etc.)
        """
        if algorithms is None:
            self.algorithms = [
                ("K-Nearest Neighbors", KNeighborsClassifier(n_neighbors=5)),
                ("Support Vector Machine", SVC()),
                ("Random Forest", RandomForestClassifier())
            ]
        else:
            self.algorithms = algorithms

        self.scoring = scoring
        self.best_algorithm = None
        self.best_score = None

    def fit(self, X, y):
        """
        Performs train/test split and trains each algorithm
        to see which performs best on the hold-out set.
        """
        # Optional: cross-validation approach instead of a single split
        # But here's a simple train/test split:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        results = []
        for name, model in self.algorithms:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)  # or your chosen metric
            results.append((name, score))

        # Pick the best
        self.best_algorithm, self.best_score = max(results, key=lambda x: x[1])

        print("Results:")
        for name, score in results:
            print(f"{name}: {score:.4f}")
        print(f"\nBest algorithm is {self.best_algorithm} with score={self.best_score:.4f}")

    def predict(self, X):
        """
        Predict using the best algorithm identified.
        """
        if not self.best_algorithm:
            raise ValueError("No best algorithm found. Did you call fit first?")
        # Retrieve the actual model instance
        for name, model in self.algorithms:
            if name == self.best_algorithm:
                return model.predict(X)
        raise ValueError("Best algorithm not found in the list of candidates.")