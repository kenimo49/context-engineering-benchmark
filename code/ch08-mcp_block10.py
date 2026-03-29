# Extracted from ch08-mcp.md
# Block #10

class SecureContextMCPServer:
    """セキュリティファーストのコンテキストサーバー"""
    
    def __init__(self):
        self.auth_manager = AuthenticationManager()
        self.permission_manager = PermissionManager()
        self.audit_logger = AuditLogger()
        
    async def handle_request(self, request, client_info):
        # Step 1: 認証確認
        user_context = await self.auth_manager.authenticate(client_info)
        if not user_context:
            raise AuthenticationError("Invalid authentication")
        
        # Step 2: 権限確認
        if not self.permission_manager.can_access_context(
            user_context, request.resource
        ):
            raise PermissionError("Insufficient permissions")
        
        # Step 3: 監査ログ
        self.audit_logger.log_context_access(
            user=user_context.user_id,
            resource=request.resource,
            timestamp=datetime.utcnow()
        )
        
        # Step 4: セキュアなコンテキスト提供
        return await self.provide_secure_context(request, user_context)
    
    async def provide_secure_context(self, request, user_context):
        """ユーザーの権限レベルに応じたコンテキスト提供"""
        base_context = await self.get_base_context(request.resource)
        
        # 権限ベースフィルタリング
        filtered_context = self.permission_manager.filter_context_by_permissions(
            base_context, user_context.permissions
        )
        
        # 機密情報のマスキング
        masked_context = self.apply_privacy_masking(
            filtered_context, user_context.privacy_level
        )
        
        return masked_context