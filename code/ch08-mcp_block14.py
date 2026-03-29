# 社内データベースへの読み取り専用アクセス
class ReadOnlyDBMCPServer:
    def __init__(self, connection_string):
        self.db = create_readonly_connection(connection_string)
    
    def register_tools(self):
        return [
            Tool(
                name="search_records",
                description="Search database records for context information"
            )
        ]
