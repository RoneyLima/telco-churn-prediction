from pathlib import Path

import joblib
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from telco_churn_prediction.modeling.preprocessing import load_and_preprocess_dataset
from telco_churn_prediction.modeling.train import save_pipeline, train_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def dataframe() -> pd.DataFrame:
    return load_and_preprocess_dataset(
        PROJECT_ROOT / "data" / "Telco_customer_churn.xlsx"
    )


def test_trains_pipeline_without_feature_engineering(dataframe: pd.DataFrame) -> None:
    result = train_model(dataframe)

    assert isinstance(result.pipeline, Pipeline)
    assert result.pipeline.steps[0][0] == "preprocessor"
    assert result.pipeline.steps[1][0] == "classifier"
    assert "avg_charge" not in dataframe.columns
    assert result.train_rows + result.test_rows == len(dataframe)


def test_persists_fitted_pipeline(
    dataframe: pd.DataFrame, tmp_path: Path
) -> None:
    sample_dataframe = dataframe.groupby("target", group_keys=False).head(100)
    result = train_model(sample_dataframe)
    destination = tmp_path / "nested" / "model.joblib"

    save_pipeline(result.pipeline, destination)
    loaded = joblib.load(destination)

    assert destination.exists()
    sample = dataframe.loc[
        dataframe.index[:1], list(result.pipeline.feature_names_in_)
    ]
    assert len(loaded.predict(sample)) == 1
