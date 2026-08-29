import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler


def load_and_split_data(
    filepath, target_col, test_size=0.2, random_state=7, stratify=False
):
    """Carrega um CSV e o divide em conjuntos de treino e teste.

    Args:
        filepath (_type_): Caminho do arquivo
        target_col (_type_): Nome da coluna target
        test_size (float, optional): Tamanho do conjunto de teste. Defaults to 0.2.
        random_state (int, optional): Seed para reprodutibilidade. Defaults to 7.
        stratify (boolean, optional): Flag para realizar estratificação por target_col. Defaults to False.

    Returns:
        list: Uma lista contendo os conjuntos de treino e teste separados
    """

    df = pd.read_csv(filepath)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    to_stratify = y if stratify else None

    return train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=to_stratify
    )


def _create_custom_num_features(df):
    df_out = df.copy()
    df_out["avg_charge"] = (df_out.total_charges / df_out.tenure_months).fillna(0)
    df_out["diff_from_avg_charge"] = df_out.avg_charge - df_out.monthly_charges
    df_out["total_charges"] = np.log1p(df_out["total_charges"])
    return df_out


def create_preprocessing_pipeline(num_features, cat_features):
    custom_features_transformer = FunctionTransformer(
        _create_custom_num_features, validate=False
    )
    num_transformer = make_pipeline(custom_features_transformer, StandardScaler())
    cat_transformer = make_pipeline(
        OneHotEncoder(handle_unknown="infrequent_if_exist", drop="first")
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, num_features),
            ("cat", cat_transformer, cat_features),
        ]
    )

    return preprocessor


def assemble_full_pipeline(preprocessor, model):
    pipeline = make_pipeline(preprocessor, model)
    return pipeline
