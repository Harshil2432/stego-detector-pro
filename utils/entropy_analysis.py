import numpy as np

def calculate_entropy(data):
    try:
        data = data.astype(np.uint8)

        histogram = np.bincount(data, minlength=256)
        probs = histogram / len(data)

        entropy = -np.sum([p * np.log2(p) for p in probs if p > 0])
        return entropy

    except Exception as e:
        print("[ERROR in entropy]", e)
        return 0