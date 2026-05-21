# ============================================
# ENTROPY ANALYSIS
# ============================================

import math

import numpy as np

# ============================================
# CALCULATE ENTROPY
# ============================================

def calculate_entropy(data):

    histogram, _ = np.histogram(
        data,
        bins=256,
        range=(0, 256)
    )

    histogram = histogram / histogram.sum()

    entropy = -sum(

        p * math.log2(p)

        for p in histogram

        if p > 0

    )

    return entropy