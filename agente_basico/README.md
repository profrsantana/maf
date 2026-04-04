# Agente Básico

Exemplo mínimo de um agente usando o **Microsoft Agent Framework (MAF)** com o Azure AI Foundry. Demonstra como instanciar um cliente Foundry, criar um agente e realizar uma interação simples.

## Pré-requisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) instalado
- Azure CLI instalado e autenticado (`az login`)
- Acesso a um projeto no [Azure AI Foundry](https://ai.azure.com)

## Instalação

Na raiz do repositório, instale as dependências necessárias:

```bash
uv add agent-framework azure-identity
```

Ative o ambiente virtual (caso ainda não esteja ativo):

```bash
source .venv/bin/activate
```

## Configuração

No arquivo `agente_basico.py`, substitua os valores de exemplo pelas informações do seu projeto Foundry:

```python
project_endpoint="https://<seu-servico>.services.ai.azure.com/api/projects/<seu-projeto>"
model="<modelo-desejado>"
```

## Autenticação

O exemplo utiliza `AzureCliCredential`, que aproveita a sessão ativa do Azure CLI. Certifique-se de estar autenticado antes de executar:

```bash
az login
```

## Execução

```bash
cd agente_basico
python agente_basico.py
```

## Referências

- [Documentação do MAF](https://aka.ms/agent-framework)
- [Azure AI Foundry](https://ai.azure.com)
- [azure-identity — Documentação](https://learn.microsoft.com/pt-br/python/api/overview/azure/identity-readme)
