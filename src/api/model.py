from pathlib import Path
from typing import Any

import joblib


class ChurnModel:
    """Mantém em memória o pipeline treinado durante a execução da API."""

    def __init__(self, model_path: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.model_path = model_path or project_root / "models" / "champion_logistic_regression_pipeline.joblib"
        self.model: Any | None = None

    @property
    def is_loaded(self) -> bool:
        """Indica se o pipeline foi carregado com sucesso."""
        return self.model is not None

    def load(self) -> None:
        """Load model once on API initialization"""
        self.model = joblib.load(self.model_path)
