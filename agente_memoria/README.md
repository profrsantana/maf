# Agente com Memória Persistente (PostgreSQL)

Exemplo de um agente usando o **Microsoft Agent Framework (MAF)** com a OpenAI e **persistência de memória em PostgreSQL**. O agente lembra o nome do usuário entre sessões diferentes, usando um `ContextProvider` customizado que salva e recupera dados do banco.

## Funcionalidades

- **ContextProvider customizado** (`PostgresUserMemoryProvider`) que persiste dados no PostgreSQL
- **Repositório** (`UserRepository`) que isola toda a lógica de banco de dados
- Detecção automática do nome do usuário via regex (ex: "meu nome é Rodrigo", "me chamo ...", "pode me chamar de ...")
- Persistência do nome entre sessões usando `before_run` e `after_run`
- Cache em memória (`state`) para evitar consultas desnecessárias ao banco durante a mesma sessão
- Simulação de duas sessões separadas para demonstrar a persistência

## Fluxo de execução

1. **Sessão 1**: `before_run` verifica o banco → nome não encontrado → agente pergunta → usuário informa → `after_run` detecta via regex e salva no PostgreSQL
2. **Sessão 2**: Nova sessão (sem histórico) → `before_run` busca o nome no banco → encontra → injeta nas instruções → agente já conhece o usuário pelo nome

## Pré-requisitos

- Python 3.13+
- Conta na [OpenAI](https://platform.openai.com/) com API key
- PostgreSQL rodando (local ou remoto)

## Instalação

Crie e ative um ambiente virtual, depois instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### PostgreSQL com Docker (opcional)

```bash
docker run -d \
  --name postgres-agente \
  -e POSTGRES_PASSWORD=senha \
  -e POSTGRES_DB=agente_db \
  -p 5432:5432 \
  postgres:17
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
POSTGRES_DSN=postgresql://postgres:senha@localhost:5432/agente_db
```

## Execução

```bash
cd agente_memoria
python agente_memoria.py
```

## Referências

- [Documentação do MAF](https://aka.ms/agent-framework)
- [asyncpg](https://magicstack.github.io/asyncpg/)
- [OpenAI Platform](https://platform.openai.com/)
