# 既存API のMCPラッパー
class APIMCPWrapper:
    def __init__(self, api_base_url, api_key):
        self.api = APIClient(api_base_url, api_key)
    
    def register_tools(self):
        return [
            Tool(
                name="fetch_api_data",
                description="Fetch data from API for contextual information"
            )
        ]
