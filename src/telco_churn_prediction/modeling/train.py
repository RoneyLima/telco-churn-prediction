"""Training workflow and command-line entry point."""

import argparse
import json
import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from telco_churn_prediction import DEFAULT_MODEL_PATH
from telco_churn_prediction.modeling.preprocessing import (
    DEFAULT_CATEGORICAL_FEATURES,
    DEFAULT_INPUT_PATH,
    DEFAULT_NUMERIC_FEATURES,
    DEFAULT_OUTPUT_PATH,
    assemble_full_pipeline,
    create_preprocessing_pipeline,
    load_and_preprocess_dataset,
    save_preprocessed_dataset,
    validate_feature_columns,
)


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class TrainingConfig:
    """Parameters for reproducible model training."""

    target_column: str = "target"
    test_size: float = 0.2
    random_state: int = 7
    numeric_features: tuple[str, ...] = DEFAULT_NUMERIC_FEATURES
    categorical_features: tuple[str, ...] = DEFAULT_CATEGORICAL_FEATURES
    engineer_numeric_features: bool = False


@dataclass(frozen=True)
class TrainingResult:
    """Fitted pipeline, metrics, and split sizes."""

    pipeline: Pipeline
    classification_report: dict[str, Any]
    train_rows: int
    test_rows: int


def build_training_pipeline(
    config: TrainingConfig = TrainingConfig(),
    estimator: ClassifierMixin | None = None,
) -> Pipeline:
    """Build the pipeline configured for a training run."""
    classifier = (
        estimator
        if estimator is not None
        else LogisticRegression(
            class_weight="balanced",
            random_state=config.random_state,
        )
    )
    preprocessor = create_preprocessing_pipeline(
        config.numeric_features,
        config.categorical_features,
        engineer_numeric_features=config.engineer_numeric_features,
    )
    return assemble_full_pipeline(preprocessor, classifier)


def train_model(
    dataframe: pd.DataFrame,
    config: TrainingConfig = TrainingConfig(),
    estimator: ClassifierMixin | None = None,
) -> TrainingResult:
    """Split prepared data, fit a pipeline, and evaluate it."""
    if config.target_column not in dataframe.columns:
        raise ValueError(f"Target column not found: {config.target_column}")
    validate_feature_columns(
        dataframe,
        config.numeric_features,
        config.categorical_features,
    )

    feature_columns = config.numeric_features + config.categorical_features
    features = dataframe.loc[:, list(feature_columns)]
    target = dataframe[config.target_column]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config.test_size,
        random_state=config.random_state,
        stratify=target,
    )

    pipeline = fit_pipeline(build_training_pipeline(config, estimator), x_train, y_train)
    predictions = pipeline.predict(x_test)
    report = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0,
    )
    return TrainingResult(
        pipeline=pipeline,
        classification_report=report,
        train_rows=len(x_train),
        test_rows=len(x_test),
    )


def fit_pipeline(pipeline: Pipeline, x_train: Any, y_train: Any) -> Pipeline:
    """Fit and return a scikit-learn pipeline."""
    pipeline.fit(x_train, y_train)
    return pipeline


def evaluate_model(
    model_name: str,
    pipeline: Pipeline,
    x_test: Any,
    y_test: Any,
    log_filepath: str | Path | None = None,
) -> dict[str, float]:
    """Calculate the metrics used to compare project experiments."""
    predictions = pipeline.predict(x_test)
    probabilities = pipeline.predict_proba(x_test)[:, 1]
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average="binary",
        zero_division=0,
    )
    metrics = {
        "average_precision": round(
            float(average_precision_score(y_test, probabilities)), 4
        ),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "f1": round(float(f1), 4),
    }
    if log_filepath is not None:
        log_training_run(model_name, metrics, log_filepath)
    return metrics


def log_training_run(
    model_name: str,
    metrics: Mapping[str, float],
    log_filepath: str | Path,
) -> None:
    """Append one model experiment to a JSON Lines file."""
    destination = Path(log_filepath)
    destination.parent.mkdir(parents=True, exist_ok=True)
    run_log = {
        "timestamp": datetime.now(UTC).isoformat(),
        "model": model_name,
        "metrics": dict(metrics),
    }
    with destination.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(run_log, ensure_ascii=False) + "\n")


def save_pipeline(pipeline: Pipeline, output_path: str | Path) -> Path:
    """Persist a fitted pipeline and return its destination."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, destination)
    return destination


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for model training."""
    parser = argparse.ArgumentParser(
        description="Prepare the Telco dataset and train the baseline model."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--processed-output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--model-output", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=7)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Prepare data and train a model from the command line."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = build_parser().parse_args(argv)
    config = TrainingConfig(
        test_size=args.test_size,
        random_state=args.random_state,
    )

    dataframe = load_and_preprocess_dataset(args.input)
    save_preprocessed_dataset(dataframe, args.processed_output)
    result = train_model(dataframe, config)
    destination = save_pipeline(result.pipeline, args.model_output)
    LOGGER.info(
        "Training complete: train_rows=%d test_rows=%d accuracy=%.4f model=%s",
        result.train_rows,
        result.test_rows,
        result.classification_report["accuracy"],
        destination,
    )


if __name__ == "__main__":
    main()
