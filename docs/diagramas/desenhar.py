"""Desenha os diagramas do relatorio (PNG) com matplotlib.

Executar: python docs/diagramas/desenhar.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon

PASTA = Path(__file__).resolve().parent
COR = "#1f4e79"
FUNDO = "#eaf1f8"
plt.rcParams["font.family"] = "Arial"


def tela(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def caixa(ax, x, y, w, h, texto, forma="ret", fs=9, cor=FUNDO, negrito=False):
    """x, y = centro."""
    if forma == "elipse":
        ax.add_patch(Ellipse((x, y), w, h, fc=cor, ec=COR, lw=1.2))
    elif forma == "losango":
        ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y), (x, y - h / 2)],
                             fc="#fff4d6", ec=COR, lw=1.2))
    else:
        estilo = "round,pad=0.3,rounding_size=2.5" if forma == "redondo" else "square,pad=0.2"
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=estilo, fc=cor, ec=COR, lw=1.2))
    ax.text(x, y, texto, ha="center", va="center", fontsize=fs, wrap=True,
            fontweight="bold" if negrito else "normal")


def seta(ax, a, b, texto="", tracejada=False, cabeca=True, fs=8):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>" if cabeca else "-", mutation_scale=11, color="#333",
                                 lw=1.1, linestyle="--" if tracejada else "-", shrinkA=0, shrinkB=0))
    if texto:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 1.2, texto, ha="center", va="bottom", fontsize=fs,
                color="#333", bbox=dict(fc="white", ec="none", pad=0.5))


def ator(ax, x, y, nome):
    ax.add_patch(Ellipse((x, y + 6), 3.2, 3.2, fc="white", ec="#333", lw=1.2))
    ax.plot([x, x], [y + 4.4, y - 1], color="#333", lw=1.2)
    ax.plot([x - 3, x + 3], [y + 2.5, y + 2.5], color="#333", lw=1.2)
    ax.plot([x, x - 2.5], [y - 1, y - 5], color="#333", lw=1.2)
    ax.plot([x, x + 2.5], [y - 1, y - 5], color="#333", lw=1.2)
    ax.text(x, y - 7.5, nome, ha="center", va="top", fontsize=9)


def tabela(ax, x, y_topo, w, titulo, linhas, fs=8.5, lh=3.6):
    """Caixa de classe/entidade: titulo + linhas. Retorna a altura."""
    h = lh * (len(linhas) + 1) + 1.5
    ax.add_patch(FancyBboxPatch((x - w / 2, y_topo - h), w, h, boxstyle="square,pad=0", fc="white", ec=COR, lw=1.2))
    ax.add_patch(FancyBboxPatch((x - w / 2, y_topo - lh - 0.8), w, lh + 0.8, boxstyle="square,pad=0",
                                fc=FUNDO, ec=COR, lw=1.2))
    ax.text(x, y_topo - (lh + 0.8) / 2, titulo, ha="center", va="center", fontsize=fs + 0.5, fontweight="bold")
    for i, t in enumerate(linhas):
        ax.text(x - w / 2 + 1.2, y_topo - lh - 0.8 - lh * (i + 0.6), t, ha="left", va="center", fontsize=fs)
    return h


def salvar(fig, nome):
    fig.savefig(PASTA / f"{nome}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def casos_de_uso():
    fig, ax = tela(10, 6.4)
    ax.add_patch(FancyBboxPatch((22, 2), 58, 60, boxstyle="square,pad=0", fc="none", ec="#333", lw=1.2))
    ax.text(51, 59.5, "Painel de Análise de Agenda", ha="center", fontsize=10, fontweight="bold")
    casos = ["Filtrar por estabelecimento,\nserviço e profissional", "Ver indicadores",
             "Ver mapa de calor dia x hora", "Ver horários vazios e de pico",
             "Ver faltas por dia e\nreceita por serviço", "Comparar estabelecimentos", "Carregar agenda (CSV)"]
    ys = [53, 46, 39, 32, 25, 17.5, 9]
    for t, y in zip(casos, ys):
        caixa(ax, 45, y, 30, 5.6, t, forma="elipse", fs=8)
    caixa(ax, 71, 9, 14, 5, "Validar colunas", forma="elipse", fs=8)
    seta(ax, (60, 9), (64, 9), "«inclui»", tracejada=True, fs=7)
    ator(ax, 10, 38, "Gestor do\nestabelecimento")
    ator(ax, 92, 16, "Consultor")
    for y in ys[:6]:
        seta(ax, (13, 38), (30, y), cabeca=False)
    for y in (17.5, 9):
        seta(ax, (89, 16), (60 if y == 17.5 else 56, y if y == 17.5 else 11.6), cabeca=False)
    salvar(fig, "casos-de-uso")


def classes():
    fig, ax = tela(10, 7)
    tabela(ax, 15, 68, 24, "Estabelecimento", ["- nome: texto"])
    tabela(ax, 15, 46, 24, "Serviço", ["- nome: texto", "- valor: real", "- duracao_min: inteiro"])
    tabela(ax, 50, 68, 24, "Profissional", ["- nome: texto"])
    tabela(ax, 50, 46, 24, "Atendimento", ["- data: data", "- hora: inteiro", "- status: texto", "- valor: real"])
    tabela(ax, 85, 68, 26, "App (View)", ["tela Streamlit", "filtros em cascata", "gráficos e tabelas"])
    tabela(ax, 85, 46, 26, "Controle (Controller)",
           ["+ preparar()", "+ opcoes() / filtrar()", "+ kpis()", "+ mapa_calor()", "+ ociosos() / picos()",
            "+ faltas_por_dia()", "+ ranking_servicos()", "+ por_estabelecimento()"])
    tabela(ax, 50, 18, 24, "Modelo (Model)", ["+ carregar(origem)", "+ COLUNAS"])
    seta(ax, (15, 59.3), (15, 46), "1 .. *")
    seta(ax, (27, 64.5), (38, 64.5), "1 .. *")
    seta(ax, (27, 38), (38, 38), "1 .. *")
    seta(ax, (50, 59.3), (50, 46), "1 .. *")
    seta(ax, (85, 52.1), (85, 46), "usa", tracejada=True)
    seta(ax, (72, 53), (62, 14.5), "usa", tracejada=True)
    seta(ax, (50, 18), (50, 26.5), "lê", tracejada=True)
    salvar(fig, "classes")


def atividades():
    fig, ax = tela(8, 10)
    x = 35
    passos = [(95, "Início", "redondo"), (86, "Ler CSV da agenda", "ret"), (75, "Colunas\nválidas?", "losango"),
              (64, "Preparar dados", "ret"), (55, "Escolher estabelecimento", "ret"),
              (46, "Listar serviços e profissionais\ndesse estabelecimento", "ret"), (37, "Aplicar filtros", "ret"),
              (26, "Há\natendimentos?", "losango"), (15, "Calcular indicadores,\nmapa de calor e rankings", "ret"),
              (6, "Exibir tela  ·  Fim", "redondo")]
    for y, t, f in passos:
        caixa(ax, x, y, 30 if f != "losango" else 22, 5 if f != "losango" else 9, t, forma=f, fs=8.5,
              cor="#d9e7d0" if f == "redondo" else FUNDO)
    for (y1, _, f1), (y2, _, f2) in zip(passos, passos[1:]):
        seta(ax, (x, y1 - (4.5 if f1 == "losango" else 2.7)), (x, y2 + (4.5 if f2 == "losango" else 2.7)),
             "sim" if f1 == "losango" else "")
    caixa(ax, 66, 75, 22, 5, "Mostrar colunas\nausentes  ·  Fim", forma="redondo", fs=8, cor="#f6d5d5")
    caixa(ax, 66, 26, 22, 5, "Mostrar aviso  ·  Fim", forma="redondo", fs=8, cor="#f6d5d5")
    seta(ax, (46, 75), (55, 75), "não")
    seta(ax, (46, 26), (55, 26), "não")
    salvar(fig, "atividades")


def entidade_relacionamento():
    fig, ax = tela(10, 6)
    tabela(ax, 16, 56, 26, "ESTABELECIMENTO", ["PK nome: texto"])
    tabela(ax, 56, 56, 26, "SERVICO", ["PK nome: texto", "FK estabelecimento", "valor: real", "duracao_min: inteiro"])
    tabela(ax, 16, 26, 26, "PROFISSIONAL", ["PK nome: texto", "FK estabelecimento"])
    tabela(ax, 84, 34, 26, "ATENDIMENTO", ["data: data", "hora: inteiro", "FK servico", "FK profissional",
                                           "status: texto", "valor: real"])
    seta(ax, (29, 52), (43, 52), "oferece  1 : N")
    seta(ax, (16, 47.3), (16, 26), "emprega  1 : N")
    seta(ax, (64, 36.5), (76, 34), "prestado em  1 : N")
    seta(ax, (29, 21), (71, 21), "realiza  1 : N")
    ax.text(36, 2, "No CSV, as quatro entidades ficam em uma única tabela (uma linha por agendamento).",
            ha="center", fontsize=8, style="italic")
    salvar(fig, "entidade-relacionamento")


def arquitetura():
    fig, ax = tela(11, 5.2)
    ax.add_patch(FancyBboxPatch((2, 8), 28, 38, boxstyle="round,pad=0.5,rounding_size=2", fc="#f7f7f7", ec="#999"))
    ax.text(16, 43, "Estabelecimento cliente\n(clínica, salão ou consultório)", ha="center", va="top", fontsize=8.5,
            fontweight="bold")
    caixa(ax, 16, 30, 20, 6, "Sistema de agenda")
    caixa(ax, 16, 15, 20, 6, "agenda.csv", cor="white")
    seta(ax, (16, 26.7), (16, 18.3), "exporta")
    ax.add_patch(FancyBboxPatch((38, 4), 46, 44, boxstyle="round,pad=0.5,rounding_size=2", fc="#f3f8fc", ec=COR))
    ax.text(61, 45.5, "Painel de Análise de Agenda (MVC)", ha="center", va="top", fontsize=9, fontweight="bold", color=COR)
    caixa(ax, 61, 35, 34, 7, "View · app.py\nStreamlit + Plotly")
    caixa(ax, 50, 15, 20, 7, "Model · modelo.py\nleitura e validação", fs=8)
    caixa(ax, 73, 15, 20, 7, "Controller · controle.py\nregras com pandas", fs=8)
    seta(ax, (55, 31.2), (50, 18.8), "usa")
    seta(ax, (67, 31.2), (73, 18.8), "usa")
    seta(ax, (26.5, 15), (39.7, 15), "lê")
    caixa(ax, 100, 35, 16, 7, "Gestor no\nnavegador", forma="redondo", cor="#d9e7d0")
    seta(ax, (91.5, 35), (78.5, 35), "usa")
    caixa(ax, 100, 12, 16, 7, "Consultoria\nimplanta e dá suporte", forma="redondo", cor="#fff4d6", fs=8)
    seta(ax, (91.5, 12), (85, 12), tracejada=True)
    salvar(fig, "arquitetura")


if __name__ == "__main__":
    casos_de_uso()
    classes()
    atividades()
    entidade_relacionamento()
    arquitetura()
    print("ok:", sorted(p.name for p in PASTA.glob("*.png")))
