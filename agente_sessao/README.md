# Agente com Sessão

Exemplo de um agente usando o **Microsoft Agent Framework (MAF)** com a OpenAI, **tools** (funções) e **sessão de conversa**. O agente consulta a temperatura atual de qualquer cidade usando a [Open-Meteo API](https://open-meteo.com/) — gratuita e sem necessidade de API key — e mantém o histórico da conversa entre múltiplas interações.

## Funcionalidades

- Criação de uma **tool** com o decorator `@tool` do MAF
- Consulta de temperatura real via Open-Meteo API (geocoding + forecast)
- Conexão com a OpenAI usando `OpenAIChatCompletionClient` (Chat Completions API)
- Criação de uma **sessão** com `agente.create_session()` para manter o contexto entre turnos
- Execução de múltiplos turnos de conversa usando a mesma sessão
- Execução assíncrona do agente

## Fluxo de execução

1. O agente pergunta a temperatura em **São José dos Campos** (chamando a tool `temperatura_atual`)
2. Em seguida, o agente responde de qual cidade falou — demonstrando que a sessão preserva o contexto da conversa

## Pré-requisitos

- Python 3.13+
- Conta na [OpenAI](https://platform.openai.com/) com API key

## Instalação

Crie e ative um ambiente virtual, depois instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

## Execução

```bash
cd agente_sessao
python agente_sessao.py
```

## Referências

- [Documentação do MAF](https://aka.ms/agent-framework)
- [Open-Meteo API](https://open-meteo.com/)
- [OpenAI Platform](https://platform.openai.com/)
