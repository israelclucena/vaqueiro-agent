# Vaqueiro — DESIGN_SPEC

> Capstone do curso **5-Day AI Agents: Intensive Vibe Coding Course With Google** (Kaggle).
> Agente **Vaqueiro** — conhece todo o "terreno" do repositório sem redescobri-lo a cada sessão.

## 0. Fatos do capstone (lidos da página oficial)

- **Prazo: 6 jul 2026, 23:59 PT = 7 jul, 07:59 de Lisboa.** ~6 dias. Rascunhos não submetidos **não** são avaliados.
- **Já existe um draft seu em andamento** na competição — dá para partir dele.
- **Submissão** só na competição do capstone (id 147722), via **"New Writeup" → Save → "Submit"**.
- **Deploy NÃO é obrigatório** para avaliação (se fizer, documente como reproduzir). Isso libera tempo no sprint.
- 🚨 **Nenhuma API key ou senha no código** (regra explícita da rubrica).

## 1. Entregáveis exigidos (specs exatas)

1. **Kaggle Writeup** — relatório do projeto (título, subtítulo, análise). Precisa **escolher 1 trilha**. **Máx. 2.500 palavras** (acima disso, penalidade).
2. **Cover image** (obrigatória) + **vídeo** no Media Gallery.
3. **Vídeo** — **≤ 5 min**, publicado no **YouTube**.
4. **Project Link público** — URL de demo funcional **ou** repositório público (GitHub) com **README + instruções de setup**.

## 2. Rubrica (100 pts) — onde o esforço rende

- **Categoria 1 — The Pitch (30):** Core Concept & Value (10) · Vídeo YouTube (10) · Writeup (10).
- **Categoria 2 — Implementation (70):** Technical Implementation (50) · Documentation/README (20).

> Leitura estratégica: **70% é código + README.** Priorizar arquitetura, qualidade e comentários no código, uso esperto de ferramentas, e um README forte (problema, solução, arquitetura, setup, diagramas). Pitch (vídeo+writeup+valor) vale 30%.

## 3. Conceitos-chave (mínimo 3) e onde demonstrar

| Conceito | Onde |
|----------|------|
| Agente / Multiagente (ADK) | Código |
| MCP Server | Código |
| Antigravity | Vídeo |
| Segurança | Código ou Vídeo |
| Deployability | Vídeo |
| Agent skills (ex.: Agents CLI) | Código ou Vídeo |

**Os 3 do Vaqueiro (forças do Israel):** MCP Server (código) · Agent skills / Agents CLI (código/vídeo) · Segurança (código/vídeo).
**4º de destaque, se sobrar tempo:** multiagente ADK `Workflow` (código).

## 4. O que é o `.ai-context/`

Pasta versionada que guarda o modelo mental do projeto (arquitetura, convenções, pitfalls, presets de stack, bootstrap prompt, manutenção) para agentes lerem conhecimento curado em vez de re-escanear o código — mais rápido, mais barato em tokens, e preserva as convenções do projeto.

## 5. Arquitetura

**Tools:** `read_ai_context(section)` · `search_codebase(query)` · `read_file(path)` · `propose_context_update(section, content)` (com confirmação humana).
**Memória/contexto:** o `.ai-context/` é a memória de longo prazo; sessão guarda o que já foi carregado; *context budgeting* (carrega só as seções relevantes → métricas de token antes/depois).
**Multiagente (ADK `Workflow`):** Curador → Respondedor → Mantenedor.
**Segurança:** redação de segredos no output · confirmação antes de escrever · sem shell arbitrário · `.env` no `.gitignore` desde o commit 1.

## 6. Stack

ADK (`pip install google-adk`, Python 3.10+; `Agent`, `Workflow`, `adk web`) · Gemini API grátis via AI Studio (`gemini-flash-latest`) · scaffold via Claude Code / agents-cli (também conta como "Agent skills").

## 7. Trilha

- **Agents for Business** — "problemas com custo ou receita em jogo". Vaqueiro reduz horas de onboarding e custo de token de times de dev. Boa história de *valor* (10 pts).
- **Freestyle** — recompensa explicitamente "boas práticas de desenvolvimento e deploy de agentes"; encaixe natural para uma ferramenta de dev focada em craft.
- (Concierge é fraco aqui; é voltado a assistentes pessoais/família.)

## 8. Cronograma — sprint (1 jul → 6 jul)

- **Dia 1 · 1/jul:** setup ADK + chave AI Studio + `.env`/`.gitignore` + agente com `read_ai_context()` no `adk web`. Escolher repo de dogfooding.
- **Dia 2 · 2/jul:** MVP — tools de leitura + agente único respondendo 4–5 perguntas reais, com carregamento seletivo.
- **Dia 3 · 3/jul:** MCP server + guardrails de segurança + eval set (`adk eval`). Multiagente se sobrar.
- **Dia 4 · 4/jul:** **README forte** (20 pts), comentários no código, métricas de token, repo público limpo (sem segredos), gravar o demo local.
- **Dia 5 · 5/jul:** Writeup (≤2.500 palavras, em inglês) + cover image + vídeo YouTube (≤5 min).
- **6/jul:** revisar e **Submit** cedo.

## 9. Pendências

- [ ] **Trilha:** Agents for Business ou Freestyle.
- [ ] **Repo de dogfooding:** o que já tiver o `.ai-context/` mais completo.
- [ ] **Draft existente:** revisar o rascunho já iniciado na competição e alinhar ao Vaqueiro.
