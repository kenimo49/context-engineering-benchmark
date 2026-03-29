# Extracted from ch08-mcp.md
# Block #5

class ContextAwareTool:
    def __init__(self, name, description, parameters, context_hints=None):
        self.name = name
        self.description = description  # これがLLMのコンテキストになる
        self.parameters = parameters
        self.context_hints = context_hints or {}
    
    def to_context_description(self):
        """Context Engineering最適化されたツール説明"""
        context_desc = f"""
Tool: {self.name}

Purpose: {self.description}

When to use:
{self._generate_usage_context()}

Parameters:
{self._format_parameters_for_context()}

Example usage:
{self._generate_example_usage()}

Context considerations:
{self._generate_context_considerations()}
"""
        return context_desc
    
    def _generate_usage_context(self):
        """いつこのツールを使うべきかの説明"""
        usage_patterns = self.context_hints.get('usage_patterns', [])
        
        if not usage_patterns:
            return "Use when the task requires this tool's functionality."
        
        return "\n".join([f"- {pattern}" for pattern in usage_patterns])
    
    def _generate_context_considerations(self):
        """Context Engineering上の考慮事項"""
        considerations = []
        
        if self.context_hints.get('high_latency'):
            considerations.append("Tool has high latency - consider batching requests")
        
        if self.context_hints.get('expensive_operation'):
            considerations.append("Tool is expensive - verify necessity before use")
        
        if self.context_hints.get('requires_confirmation'):
            considerations.append("Tool requires user confirmation for destructive operations")
        
        return "\n".join([f"- {c}" for c in considerations])

# 実際のツール定義例
email_tool = ContextAwareTool(
    name="send_email",
    description="Send an email to specified recipients with subject and body",
    parameters={
        "to": {"type": "string", "description": "Recipient email address"},
        "subject": {"type": "string", "description": "Email subject line"},
        "body": {"type": "string", "description": "Email body content"}
    },
    context_hints={
        "usage_patterns": [
            "User explicitly requests to send an email",
            "Automated notification is required",
            "Follow-up communication is needed"
        ],
        "expensive_operation": True,
        "requires_confirmation": True
    }
)