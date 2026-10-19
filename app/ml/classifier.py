from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "tickets.csv"
MODEL_PATH = ROOT / "artifacts" / "ticket_classifier.joblib"


def make_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True, strip_accents="unicode")),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])


def train_and_save():
    df = pd.read_csv(DATA_PATH)
    text = (df["title"].fillna("") + ". " + df["description"].fillna("")).tolist()
    model = make_model().fit(text, df["category"].tolist())
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


class TicketClassifier:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

    def load_or_train(self):
        if self.model is None:
            self.model = train_and_save()
        return self

    def predict(self, title: str, description: str) -> dict:
        self.load_or_train()
        probabilities = self.model.predict_proba([f"{title}. {description}"])[0]
        classes = self.model.classes_
        idx = int(probabilities.argmax())
        return {"category": str(classes[idx]), "confidence": float(probabilities[idx]),
                "probabilities": {str(c): float(p) for c, p in zip(classes, probabilities)}}


def evaluate_holdout():
    df = pd.read_csv(DATA_PATH)
    x = df["title"].fillna("") + ". " + df["description"].fillna("")
    y = df["category"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.25, random_state=42, stratify=y)
    model = make_model().fit(x_train, y_train)
    pred = model.predict(x_test)
    return {"accuracy": float(accuracy_score(y_test, pred)), "macro_f1": float(f1_score(y_test, pred, average="macro")),
            "report": classification_report(y_test, pred, zero_division=0)}
