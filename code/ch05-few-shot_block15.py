# Extracted from ch05-few-shot.md
# Block #15

def validate_few_shot_quality(examples):
    quality_metrics = {
        "consistency": check_output_consistency(examples),
        "diversity": measure_input_diversity(examples),  
        "appropriateness": assess_response_quality(examples)
    }
    return quality_metrics