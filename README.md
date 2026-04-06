# Microsoft Agent Framework — Exploração e Exemplos

Repositório prático para explorar o **Microsoft Agent Framework (MAF)**: sua arquitetura, funcionalidades principais, integrações e casos de uso reais. Serve também como diário de aprendizado pessoal, registrando descobertas e impressões ao longo da jornada.

## Objetivos

- Entender a arquitetura do MAF e seus componentes fundamentais
- Explorar funcionalidades nativas: orquestração de agentes, memória, uso de ferramentas, comunicação multi-agente, etc.
- Testar integrações com serviços e APIs externas
- Documentar casos de uso e cenários práticos onde o MAF se destaca
- Compartilhar aprendizados e lições da experiência com o framework

## Estrutura

| Pasta | Descrição |
|-------|-----------|
| [`agente_basico/`](agente_basico/) | Agente mínimo usando `FoundryChatClient` com Azure AI Foundry e autenticação via Azure CLI |

## Exemplos

Implementações práticas adicionadas progressivamente, cada uma com foco em uma funcionalidade ou caso de uso específico do framework. Cada exemplo tem seu próprio README com contexto, instruções de configuração e anotações sobre os resultados.

### `agente_basico`

Implementação mínima de um agente usando o MAF com o Azure AI Foundry. Demonstra:

- Autenticação com `AzureCliCredential`
- Configuração do `FoundryChatClient` via variáveis de ambiente (`.env`)
- Criação de um agente com `client.as_agent()`
- Execução de uma pergunta simples de forma assíncrona

**Stack:** `agent-framework` · `azure-identity` · `python-dotenv`

## Série de Posts

Acompanhe os artigos publicados sobre o MAF no blog:

| # | Título | Descrição | Data |
|---|--------|-----------|------|
| 1 | [Microsoft Agent Framework Versão 1.0 Lançada](https://profrsantana.github.io/posts/maf/) | Introdução à série — visão geral do MAF, proposta PRO-CODE, foco enterprise e integração com o ecossistema Microsoft | 03/04/2026 |

## Referências

- [Microsoft Agent Framework — Documentação Oficial](https://aka.ms/agent-framework)
- [Azure AI Foundry](https://ai.azure.com)

---

> Em desenvolvimento. Implementações e anotações são adicionadas continuamente conforme a exploração avança.

