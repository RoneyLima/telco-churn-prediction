import joblib
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    precision_recall_fscore_support,
)

from utils import log_training_run


def train_model(pipeline, X_train, y_train):
    pipeline.fit(X_train, y_train)

    return pipeline


def evaluate_model(model_name, pipeline, X_test, y_test, log_filepath):

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    average_precision = average_precision_score(y_test, y_proba)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="binary"
    )

    metrics_dict = {
        "average_precision": round(average_precision, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4),
        "f1": round(f1, 4),
    }

    print(f"=== {model_name} ===")
    for metric_name, metric_value in metrics_dict.items():
        print(f"{metric_name}: {metric_value}")

    log_training_run(model_name, metrics_dict, log_filepath=log_filepath)
    return y_pred


def save_artifact(pipeline, filename):
    joblib.dump(pipeline, filename)
    print(f"Artefato salvo com sucesso em {filename}")
