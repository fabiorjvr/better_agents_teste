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
- `app/chatbot_agent.py`: ChatbotAgent
  - Carrega `.env` com `python-dotenv`
  - Usa prompt versionado `chatbot_system`
  - Sanitiza mensagens para compatibilidade com Groq
  - `@trace()` para observabilidade no LangWatch
  - Fallback determinístico sem LLM para testes estáveis
- `prompts/chatbot_system.yaml` + `prompts.json`: prompt versionado e registrado
- `tests/scenarios/test_chatbot_agent.py`: cenário simples de resposta
- `tests/scenarios/test_chatbot_basic_response.py`: cenário simples de saudação
- `tests/unit/test_chatbot_fallback.py`: unit test sem LLM (grátis)

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
- Cenários foram simplificados para não depender de agentes nativos que exigem LLM.
- ChatbotAgent usa sanitização e fallback determinístico para manter testes estáveis.

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

## Groq Setup
- Crie a conta no Groq e copie sua chave da API.
- Configure `.env` ou `.env.example` com:
  - `GROQ_API_KEY=sua-chave-aqui`
  - `MODEL_NAME=groq/llama-3.1-70b-instant`
  - `USE_LLM=true`
- Instale dependências: `pip install -r requirements.txt`
- Rode:
  - Unit (sem LLM): `$env:USE_LLM="false"; pytest tests/unit/`
  - Cenários (com Groq): `$env:USE_LLM="true"; pytest tests/scenarios/`
- Visualize no LangWatch: configure `LANGWATCH_API_KEY` e acesse `https://app.langwatch.ai`.

## Projeto WhatsApp Finanças (Teste)
- Objetivo: enviar diariamente às 09:00 rentabilidade de ações brasileiras via WhatsApp (WPPConnect).
- Implementação atual: agendamento lógico e envio stub para custo zero; pronto para troca por conector real.
