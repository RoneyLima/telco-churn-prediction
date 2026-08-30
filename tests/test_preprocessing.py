import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from telco_churn_prediction.data.preprocessing import (
    DEFAULT_FEATURE_CONFIG,
    EDA_COLUMNS_TO_DROP,
    FeatureConfig,
    build_column_transformer,
    preprocess_telco_dataset,
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
    config = FeatureConfig.from_sequences(["amount"], ["category"])

    transformer = build_column_transformer(config)

    assert isinstance(transformer, ColumnTransformer)
    assert transformer.transformers[0][2] == ["amount"]
    assert transformer.transformers[1][2] == ["category"]


def test_rejects_missing_configured_features() -> None:
    with pytest.raises(ValueError, match="not found"):
        DEFAULT_FEATURE_CONFIG.validate(["tenure_months"])
