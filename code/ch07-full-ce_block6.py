class ToolOutputStructurizer:
    def __init__(self):
        self.output_formatters = {
            "api_response": APIResponseFormatter(),
            "database_query": DatabaseResultFormatter(), 
            "file_content": FileContentFormatter(),
            "web_scrape": WebContentFormatter()
        }
    
    def structure_tool_output(self, tool_name, raw_output, context_purpose):
        formatter = self.output_formatters.get(
            self.get_tool_type(tool_name),
            DefaultFormatter()
        )
        
        structured_output = formatter.format(
            raw_output, 
            context_purpose=context_purpose
        )
        
        return self.add_metadata(structured_output, tool_name)
    
    def add_metadata(self, structured_output, tool_name):
        return {
            "source": f"Tool: {tool_name}",
            "timestamp": datetime.utcnow().isoformat(),
            "content": structured_output,
            "type": "tool_output"
        }

class APIResponseFormatter:
    def format(self, raw_response, context_purpose="general"):
        try:
            data = json.loads(raw_response)
            
            if context_purpose == "debugging":
                return self.format_for_debugging(data)
            elif context_purpose == "user_info":
                return self.format_for_user_info(data)
            else:
                return self.format_general(data)
                
        except json.JSONDecodeError:
            return f"Raw response: {raw_response[:500]}..."
    
    def format_for_user_info(self, data):
        # ユーザー情報として重要な部分のみ抽出
        essential_fields = ["id", "name", "email", "status", "last_login"]
        
        formatted = "User Information:\n"
        for field in essential_fields:
            if field in data:
                formatted += f"- {field.replace('_', ' ').title()}: {data[field]}\n"
        
        return formatted
