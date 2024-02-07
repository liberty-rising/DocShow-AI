import json
import traceback

import httpx
from azure.identity import ClientSecretCredential
from settings import AZURE_CLIENT_ID, AZURE_SECRET_VALUE, AZURE_TENANT_ID


class AzureManager:
    def __init__(self):
        self.credential = ClientSecretCredential(
            AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_SECRET_VALUE
        )
        self.azure_token = self.credential.get_token(
            "https://analysis.windows.net/powerbi/api/.default"
        )

    def get_azure_token(self):
        return self.azure_token.token

    async def get_powerbi_embeded_token(self, workspace_ids, dataset_ids, report_ids):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_azure_token()}",
        }
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "targetWorkspaces": [
                        {"id": workspace_id} for workspace_id in workspace_ids
                    ],
                    "datasets": [
                        {"id": dataset_id, "xmlaPermissions": "ReadOnly"}
                        for dataset_id in dataset_ids
                    ],
                    "reports": [
                        {"id": report_id, "allowEdit": True} for report_id in report_ids
                    ],
                }
                response = await client.post(
                    "https://api.powerbi.com/v1.0/myorg/GenerateToken",
                    headers=headers,
                    content=json.dumps(payload),
                )
                print(f"Response status code: {response.status_code}")
                token = response.json().get("token")
                return token
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
                return None

    async def get_powerbi_reports(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_azure_token()}",
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

    async def get_powerbi_report(self, report_id):
        headers = {"Authorization": f"Bearer {self.get_azure_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.powerbi.com/v1.0/myorg/groups/361eea67-d03b-4799-8779-7c1d6c175182/reports/{report_id}",
                headers=headers,
            )
        return response.json()

    async def get_powerbi_workspaces(self):
        headers = {"Authorization": f"Bearer {self.get_azure_token()}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.powerbi.com/v1.0/myorg/groups", headers=headers
            )
        return response.json()
