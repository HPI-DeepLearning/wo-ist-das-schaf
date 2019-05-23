def apply_convolution_2d_kernel(input, output, y, x, kernel):
    # output[y, x] = input[y, x]
    # return

    kernel_radius = len(kernel) // 2
    for k_y in range(-kernel_radius, kernel_radius + 1):
        for k_x in range(-kernel_radius, kernel_radius + 1):
            kernel_value = kernel[kernel_radius + k_y, kernel_radius + k_x]
            output[y - kernel_radius, x - kernel_radius] += kernel_value * input[y + k_y, x + k_x]


# Bonus
def apply_convolution_1d_kernel(input, output, buffer_index, axis, kernel):
    # output[buffer_index] = input[buffer_index]
    # return

    kernel_radius = len(kernel) // 2
    for k in range(-kernel_radius, kernel_radius + 1):
        kernel_value = kernel[k + kernel_radius]
        image_index = list(buffer_index)
        image_index[axis] += k
        output_index = list(buffer_index)
        output_index[axis] -= kernel_radius
        output[output_index[0], output_index[1]] += kernel_value * input[image_index[0], image_index[1]]
