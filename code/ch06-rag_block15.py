# Extracted from ch06-rag.md
# Block #15

class GrabAnalyticalRAG:
    def __init__(self):
        self.data_apis = DataArksAPI()
        self.report_templates = ReportTemplateDB()
        
    def generate_report(self, report_request):
        # 関連するAPIとクエリの選択
        relevant_apis = self.data_apis.select_relevant_apis(
            domain=report_request.domain,
            metrics=report_request.metrics
        )
        
        # データ取得・加工
        raw_data = self.data_apis.execute_queries(relevant_apis)
        
        # 類似レポートテンプレート検索
        similar_reports = self.report_templates.find_similar(
            request=report_request,
            top_k=3
        )
        
        # LLMでレポート生成
        return self.generate_analytical_report(
            data=raw_data,
            templates=similar_reports,
            request=report_request
        )