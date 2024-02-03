import httpx
from azure.identity import ClientSecretCredential
from settings import AZURE_CLIENT_ID, AZURE_SECRET_VALUE, AZURE_TENANT_ID


class AzureManager:
    def __init__(self):
        self.credential = ClientSecretCredential(
            AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_SECRET_VALUE
        )
        self.powerbi_token = self.credential.get_token(
            "https://analysis.windows.net/powerbi/api/.default"
        )

    def get_powerbi_token(self):
        print(self.powerbi_token.token)
        return self.powerbi_token.token

    async def get_powerbi_reports(self):
        headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.powerbi.com/v1.0/myorg/reports", headers=headers
            )
        print(response)
        return response

    async def create_powerbi_workspace(self, name):
        headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.powerbi.com/v1.0/myorg/groups", headers=headers
            )
        return response

    async def get_powerbi_workspaces(self):
        headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.powerbi.com/v1.0/myorg/groups", headers=headers
            )
        return response

    async def get_powerbi_report(self, report_id):
        headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.powerbi.com/v1.0/myorg/reports/{report_id}",
                headers=headers,
            )
        print(response)
        return response
