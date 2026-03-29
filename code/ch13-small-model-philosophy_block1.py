def baseline_test(model_name, test_dataset):
    scores = []
    for example in test_dataset:
        response = model.generate(
            prompt=example.prompt,
            context=""  # ゼロコンテキスト
        )
        scores.append(evaluate(response, example.expected))
    return np.mean(scores)
