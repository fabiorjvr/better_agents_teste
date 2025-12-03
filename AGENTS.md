# Better Agents — Diretrizes do Projeto

## Princípios
- TDD para Agents: escreva cenários antes das features
- Pirâmide de Testes: unitários → cenários → avaliações
- Versionamento de Prompts: YAML + `prompts.json`
- Observabilidade First: `@trace()` do LangWatch e traces completos

## Estrutura
```
app/
tests/
  evaluations/
  scenarios/
prompts/
prompts.json
.mcp.json
.env
AGENTS.md
```

## Checklist de Quality
- Cenário escrito e passando
- Prompt versionado em YAML
- Código instrumentado com `@trace()`
- Avaliação criada (se aplicável)
- Edge cases cobertos
- Documentação atualizada aqui
- Variáveis em `.env.example`

## Observabilidade
- Configure `LANGWATCH_API_KEY` e `LANGWATCH_ENDPOINT`
- Trace cada chamada de modelo e ferramentas

## Execução
- Rodar cenários: `pytest tests/scenarios/`
- Avaliações: abrir `tests/evaluations/` no Jupyter
- Sync de prompts: `better-agents prompts sync`

## 📊 Dashboard LangWatch - Como Acompanhar

### Acesso
- URL: `https://app.langwatch.ai`
- Project ID: `whatsapp-bot-prod-Q6G0lH`
- Mensagens aparecem quando `@trace()` está ativo

### 3 Telas Principais
#### 1. Analytics
- Requests (volume), Error Rate (< 10%), Avg Latency (< 1s)
#### 2. Traces
- Input/Output, Status, Latência, Tokens, Custo
#### 3. Simulations
- Nome do cenário, data/hora, passou/falhou, duração

### Como Debugar Usando LangWatch
1. Abra Simulations e selecione o run
2. Revise a conversa e identifique o erro
3. Abra o trace com falha e verifique input/output
4. Ajuste prompt ou agente e rode pytest novamente

### Métricas Para Monitorar
- Taxa Erro: alvo < 5%
- Latência Média: alvo < 500ms
- Custo por chamada: alvo < $0.01
- Uptime: alvo 99%
