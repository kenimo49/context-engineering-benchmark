class CustomerDataMCPServer:
    """顧客データ専用MCPサーバー"""
    
    def __init__(self, database_config):
        self.db = CustomerDatabase(database_config)
        self.privacy_filter = PrivacyFilter()
        
    def register_resources(self):
        return [
            Resource(
                uri="customer://profile/{customer_id}",
                name="Customer Profile",
                description="Customer profile information with privacy filtering",
                mime_type="application/json"
            ),
            Resource(
                uri="customer://orders/{customer_id}",
                name="Order History", 
                description="Customer order history for support context",
                mime_type="application/json"
            )
        ]
    
    def register_tools(self):
        return [
            Tool(
                name="lookup_customer",
                description="Look up customer information by email or ID for support context",
                input_schema={
                    "type": "object",
                    "properties": {
                        "identifier": {"type": "string", "description": "Email or customer ID"},
                        "include_orders": {"type": "boolean", "default": False}
                    }
                }
            ),
            Tool(
                name="update_customer_notes", 
                description="Add support notes to customer profile",
                input_schema={
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "string"},
                        "note": {"type": "string", "description": "Support interaction note"}
                    }
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name, arguments):
        if tool_name == "lookup_customer":
            return await self.lookup_customer_for_context(arguments)
        elif tool_name == "update_customer_notes":
            return await self.update_customer_notes(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def lookup_customer_for_context(self, arguments):
        """Context Engineering最適化された顧客検索"""
        customer_data = await self.db.lookup_customer(arguments["identifier"])
        
        if not customer_data:
            return {"error": "Customer not found"}
        
        # プライバシーフィルタリング
        filtered_data = self.privacy_filter.filter_for_support_context(
            customer_data
        )
        
        # Context用の構造化
        context_optimized = {
            "customer_summary": filtered_data["summary"],
            "support_relevant_info": filtered_data["support_info"],
            "recent_interactions": filtered_data["recent_interactions"][:3]
        }
        
        if arguments.get("include_orders"):
            context_optimized["recent_orders"] = await self.get_recent_orders_summary(
                customer_data["id"]
            )
        
        return context_optimized
