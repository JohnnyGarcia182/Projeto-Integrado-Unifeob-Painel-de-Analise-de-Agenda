import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import controle as ctl
import modelo
from gerar_csv import ESTABELECIMENTOS, gerar


def dados():
    df = gerar(dias=60)
    df["data"] = pd.to_datetime(df["data"])
    return ctl.preparar(df)


def test_kpis_consistentes():
    k = ctl.kpis(dados())
    assert k["realizados"] + k["faltas"] <= k["agendados"]
    assert 0 <= k["taxa_falta"] <= 1


def test_mapa_calor_e_ociosos():
    m = ctl.mapa_calor(dados())
    assert (m.values >= 0).all()
    o = ctl.ociosos(m, 3)
    assert len(o) == 3 and o["atendimentos_por_dia"].is_monotonic_increasing


def test_filtro_vazio():
    assert ctl.kpis(dados().iloc[0:0])["agendados"] == 0


def test_csv_invalido(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("data,hora\n2026-06-01,9\n")
    with pytest.raises(ValueError):
        modelo.carregar(p)


def test_servicos_e_profissionais_sao_proprios_de_cada_estabelecimento():
    d = dados()
    for estab, cfg in ESTABELECIMENTOS.items():
        assert set(ctl.opcoes(d, "servico", [estab])) <= set(cfg["servicos"])
        assert set(ctl.opcoes(d, "profissional", [estab])) <= set(cfg["profissionais"])
    # nenhum servico/profissional aparece em dois estabelecimentos
    por_estab = [set(ctl.opcoes(d, "servico", [e])) for e in ESTABELECIMENTOS]
    assert not (por_estab[0] & por_estab[1]) and not (por_estab[0] & por_estab[2])


def test_filtro_em_cascata():
    d = dados()
    f = ctl.filtrar(d, ["Salão Bela Vista"], ["Corte"], ["Ana"])
    assert not f.empty
    assert set(f["estabelecimento"]) == {"Salão Bela Vista"} and set(f["servico"]) == {"Corte"}
    assert set(ctl.opcoes(d, "profissional", ["Salão Bela Vista"], ["Corte"])) <= {"Ana", "Bruno", "Carla"}


def test_rnf01_carga_em_ate_10_segundos():
    import time
    t0 = time.perf_counter()
    d = ctl.preparar(modelo.carregar())
    m = ctl.mapa_calor(d)
    ctl.kpis(d), ctl.ociosos(m), ctl.picos(m), ctl.faltas_por_dia(d), ctl.ranking_servicos(d)
    assert time.perf_counter() - t0 < 10
