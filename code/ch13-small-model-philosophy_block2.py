class ContextAccess:
    def __init__(self, agent_id, security_level):
        self.agent_id = agent_id
        self.security_level = security_level
    
    def can_access(self, context_item):
        return context_item.required_level <= self.security_level
