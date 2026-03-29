# Extracted from ch13-small-model-philosophy.md
# Block #9

def calculate_monthly_cost(
    queries_per_day: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    model_pricing: dict
):
    monthly_queries = queries_per_day * 30
    input_cost = (avg_input_tokens / 1_000_000) * model_pricing['input']
    output_cost = (avg_output_tokens / 1_000_000) * model_pricing['output']
    total_cost_per_query = input_cost + output_cost
    return monthly_queries * total_cost_per_query