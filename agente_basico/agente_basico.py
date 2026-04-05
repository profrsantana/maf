from dotenv import load_dotenv
import os
import asyncio
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()

credenciais = (
    AzureCliCredential()
)  # necessario autenticação via Azure CLI para acessar o Azure Foundry. Certifique-se de estar logado usando `az login` no terminal.
cliente_foundry = FoundryChatClient(
    project_endpoint=os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT"),
    model=os.getenv("AZURE_FOUNDRY_MODEL"),
    credential=credenciais,
)

agente = cliente_foundry.as_agent(
    name="Agente Básico",
    instructions="Você é um assistente amigável. Mantenha suas respostas breves.",
)


async def main():
    result = await agente.run("Qual é a maior cidade da França?")
    print(f"Agente: {result}")


if __name__ == "__main__":
    asyncio.run(main())
