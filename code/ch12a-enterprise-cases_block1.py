# Extracted from ch12a-enterprise-cases.md
# Block #1

import boto3

def enterprise_rag_query(question: str, user_dept: str, kb_id: str) -> dict:
    """権限フィルタ付きエンタープライズRAGクエリの基本形"""
    client = boto3.client('bedrock-agent-runtime')
    
    # ユーザーの部署に基づくアクセスフィルタ
    access_filter = {
        'andAll': [
            {'equals': {'key': 'department', 'value': user_dept}},
            {'in': {'key': 'security_level', 'value': ['public', 'internal']}}
        ]
    }
    
    response = client.retrieve_and_generate(
        input={'text': question},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kb_id,
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0',
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'numberOfResults': 10,
                        'overrideSearchType': 'HYBRID',
                        'filter': access_filter
                    }
                }
            }
        }
    )
    
    return {'answer': response['output']['text']}