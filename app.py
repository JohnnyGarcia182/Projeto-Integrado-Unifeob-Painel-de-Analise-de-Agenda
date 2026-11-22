"""View: dashboard Streamlit. Executar: streamlit run app.py"""
import plotly.express as px
import streamlit as st

import controle as ctl
import modelo

st.set_page_config(page_title="Painel de Análise de Agenda", layout="wide")
st.title("Painel de Análise de Agenda")
st.subheader("Melhor dia e horário para atender")
st.caption("Painel para negócios de atendimento · "
           "dados fictícios para demonstração · PI Engenharia de Software · UNIFEOB")

arq = st.sidebar.file_uploader("Outro CSV (mesmas colunas)", type="csv")
try:
    dados = ctl.preparar(modelo.carregar(arq) if arq else modelo.carregar())
except ValueError as e:
    st.error(str(e))
    st.stop()

# Filtros em cascata: Estabelecimento -> Serviço -> Profissional
st.sidebar.header("Filtros")
estabs = st.sidebar.multiselect("Estabelecimento", ctl.opcoes(dados, "estabelecimento"))
servs = st.sidebar.multiselect("Serviço", ctl.opcoes(dados, "servico", estabs))
profs = st.sidebar.multiselect("Profissional", ctl.opcoes(dados, "profissional", estabs, servs))
d = ctl.filtrar(dados, estabs, servs, profs)
if d.empty:
    st.warning("Nenhum atendimento para os filtros.")
    st.stop()

k = ctl.kpis(d)
c = st.columns(4)
c[0].metric("Agendamentos", k["agendados"])
c[1].metric("Realizados", k["realizados"])
c[2].metric("Taxa de faltas", f"{k['taxa_falta']:.1%}")
c[3].metric("Receita", f"R$ {k['receita']:,.0f}".replace(",", "."))

if d["estabelecimento"].nunique() > 1:
    st.subheader("Comparação entre estabelecimentos")
    st.dataframe(ctl.por_estabelecimento(d).style.format({"receita": "R$ {:,.0f}", "taxa_falta": "{:.1%}"}),
                 hide_index=True)

mapa = ctl.mapa_calor(d)
st.subheader("Movimento por dia e hora (atendimentos por dia)")
st.plotly_chart(px.imshow(mapa, aspect="auto", color_continuous_scale="Blues",
                          labels={"x": "Hora", "y": "Dia", "color": "Atend./dia"}), width="stretch")

esq, dir_ = st.columns(2)
esq.subheader("Horários mais vazios (ideais para promoção)")
esq.dataframe(ctl.ociosos(mapa), hide_index=True)
dir_.subheader("Horários de pico")
dir_.dataframe(ctl.picos(mapa), hide_index=True)

esq2, dir2 = st.columns(2)
esq2.subheader("Taxa de faltas por dia")
esq2.plotly_chart(px.bar(ctl.faltas_por_dia(d), x="dia", y="taxa_falta"), width="stretch")
dir2.subheader("Serviços por receita")
dir2.plotly_chart(px.bar(ctl.ranking_servicos(d), x="servico", y="receita"), width="stretch")
