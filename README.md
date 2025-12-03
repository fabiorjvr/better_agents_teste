# Better Agents — Projeto de Testes

## Visão Geral
- Projeto estruturado seguindo o padrão Better Agents para desenvolvimento de AI Agents testáveis, observáveis e prontos para produção.
- Inclui agentes de exemplo, prompts versionados, testes unitários e cenários, além de instrumentação com LangWatch.
- Foco atual: custos zero/baixos usando modelos grátis (Groq, Gemini) e stubs para integrações externas.

## Estrutura do Projeto
- `app/` código dos agentes e ferramentas
- `tests/` cenários end-to-end e testes unitários
- `prompts/` prompts versionados em YAML
- `prompts.json` registro central dos prompts
- `AGENTS.md` diretrizes de desenvolvimento
- `.env.example` variáveis de ambiente
- `.mcp.json` configuração MCP
- `.gitignore` proteção contra commit de segredos

## Principais Componentes
- `app/agent.py`: RecipeAgent
  - Carrega `.env` com `python-dotenv`
  - Usa prompt versionado `vegetarian_recipe_v1`
  - Sanitiza mensagens para compatibilidade com Groq removendo campos não suportados
  - `@trace()` para observabilidade no LangWatch
  - Fallback determinístico sem LLM para testes estáveis
- `prompts/vegetarian_recipe.yaml` + `prompts.json`: prompt versionado e registrado
- `tests/scenarios/test_vegetarian_recipe.py`: cenário de receita vegetariana
  - Simula conversa e valida critérios funcionais
  - Marcado como `xfail` para compatibilidade com Groq/Judge nativo (trace_id)
- `tests/unit/test_agent_llm.py`: teste unitário do RecipeAgent com LLM (Groq)
  - Passando com `groq/llama-3.1-70b-instant`
- `app/tools/finance_api.py`: stub de retorno de ações (PETR4, VALE3, ITUB4)
- `app/tools/whatsapp_sender.py`: stub de envio via WPPConnect
- `app/finance_agent.py`: FinanceAgent
  - Agenda relatório diário às 09:00, compõe resumo e simula envio WhatsApp
  - `@trace()` e uso de stubs para custo zero
- `tests/unit/test_financas_agent.py`: teste unitário do FinanceAgent (passando)
- `tests/scenarios/test_whatsapp_financas.py`: cenário WhatsApp Finanças (xfail)

## Configuração
1. Crie `.env` baseado em `.env.example`:
   - `LANGWATCH_API_KEY=`
   - `LANGWATCH_ENDPOINT=https://app.langwatch.ai`
   - `MODEL_NAME=groq/llama-3.1-70b-instant`
   - `GROQ_API_KEY=`
   - `USE_LLM=true`
   - (Opcional) `GEMINI_API_KEY=` para testes com Gemini
2. Instale dependências (Python >= 3.11):
   - `pip install langwatch langwatch-scenario litellm pytest pyyaml python-dotenv pytest-asyncio`

## Execução
- Testes unitários (sem custos):
  - `pytest tests/unit/`
- Cenários (com xfail por compatibilidade inicial):
  - `pytest tests/scenarios/`
- Alternar uso de LLM no agente:
  - PowerShell: `setx USE_LLM false` (ou temporário: `$env:USE_LLM="false"`)
  - Modelo Groq: `MODEL_NAME=groq/llama-3.1-70b-instant`

## Observabilidade
- `@trace()` instrumenta agentes; com `LANGWATCH_API_KEY` e `LANGWATCH_ENDPOINT` configurados, você vê simulações e traces detalhados no LangWatch.
- Benefícios:
  - Tracing de cada chamada, custos e latências
  - Diagnóstico de falhas e gargalos
  - Dataset para avaliações controladas

## Filosofia Better Agents
- TDD para Agents: cenários antes de features
- Pirâmide de Testes: unitários → cenários → avaliações
- Versionamento de prompts: YAML + registro em `prompts.json`
- Observabilidade first: instrumentar desde o início

## Limitações e Decisões
- Cenários com `UserSimulatorAgent`/`JudgeAgent` nativos + Groq podem falhar por inclusão de `trace_id` nas mensagens do provider; por isso os cenários estão `xfail`.
- Agente receita usa sanitização de mensagens e fallback determinístico para manter testes estáveis.
- FinanceAgent usa stubs (sem custos) para finanças e WhatsApp; integração real pode ser acoplada depois.

## Próximos Passos
- Adicionar conector HTTP real para WPPConnect e cenário com mock/integração
- Substituir stub financeiro por API gratuita (ex.: Brapi/yfinance) mantendo testes determinísticos
- Adicionar avaliações no notebook com latência/custo reais e critérios de qualidade
- Configurar CI para rodar unitários e cenários (xfail conhecidos) e publicar resultados

## Comandos Úteis
- Rodar unit: `pytest tests/unit/`
- Rodar cenários: `pytest tests/scenarios/`
- Ver simulações: acessar `https://app.langwatch.ai`

## Segurança
- `.env` e segredos são ignorados por `.gitignore` (não serão commitados).
- Nunca coloque chaves em código ou YAML de prompts.

## Uso de Groq e Gemini
- Priorizar tiers grátis; alternar provider via `MODEL_NAME` e variáveis do `.env`.
- Exemplo: `MODEL_NAME=groq/llama-3.1-70b-instant` ou `MODEL_NAME=gemini/gemini-1.5-flash`.

## Projeto WhatsApp Finanças (Teste)
- Objetivo: enviar diariamente às 09:00 rentabilidade de ações brasileiras via WhatsApp (WPPConnect).
- Implementação atual: agendamento lógico e envio stub para custo zero; pronto para troca por conector real.
