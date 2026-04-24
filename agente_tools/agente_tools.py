import os
import asyncio

import httpx
from pydantic import Field
from typing_extensions import Annotated
from dotenv import load_dotenv
from agent_framework import tool
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv()


@tool(
    name="temperatura_atual",
    description="Obtenha a previsão do tempo para um local específico.",
)
def temperatura_atual(
    location: Annotated[
        str, Field(description="O local para obter a previsão do tempo.")
    ],
) -> str:
    with httpx.Client(timeout=10) as client:
        geo = client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "pt"},
        ).json()

        if not geo.get("results"):
            return f"Não foi possível encontrar a localização '{location}'."

        local = geo["results"][0]
        lat, lon, nome = local["latitude"], local["longitude"], local["name"]

        meteo = client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m",
                "timezone": "auto",
            },
        ).json()

        temp = meteo["current"]["temperature_2m"]

        return f"Temperatura atual em {nome}: {temp}°C."


cliente_openai = OpenAIChatCompletionClient(
    api_key=os.getenv("OPENAI_API_KEY"), model=os.getenv("OPENAI_MODEL")
)


agente = cliente_openai.as_agent(
    name="Agente Básico para previsão do tempo",
    instructions="Você é um assistente amigável com acesso a ferramenta de previsão do tempo. Use a ferramenta para responder perguntas sobre o clima. Mantenha suas respostas breves.",
    tools=[temperatura_atual],
)


async def main():
    result = await agente.run("Qual é a temperatura em São José dos Campos?")
    print(f"Agente: {result}")


if __name__ == "__main__":
    asyncio.run(main())
