from functools import reduce

import numpy as np


def threshold(image, min_values, max_values):
    # schnelle loesung

    channel_thresholds = []
    for channel in range(image.shape[-1]):
        thresholded = np.bitwise_and(min_values[channel] <= image[:, :, channel], image[:, :, channel] <= max_values[channel])
        channel_thresholds.append(thresholded)

    return reduce(lambda x, y: np.bitwise_and(x, y), channel_thresholds, np.ones_like(image[:, :, 0]))


def naive_threshold(image, min_values, max_values):
    # etwas langsamere loesung

    height, width, num_channels = image.shape
    thresholded_image = np.zeros((height, width), dtype=image.dtype)

    for y in range(height):
        for x in range(width):
            do_threshold = all([min_values[c] <= image[y, x, c] <= max_values[c] for c in range(num_channels)])
            thresholded_image[y, x] = do_threshold

    return thresholded_image
