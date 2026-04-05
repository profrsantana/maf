from dotenv import load_dotenv
import os
import asyncio
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()

credential = AzureCliCredential()
client = FoundryChatClient(
    project_endpoint=os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT"),
    model=os.getenv("AZURE_FOUNDRY_MODEL"),
    credential=credential,
)

agent = client.as_agent(
    name="HelloAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
)


async def main():
    # Non-streaming: get the complete response at once
    result = await agent.run("What is the largest city in France?")
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
