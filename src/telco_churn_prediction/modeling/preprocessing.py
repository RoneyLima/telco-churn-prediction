"""Carregamento, preparação dos dados e montagem do pipeline."""

import argparse
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from telco_churn_prediction import PROJECT_ROOT


DEFAULT_INPUT_PATH = PROJECT_ROOT / "data" / "Telco_customer_churn.xlsx"
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "telco_customer_churn_preprocessed.csv"
)

EDA_COLUMNS_TO_DROP = (
    "CustomerID",
    "Count",
    "Country",
    "State",
    "Churn Label",
    "Churn Score",
    "Churn Reason",
)
GEOGRAPHIC_COLUMNS_TO_DROP = (
    "city",
    "zip_code",
    "lat_long",
    "latitude",
    "longitude",
)
DEFAULT_NUMERIC_FEATURES = (
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "cltv",
)
DEFAULT_CATEGORICAL_FEATURES = (
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "phone_service",
    "multiple_lines",
    "internet_service",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
    "contract",
    "paperless_billing",
    "payment_method",
)


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Carrega um conjunto de dados CSV ou Excel.

    Args:
        path: Caminho do arquivo que será carregado.

    Returns:
        DataFrame com os dados do arquivo.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o formato não for CSV ou Excel.
    """
    dataset_path = Path(path)
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    if dataset_path.suffix.lower() == ".csv":
        return pd.read_csv(dataset_path)
    if dataset_path.suffix.lower() in {".xls", ".xlsx"}:
        return pd.read_excel(dataset_path)

    raise ValueError(
        f"Unsupported dataset format '{dataset_path.suffix}'. Use CSV or Excel."
    )


def normalize_column_name(column: str) -> str:
    """Converte um nome de coluna para letras minúsculas e snake case.

    Args:
        column: Nome original da coluna.

    Returns:
        Nome normalizado. Por exemplo, ``Total Charges`` vira
        ``total_charges``.
    """
    return "_".join(column.lower().split())


def preprocess_telco_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras de limpeza definidas na análise exploratória.

    A função remove colunas sem uso na modelagem, converte ``Total Charges``
    para número, renomeia o alvo para ``target`` e normaliza os nomes das
    colunas. O DataFrame recebido não é modificado.

    Args:
        dataframe: Dados originais da base Telco Customer Churn.

    Returns:
        Cópia limpa e pronta para ser usada na modelagem.

    Raises:
        ValueError: Se alguma coluna obrigatória não estiver presente.
    """
    required_columns = set(EDA_COLUMNS_TO_DROP) | {
        "City",
        "Zip Code",
        "Lat Long",
        "Latitude",
        "Longitude",
        "Total Charges",
        "Churn Value",
    }
    missing_columns = sorted(required_columns - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Required raw dataset columns not found: {missing_columns}")

    processed = dataframe.copy()
    processed = processed.drop(columns=list(EDA_COLUMNS_TO_DROP))
    processed["Total Charges"] = pd.to_numeric(
        processed["Total Charges"], errors="coerce"
    ).fillna(0)
    processed = processed.rename(columns={"Churn Value": "target"})
    processed.columns = [normalize_column_name(column) for column in processed]
    return processed.drop(columns=list(GEOGRAPHIC_COLUMNS_TO_DROP))


def load_and_preprocess_dataset(input_path: str | Path) -> pd.DataFrame:
    """Carrega a base original e aplica as regras de limpeza.

    Args:
        input_path: Caminho do arquivo CSV ou Excel original.

    Returns:
        DataFrame limpo e pronto para modelagem.
    """
    dataframe = load_dataset(input_path)
    return preprocess_telco_dataset(dataframe)


def save_preprocessed_dataset(
    dataframe: pd.DataFrame, output_path: str | Path
) -> Path:
    """Salva o conjunto de dados preparado em um arquivo CSV.

    Args:
        dataframe: Dados que serão salvos.
        output_path: Caminho do arquivo CSV de destino.

    Returns:
        Caminho em que o arquivo foi salvo.
    """
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(destination, index=False)
    return destination


def load_and_split_data(
    filepath: str | Path,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 7,
    stratify: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Carrega os dados e os divide em conjuntos de treino e teste.

    Args:
        filepath: Caminho do arquivo CSV ou Excel preparado.
        target_column: Nome da coluna que contém o alvo da predição.
        test_size: Proporção dos dados destinada ao teste. O padrão é ``0.2``.
        random_state: Semente utilizada na divisão. O padrão é ``7``.
        stratify: Se verdadeiro, mantém a proporção das classes do alvo. O
            padrão é ``False``.

    Returns:
        Tupla com ``X_train``, ``X_test``, ``y_train`` e ``y_test``, nessa
        ordem.

    Raises:
        ValueError: Se a coluna alvo não existir.
    """
    dataframe = load_dataset(filepath)
    if target_column not in dataframe.columns:
        raise ValueError(f"Target column not found: {target_column}")

    features = dataframe.drop(columns=[target_column])
    target = dataframe[target_column]
    stratification = target if stratify else None
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=stratification,
    )
    return x_train, x_test, y_train, y_test


def validate_feature_columns(
    dataframe: pd.DataFrame,
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
) -> None:
    """Verifica se todas as features configuradas existem nos dados.

    Args:
        dataframe: Dados que serão usados pelo pipeline.
        numeric_features: Nomes das features numéricas.
        categorical_features: Nomes das features categóricas.

    Returns:
        ``None``. A função apenas valida as colunas.

    Raises:
        ValueError: Se uma feature estiver ausente ou repetida.
    """
    configured_features = list(numeric_features) + list(categorical_features)
    if len(configured_features) != len(set(configured_features)):
        raise ValueError("Feature columns must be unique.")

    missing = sorted(set(configured_features) - set(dataframe.columns))
    if missing:
        raise ValueError(f"Configured features not found in dataset: {missing}")


def _create_custom_num_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Cria as features numéricas utilizadas pelo modelo champion.

    Calcula ``avg_charge`` e ``diff_from_avg_charge`` e aplica uma
    transformação logarítmica em ``total_charges``.

    Args:
        dataframe: Dados numéricos contendo ``total_charges``,
            ``tenure_months`` e ``monthly_charges``.

    Returns:
        Cópia do DataFrame com as novas features numéricas.
    """
    transformed = dataframe.copy()
    average_charge = transformed["total_charges"].div(
        transformed["tenure_months"].replace(0, np.nan)
    )
    transformed["avg_charge"] = average_charge.fillna(0)
    transformed["diff_from_avg_charge"] = (
        transformed["avg_charge"] - transformed["monthly_charges"]
    )
    transformed["total_charges"] = np.log1p(transformed["total_charges"])
    return transformed


def create_preprocessing_pipeline(
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
    engineer_numeric_features: bool = True,
) -> ColumnTransformer:
    """Cria o pré-processamento das features numéricas e categóricas.

    As features numéricas são padronizadas com ``StandardScaler``. Quando
    solicitado, a engenharia de features do modelo champion é executada antes
    da padronização. As features categóricas usam ``OneHotEncoder``.

    Args:
        numeric_features: Nomes das features numéricas.
        categorical_features: Nomes das features categóricas.
        engineer_numeric_features: Se verdadeiro, cria as features numéricas
            adicionais usadas pelo modelo champion. O padrão é ``True``.

    Returns:
        ``ColumnTransformer`` configurado para o pré-processamento.
    """
    if engineer_numeric_features:
        numeric_transformer = make_pipeline(
            FunctionTransformer(_create_custom_num_features, validate=False),
            StandardScaler(),
        )
    else:
        numeric_transformer = make_pipeline(StandardScaler())

    categorical_transformer = make_pipeline(
        OneHotEncoder(handle_unknown="infrequent_if_exist", drop="first")
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, list(numeric_features)),
            ("categorical", categorical_transformer, list(categorical_features)),
        ]
    )


def assemble_full_pipeline(
    preprocessor: ColumnTransformer,
    model: ClassifierMixin,
) -> Pipeline:
    """Combina o pré-processamento e o modelo em um único pipeline.

    Args:
        preprocessor: Transformações aplicadas antes da predição.
        model: Classificador compatível com o scikit-learn, como
            ``LogisticRegression`` ou ``RandomForestClassifier``.

    Returns:
        Pipeline pronto para treinamento e predição.
    """
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model),
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser do comando de preparação dos dados.

    Returns:
        Parser com os argumentos ``--input`` e ``--output``.
    """
    parser = argparse.ArgumentParser(description="Prepare the Telco churn dataset.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Executa a preparação dos dados pela linha de comando.

    Args:
        argv: Argumentos opcionais da linha de comando.

    Returns:
        ``None``.
    """
    args = build_parser().parse_args(argv)
    dataframe = load_and_preprocess_dataset(args.input)
    destination = save_preprocessed_dataset(dataframe, args.output)
    print(f"Prepared {len(dataframe)} rows in {destination}")


if __name__ == "__main__":
    main()
