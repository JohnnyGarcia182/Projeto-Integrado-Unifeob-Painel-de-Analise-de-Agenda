"""Gera data/agenda_exemplo.csv com dados FICTICIOS (semente fixa).

Cada estabelecimento tem seus proprios servicos (valor, duracao) e profissionais.
"""
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ESTABELECIMENTOS = {
    "Clínica Vida Plena": {
        "servicos": {"Consulta": (180, 40), "Retorno": (0, 20), "Exame de rotina": (120, 30),
                     "Vacinação": (90, 15)},
        "profissionais": ["Dra. Helena", "Dr. Marcos", "Enf. Paula"],
        "peso_dia": [1.3, 1.2, 1.1, 1.1, 1.0, 0.5],  # seg a sab
    },
    "Salão Bela Vista": {
        "servicos": {"Corte": (60, 45), "Coloração": (180, 90), "Manicure": (45, 50), "Escova": (70, 40)},
        "profissionais": ["Ana", "Bruno", "Carla"],
        "peso_dia": [0.5, 0.7, 0.8, 1.0, 1.4, 1.8],
    },
    "Consultório Sorriso": {
        "servicos": {"Avaliação": (100, 30), "Limpeza": (150, 60), "Restauração": (250, 60),
                     "Clareamento": (600, 90)},
        "profissionais": ["Dr. Rafael", "Dra. Beatriz"],
        "peso_dia": [1.2, 1.1, 1.0, 1.2, 1.0, 0.6],
    },
}
PESO_HORA = {8: 0.8, 9: 1.2, 10: 1.5, 11: 1.3, 12: 0.4, 13: 0.6, 14: 1.0, 15: 1.1, 16: 1.2, 17: 0.9}
COLUNAS = ["data", "hora", "estabelecimento", "servico", "profissional", "status", "valor", "duracao_min"]


def gerar(seed=2026, inicio=date(2026, 6, 1), dias=150):
    rng = random.Random(seed)
    linhas = []
    for i in range(dias):
        d = inicio + timedelta(days=i)
        if d.weekday() == 6:  # domingo fechado
            continue
        for estab, cfg in ESTABELECIMENTOS.items():
            for h, ph in PESO_HORA.items():
                for prof in cfg["profissionais"]:
                    if rng.random() < 0.55 * cfg["peso_dia"][d.weekday()] * ph:
                        serv = rng.choice(list(cfg["servicos"]))
                        valor, dur = cfg["servicos"][serv]
                        p_falta = 0.22 if (d.weekday() == 0 and h < 10) else 0.08
                        r = rng.random()
                        status = "Falta" if r < p_falta else "Cancelado" if r < p_falta + 0.05 else "Realizado"
                        linhas.append([d.isoformat(), h, estab, serv, prof, status,
                                       valor if status == "Realizado" else 0, dur])
    return pd.DataFrame(linhas, columns=COLUNAS)


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent / "data" / "agenda_exemplo.csv"
    destino.parent.mkdir(exist_ok=True)
    df = gerar()
    df.to_csv(destino, index=False)
    print(df.shape)
