import asyncio
import os
import re
from typing import Any

import asyncpg
from dotenv import load_dotenv
from agent_framework import InMemoryHistoryProvider
from agent_framework.openai import OpenAIChatCompletionClient
from agent_framework import AgentSession, SessionContext, ContextProvider

load_dotenv()


class UserRepository:
    """
    Isola toda a lógica de banco de dados.
    O provider não precisa saber nada sobre SQL.
    """

    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    @classmethod
    async def criar(cls, dsn: str) -> "UserRepository":
        """Cria o pool de conexões e garante que a tabela existe."""
        pool = await asyncpg.create_pool(dsn)
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    user_id   TEXT PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    criado_em TIMESTAMPTZ DEFAULT NOW(),
                    atualizado_em TIMESTAMPTZ DEFAULT NOW()
                )
            """)
        return cls(pool)

    async def buscar_nome(self, user_id: str) -> str | None:
        """Retorna o nome salvo ou None se não existir."""
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT user_name FROM usuarios WHERE user_id = $1",
                user_id,
            )
        return row["user_name"] if row else None

    async def salvar_nome(self, user_id: str, user_name: str) -> None:
        """Insere ou atualiza o nome do usuário (upsert)."""
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO usuarios (user_id, user_name)
                VALUES ($1, $2)
                ON CONFLICT (user_id) DO UPDATE
                    SET user_name     = EXCLUDED.user_name,
                        atualizado_em = NOW()
                """,
                user_id,
                user_name,
            )

    async def fechar(self):
        await self._pool.close()


class PostgresUserMemoryProvider(ContextProvider):
    """
    ContextProvider que persiste o nome do usuário no PostgreSQL.

    Fluxo:
      before_run → busca o nome no banco e injeta nas instruções
      after_run  → se o usuário informou o nome, salva no banco
    """

    SOURCE_ID = "postgres_user_memory"

    def __init__(self, repo: UserRepository, user_id: str):
        super().__init__(self.SOURCE_ID)
        self._repo = repo
        self._user_id = user_id

    async def before_run(
        self,
        *,
        agent: Any,
        session: AgentSession | None,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        """Busca o nome no PostgreSQL e injeta nas instruções do agente."""
        user_name = state.get("user_name")

        if not user_name:
            user_name = await self._repo.buscar_nome(self._user_id)
            if user_name:
                state["user_name"] = user_name
                # print(f"[DB] Nome carregado do PostgreSQL: {user_name}")

        if user_name:
            context.extend_instructions(
                self.source_id,
                f"O nome do usuário é {user_name}. Sempre chame-o pelo nome.",
            )
        else:
            context.extend_instructions(
                self.source_id,
                "Você não sabe o nome do usuário ainda. Pergunte educadamente.",
            )

    async def after_run(
        self,
        *,
        agent: Any,
        session: AgentSession | None,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        """Extrai o nome da mensagem e salva no PostgreSQL."""
        for msg in context.input_messages:
            text = msg.text if hasattr(msg, "text") else ""

            if not isinstance(text, str):
                continue

            padroes = [
                r"meu nome [eé]\s+(\w+)",
                r"pode me chamar de\s+(\w+)",
                r"me chamo\s+(\w+)",
                r"sou o\s+(\w+)",
                r"sou a\s+(\w+)",
            ]

            for padrao in padroes:
                match = re.search(padrao, text.lower())
                if match:
                    nome = match.group(1).capitalize()
                    await self._repo.salvar_nome(self._user_id, nome)
                    state["user_name"] = nome
                    # print(
                    #     f"[DB] Nome '{nome}' salvo no PostgreSQL "
                    #     f"para user_id='{self._user_id}'"
                    # )
                    break


cliente_openai = OpenAIChatCompletionClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL"),
)


db_conn = os.environ.get(
    "POSTGRES_DSN", "postgresql://postgres:senha@localhost:5432/agente_db"
)


async def main():

    USER_ID = "usuario_001"

    repo = await UserRepository.criar(db_conn)
    memoria = PostgresUserMemoryProvider(repo, USER_ID)

    agente = cliente_openai.as_agent(
        name="Agente_Postgres",
        instructions="Você é um assistente amigável e prestativo.",
        context_providers=[memoria],
    )

    try:
        print("-" * 55)
        print("SESSÃO 1 - Novo usuário, sem nome salvo")
        print("-" * 55)

        sessao_1 = agente.create_session()
        print("Usuário: Olá! Tudo bem?")
        resposta = await agente.run("Olá! Tudo bem?", session=sessao_1)
        print(f"Agente: {resposta}\n")
        print("Usuário: Meu nome é Rodrigo")
        resposta = await agente.run("Meu nome é Rodrigo", session=sessao_1)
        print(f"Agente: {resposta}\n")
        print("Usuário: Qual a capital da França?")
        resposta = await agente.run("Qual a capital da França?", session=sessao_1)
        print(f"Agente: {resposta}\n")

        print("-" * 55)
        print("SESSÃO 2 - Retorno do mesmo usuário, nome deve ser lembrado")
        print("-" * 55)
        sessao_2 = agente.create_session()
        print("Usuário: Oi, estou de volta! Se lembra de mim?")
        resposta = await agente.run("Oi, estou de volta!", session=sessao_2)
        print(f"Agente: {resposta}\n")

    finally:
        await repo.fechar()


if __name__ == "__main__":
    asyncio.run(main())
