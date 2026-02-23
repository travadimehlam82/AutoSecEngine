# ml_detector.py
# Trains a small RandomForest on synthetic data and provides a simple predict API.
import os, pickle, argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = 'rf_model.pkl'

class MLDetector:
    def __init__(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model = None

    def train(self):
        # create synthetic dataset: entropy, write_rate -> label (0 benign, 1 malicious)
        rng = np.random.RandomState(42)
        benign_entropy = rng.normal(3.0, 1.0, 500)
        benign_write = rng.poisson(1.0, 500)
        mal_entropy = rng.normal(7.8, 0.5, 200)
        mal_write = rng.poisson(12.0, 200)
        X = np.concatenate([np.stack([benign_entropy, benign_write], axis=1),
                            np.stack([mal_entropy, mal_write], axis=1)], axis=0)
        y = np.concatenate([np.zeros(500), np.ones(200)])
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(X, y)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(clf, f)
        self.model = clf
        print('[ml] model trained and saved.')

    def predict(self, feature_dict):
        if self.model is None:
            return 0, 0.0
        x = [[feature_dict.get('entropy', 0.0), feature_dict.get('write_rate', 0)]]
        prob = self.model.predict_proba(x)[0][1]
        pred = int(prob > 0.5)
        return pred, float(prob)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()
    if args.train:
        ml = MLDetector()
        ml.train()
