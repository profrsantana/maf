import os
import asyncio

from random import randint
from pydantic import Field
from typing_extensions import Annotated
from dotenv import load_dotenv
from agent_framework import tool
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv()


@tool
def previsao_do_tempo(
    location: Annotated[
        str, Field(description="O local para obter a previsão do tempo.")
    ],
) -> str:
    """Obtenha a previsão do tempo para um local específico."""
    opcoes_tempo = ["ensolarado", "nublado", "chuvoso", "tempestuoso"]
    return f"O clima em {location} está {opcoes_tempo[randint(0, 3)]} com uma máxima de {randint(10, 30)}°C."


cliente_openai = OpenAIChatCompletionClient(
    api_key=os.getenv("OPENAI_API_KEY"), model=os.getenv("OPENAI_MODEL")
)


agente = cliente_openai.as_agent(
    name="Agente Básico para previsão do tempo",
    instructions="Você é um assistente amigável com acesso a ferramenta de previsão do tempo. Use a ferramenta para responder perguntas sobre o clima. Mantenha suas respostas breves.",
    tools=[previsao_do_tempo],
)


async def main():
    result = await agente.run("Qual é a temperatura em Paris?")
    print(f"Agente: {result}")


if __name__ == "__main__":
    asyncio.run(main())
