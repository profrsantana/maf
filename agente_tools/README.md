# Agente com Tools

Exemplo de um agente usando o **Microsoft Agent Framework (MAF)** com a OpenAI e uso de **tools** (funções). O agente consulta a temperatura atual de qualquer cidade usando a [Open-Meteo API](https://open-meteo.com/) — gratuita e sem necessidade de API key.

## Funcionalidades

- Criação de uma **tool** com o decorator `@tool` do MAF
- Consulta de temperatura real via Open-Meteo API (geocoding + forecast)
- Conexão com a OpenAI usando `OpenAIChatCompletionClient` (Chat Completions API)
- Execução assíncrona do agente

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
cd agente_tools
python agente_tools.py
```

## Referências

- [Documentação do MAF](https://aka.ms/agent-framework)
- [Open-Meteo API](https://open-meteo.com/)
- [OpenAI Platform](https://platform.openai.com/)
