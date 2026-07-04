# Vaqueiro - retomada (continuar amanha)

Capstone Kaggle "Vibe Coding". HOJE=4/jul; prazo 6/jul. Agente que responde lendo o `.ai-context/` de um
projeto em vez de re-escanear o codigo. Trilha: Freestyle.

**Prazo:** 6 jul 2026, 23:59 PT (= 7 jul, 07:59 Lisboa). Submeter na pagina do
capstone: New Writeup -> Save -> Submit.

## Status
| # | Atividade | Status |
|---|-----------|--------|
| 1 | Scaffold ADK | feito |
| 2 | MVP + .ai-context real do NG-M3 | falta (rodar) |
| 3 | MCP server + eval | codigo pronto; falta rodar |
| 3b | Multiagente (Answerer->Evaluator) | codigo pronto (`vaqueiro_reviewed/`) |
| 4 | Metricas + repo limpo | script pronto; falta numeros reais |
| 5 | Writeup + video | draft+roteiro prontos; preencher + gravar |
| 6 | Submeter | pendente |

Restante estimado: ~8-12h focadas.

## Proximos passos (nesta ordem)
1. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. `cp vaqueiro/.env.example vaqueiro/.env` e colar a chave do Google AI Studio.
3. `adk web` -> selecionar "vaqueiro" -> testar 3-4 perguntas.
4. Apontar `AI_CONTEXT_ROOT` para o `.ai-context/` real do NG-M3.
5. `python scripts/token_metrics.py` e `python -m eval.run_eval` -> anotar numeros.
6. Preencher os `[[ ]]` em docs/WRITEUP.md e docs/VIDEO_SCRIPT.md.
7. Gravar video (<=5 min, YouTube) seguindo o roteiro.
8. Colar Writeup no Kaggle + URLs -> Submit.

## Onde esta cada coisa
- Codigo do agente: `vaqueiro/` (agent.py, tools.py, mcp_client.py)
- Logica compartilhada: `ai_context_core.py`
- MCP server: `mcp_server/server.py`  (ligar com VAQUEIRO_USE_MCP=true)
- Eval: `eval/`   |   Metricas: `scripts/token_metrics.py`
- Projeto de teste: `sample_project/`  (trocar pelo NG-M3 real)
- Docs: `docs/` (DESIGN_SPEC, WRITEUP, VIDEO_SCRIPT, este HANDOFF)
- Setup completo: `README.md`

## Regra fixa
Nunca commitar `.env` / chaves. `.env` ja esta no `.gitignore`.
