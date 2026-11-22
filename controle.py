"""Controller: regras de negocio (sem Streamlit e sem leitura de arquivos)."""
import pandas as pd

DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["dia"] = d["data"].dt.dayofweek.map(lambda i: DIAS[i])
    d["realizado"] = d["status"] == "Realizado"
    return d


def opcoes(d: pd.DataFrame, coluna: str, estabs=None, servs=None) -> list:
    """Opcoes de filtro em cascata: servicos e profissionais dependem do estabelecimento escolhido."""
    if estabs:
        d = d[d["estabelecimento"].isin(estabs)]
    if servs and coluna == "profissional":
        d = d[d["servico"].isin(servs)]
    return sorted(d[coluna].unique())


def filtrar(d: pd.DataFrame, estabs=None, servs=None, profs=None) -> pd.DataFrame:
    if estabs:
        d = d[d["estabelecimento"].isin(estabs)]
    if servs:
        d = d[d["servico"].isin(servs)]
    if profs:
        d = d[d["profissional"].isin(profs)]
    return d


def por_estabelecimento(d: pd.DataFrame) -> pd.DataFrame:
    g = d.groupby("estabelecimento").agg(
        agendados=("status", "size"), faltas=("status", lambda s: (s == "Falta").sum()), receita=("valor", "sum"))
    g["taxa_falta"] = g["faltas"] / g["agendados"]
    return g.sort_values("receita", ascending=False).reset_index()


def kpis(d: pd.DataFrame) -> dict:
    n = len(d)
    if n == 0:
        return {"agendados": 0, "realizados": 0, "faltas": 0, "taxa_falta": 0.0, "receita": 0.0}
    return {"agendados": n, "realizados": int(d["realizado"].sum()), "faltas": int((d["status"] == "Falta").sum()),
            "taxa_falta": (d["status"] == "Falta").mean(), "receita": float(d["valor"].sum())}


def mapa_calor(d: pd.DataFrame) -> pd.DataFrame:
    """Tabela dia da semana x hora com a media de atendimentos por dia de expediente."""
    dias_por_dia = d.groupby("dia")["data"].nunique()
    cont = d[d["realizado"]].groupby(["dia", "hora"]).size().unstack(fill_value=0)
    cont = cont.reindex([x for x in DIAS if x in cont.index])
    return cont.div(dias_por_dia.reindex(cont.index), axis=0).round(2)


def ociosos(mapa: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Os n horarios com menos atendimentos por dia: candidatos a promocao."""
    s = mapa.stack().rename("atendimentos_por_dia").reset_index()
    return s.sort_values("atendimentos_por_dia").head(n).reset_index(drop=True)


def picos(mapa: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    s = mapa.stack().rename("atendimentos_por_dia").reset_index()
    return s.sort_values("atendimentos_por_dia", ascending=False).head(n).reset_index(drop=True)


def faltas_por_dia(d: pd.DataFrame) -> pd.DataFrame:
    g = d.groupby("dia").agg(agendados=("status", "size"), faltas=("status", lambda s: (s == "Falta").sum()))
    g["taxa_falta"] = g["faltas"] / g["agendados"]
    return g.reindex([x for x in DIAS if x in g.index]).reset_index()


def ranking_servicos(d: pd.DataFrame) -> pd.DataFrame:
    r = d[d["realizado"]].groupby("servico").agg(atendimentos=("valor", "size"), receita=("valor", "sum"))
    return r.sort_values("receita", ascending=False).reset_index()
