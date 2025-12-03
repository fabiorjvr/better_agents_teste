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
