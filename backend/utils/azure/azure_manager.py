from azure.identity import ClientSecretCredential
from settings import AZURE_APP_SECRET, AZURE_CLIENT_ID, AZURE_TENANT_ID


class AzureManager:
    def __init__(self):
        self.credential = ClientSecretCredential(
            AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_APP_SECRET
        )
        self.powerbi_token = self.credential.get_token(
            "https://analysis.windows.net/powerbi/api/.default"
        )

    def get_powerbi_token(self):
        return self.powerbi_token.token
