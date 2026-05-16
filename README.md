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
| [`agente_tools/`](agente_tools/) | Agente com **tools** usando `OpenAIChatCompletionClient` e consulta de temperatura real via Open-Meteo API |
| [`agente_sessao/`](agente_sessao/) | Agente com **sessão de conversa** usando `OpenAIChatCompletionClient`, tools e múltiplos turnos de interação |
| [`agente_memoria/`](agente_memoria/) | Agente com **memória persistente** usando `ContextProvider` customizado e PostgreSQL para lembrar o usuário entre sessões |

## Exemplos

Implementações práticas adicionadas progressivamente, cada uma com foco em uma funcionalidade ou caso de uso específico do framework. Cada exemplo tem seu próprio README com contexto, instruções de configuração e anotações sobre os resultados.

### `agente_basico`

Implementação mínima de um agente usando o MAF com o Azure AI Foundry. Demonstra:

- Autenticação com `AzureCliCredential`
- Configuração do `FoundryChatClient` via variáveis de ambiente (`.env`)
- Criação de um agente com `client.as_agent()`
- Execução de uma pergunta simples de forma assíncrona

**Stack:** `agent-framework` · `azure-identity` · `python-dotenv`

### `agente_tools`

Agente com uso de **tools** (funções) conectado à OpenAI. Demonstra:

- Criação de uma tool com o decorator `@tool` do MAF
- Consulta de temperatura real via [Open-Meteo API](https://open-meteo.com/) (gratuita, sem API key)
- Conexão com a OpenAI usando `OpenAIChatCompletionClient` (Chat Completions API)
- Execução assíncrona do agente com chamada automática de ferramenta

**Stack:** `agent-framework` · `agent-framework-openai` · `python-dotenv` · `httpx`

### `agente_sessao`

Agente com **sessão de conversa** conectado à OpenAI. Demonstra:

- Criação de uma sessão com `agente.create_session()` para preservar o contexto entre turnos
- Execução de múltiplos turnos de conversa usando a mesma sessão
- Uso de tools com o decorator `@tool` do MAF
- Consulta de temperatura real via [Open-Meteo API](https://open-meteo.com/) (gratuita, sem API key)

**Stack:** `agent-framework` · `agent-framework-openai` · `python-dotenv` · `httpx`

### `agente_memoria`

Agente com **memória persistente** entre sessões usando PostgreSQL. Demonstra:

- Implementação de um `ContextProvider` customizado (`PostgresUserMemoryProvider`)
- Padrão repositório (`UserRepository`) para isolar a lógica de banco de dados
- Detecção automática do nome do usuário via regex em `after_run`
- Injeção do nome nas instruções do agente via `before_run`
- Cache em memória (`state`) para evitar consultas desnecessárias ao banco durante a mesma sessão
- Persistência que sobrevive entre sessões, reinicializações e deploys

**Stack:** `agent-framework` · `agent-framework-openai` · `python-dotenv` · `asyncpg`

## Série de Posts

Acompanhe os artigos publicados sobre o MAF no blog:

| # | Título | Descrição | Data |
|---|--------|-----------|------|
| 1 | [Microsoft Agent Framework Versão 1.0 Lançada](https://profrsantana.github.io/posts/maf/?utm_source=github&utm_medium=readme) | Introdução à série — visão geral do MAF, proposta PRO-CODE, foco enterprise e integração com o ecossistema Microsoft | 03/04/2026 |
| 2 | [Agente básico com Microsoft Agent Framework usando Python](https://profrsantana.github.io/posts/agente_basico/?utm_source=github&utm_medium=readme) | Conceito de agentes, enterprise ready e implementação de um agente básico com Python e Azure AI Foundry | 11/04/2026 |
| 3 | [Agente com Tools usando Microsoft Agent Framework](https://profrsantana.github.io/posts/agente_tool/?utm_source=github&utm_medium=readme) | Uso de tools com o decorator `@tool`, consulta de temperatura real via Open-Meteo API e conexão com a OpenAI | 24/04/2026 |
| 4 | [Agente com Sessão usando Microsoft Agent Framework](https://profrsantana.github.io/posts/agente_sessao/?utm_source=github&utm_medium=readme) | Uso de sessão de conversa com `create_session()` para manter o contexto entre múltiplos turnos de interação | 08/05/2026 |
| 5 | [Agente com Memória Persistente usando Microsoft Agent Framework](https://profrsantana.github.io/posts/agente_memoria/?utm_source=github&utm_medium=readme) | Persistência de memória entre sessões com `ContextProvider` customizado e PostgreSQL via `asyncpg` | — |

## Referências

- [Microsoft Agent Framework — Documentação Oficial](https://aka.ms/agent-framework)
- [Azure AI Foundry](https://ai.azure.com)

---

> Em desenvolvimento. Implementações e anotações são adicionadas continuamente conforme a exploração avança.

