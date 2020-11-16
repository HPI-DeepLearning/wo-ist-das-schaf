def apply_convolution_2d_kernel(input, output, y, x, channel, image_width, image_height, kernel):
    # output[y, x, channel] = input[y, x, channel]
    # return

    kernel_radius = len(kernel) // 2
    normalization_factor = 0
    for k_y in range(-kernel_radius, kernel_radius + 1):
        for k_x in range(-kernel_radius, kernel_radius + 1):
            kernel_value = kernel[kernel_radius - k_y, kernel_radius - k_x]
            inside_image = 0 <= x + k_x < image_width and 0 <= y + k_y < image_height
            if inside_image:
                normalization_factor += kernel_value
                output[y, x, channel] += kernel_value * input[y + k_y, x + k_x, channel]
    output[y, x, channel] /= max(normalization_factor, 1)


# Bonus
def apply_convolution_1d_kernel(input, output, buffer_index, axis, max_axis_value, kernel):
    # output[buffer_index] = input[buffer_index]
    # return

    kernel_radius = len(kernel) // 2
    normalize_factor = 0
    for k in range(-kernel_radius, kernel_radius):
        inside_image = 0 <= buffer_index[axis] + k < max_axis_value
        if inside_image:
            kernel_value = kernel[k + kernel_radius]
            normalize_factor += kernel_value
            image_index = list(buffer_index)
            image_index[axis] += k
            image_index = tuple(image_index)
            output[buffer_index] += kernel_value * input[image_index]
    output[buffer_index] /= max(normalize_factor, 1)
