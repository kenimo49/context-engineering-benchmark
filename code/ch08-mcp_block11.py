# Extracted from ch08-mcp.md
# Block #11

# 最小限のMCPサーバー
class SimpleMCPServer:
    def __init__(self, domain="files"):
        self.domain = domain
        self.resources = []
        self.tools = []
    
    def add_resource(self, uri, name, description):
        self.resources.append(Resource(uri, name, description))
    
    def add_tool(self, name, description, handler):
        self.tools.append(Tool(name, description, handler))
    
    async def serve(self):
        # 基本的なMCPサーバー実装
        pass