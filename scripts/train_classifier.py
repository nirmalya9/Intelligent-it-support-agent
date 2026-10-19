from app.ml.classifier import train_and_save, evaluate_holdout
if __name__ == "__main__":
    train_and_save()
    print(evaluate_holdout())
