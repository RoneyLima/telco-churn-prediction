import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from telco_churn_prediction.modeling.preprocessing import (
    DEFAULT_CATEGORICAL_FEATURES,
    DEFAULT_NUMERIC_FEATURES,
    EDA_COLUMNS_TO_DROP,
    create_preprocessing_pipeline,
    preprocess_telco_dataset,
    validate_feature_columns,
)


def test_applies_only_eda_cleaning_rules() -> None:
    row = {column: "unused" for column in EDA_COLUMNS_TO_DROP}
    row.update(
        {
            "City": "Sao Paulo",
            "Zip Code": 12345,
            "Lat Long": "0, 0",
            "Latitude": 0.0,
            "Longitude": 0.0,
            "Total Charges": " ",
            "Churn Value": 1,
            "Tenure Months": 0,
        }
    )
    original = pd.DataFrame([row])

    result = preprocess_telco_dataset(original)

    assert result.columns.tolist() == ["total_charges", "target", "tenure_months"]
    assert result.loc[0, "total_charges"] == 0
    assert "CustomerID" in original.columns


def test_builds_column_transformer_from_explicit_config() -> None:
    transformer = create_preprocessing_pipeline(
        ["amount"],
        ["category"],
        engineer_numeric_features=False,
    )

    assert isinstance(transformer, ColumnTransformer)
    assert transformer.transformers[0][2] == ["amount"]
    assert transformer.transformers[1][2] == ["category"]


def test_rejects_missing_configured_features() -> None:
    with pytest.raises(ValueError, match="not found"):
        validate_feature_columns(
            pd.DataFrame(columns=["tenure_months"]),
            DEFAULT_NUMERIC_FEATURES,
            DEFAULT_CATEGORICAL_FEATURES,
        )
