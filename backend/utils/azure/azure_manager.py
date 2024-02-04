import traceback

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
        return self.powerbi_token.token

    async def get_powerbi_reports(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_powerbi_token()}",
        }
        print(headers)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    # "https://analysis.windows.net/powerbi/api/v1.0/myorg/reports",
                    # headers=headers
                    "https://api.powerbi.com/v1.0/myorg/groups/361eea67-d03b-4799-8779-7c1d6c175182/reports",
                    headers=headers,
                )
                print(f"Response status code: {response.status_code}")
                if response.status_code == 200:
                    response_json = response.json()
                    print(response_json)
                    return response_json
                else:
                    print(f"Response content: {response.content}")
                    return None
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
                return None

    # async def get_powerbi_report(self, report_id):
    #     headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(
    #             f"https://api.powerbi.com/v1.0/myorg/reports/{report_id}",
    #             headers=headers,
    #         )
    #     print(response.json())
    #     return response.json()

    # async def create_powerbi_workspace(self, name):
    #     headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(
    #             "https://api.powerbi.com/v1.0/myorg/groups", headers=headers
    #         )
    #     return response

    async def get_powerbi_workspaces(self):
        headers = {"Authorization": f"Bearer {self.get_powerbi_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.powerbi.com/v1.0/myorg/groups", headers=headers
            )
        return response.json()
