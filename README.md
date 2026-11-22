# Painel de Análise de Agenda

Painel em Python para analisar a agenda de negócios de atendimento (clínicas, salões e consultórios): movimento por dia e hora, horários vazios e de pico, faltas e receita.
Projeto Integrado – Engenharia de Software – UNIFEOB (4º trimestre 2026).

## Funcionalidades
- RF01 Ler a agenda em CSV, validando as colunas
- RF02 Exibir agendamentos, atendimentos realizados, taxa de faltas e receita
- RF03 Filtrar em cascata por estabelecimento, serviço e profissional
- RF04 Exibir mapa de calor de dia da semana × hora
- RF05 Listar os horários mais vazios e os de pico
- RF06 Exibir taxa de faltas por dia e receita por serviço
- RF07 Comparar estabelecimentos
- RNF01 Carrega em até 10 segundos | RNF02 Funciona localmente, sem servidor | RNF03 Dados fictícios

## Como rodar
```bash
pip install -r requirements.txt
streamlit run app.py
```
## Testes
```bash
pytest
```
## Estrutura
`modelo.py` leitura e validação (Model) · `controle.py` regras de negócio (Controller) · `app.py` interface (View) · `gerar_csv.py` dados fictícios · `docs/diagramas/` diagramas UML e de arquitetura
