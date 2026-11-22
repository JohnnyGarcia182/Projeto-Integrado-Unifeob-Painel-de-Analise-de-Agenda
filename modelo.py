"""Model: leitura e validacao dos dados."""
from pathlib import Path

import pandas as pd

COLUNAS = ["data", "hora", "estabelecimento", "servico", "profissional", "status", "valor", "duracao_min"]
CSV_PADRAO = Path(__file__).resolve().parent / "data" / "agenda_exemplo.csv"


def carregar(origem=CSV_PADRAO) -> pd.DataFrame:
    df = pd.read_csv(origem)
    faltando = [c for c in COLUNAS if c not in df.columns]
    if faltando:
        raise ValueError("Colunas ausentes: " + ", ".join(faltando))
    df["data"] = pd.to_datetime(df["data"])
    return df
