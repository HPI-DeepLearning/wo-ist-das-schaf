
def apply_erode_kernel(image, output, x, y, kernel_size):
    kernel_height, kernel_width = kernel_size
    image_height, image_width = image.shape
    image_data = []

    for ky in range(-(kernel_height // 2), kernel_height // 2 + 1):
        for kx in range(-(kernel_width // 2), kernel_width // 2 + 1):
            inside_image = 0 <= x + kx < image_width and 0 <= y + ky < image_height

            if inside_image:
                image_data.append(image[y + ky, x + kx])

    output[y, x] = min(image_data)


def apply_dilate_kernel(image, output, x, y, kernel_size):
    kernel_height, kernel_width = kernel_size
    image_height, image_width = image.shape
    image_data = []

    for ky in range(-(kernel_height // 2), kernel_height // 2 + 1):
        for kx in range(-(kernel_width // 2), kernel_width // 2 + 1):
            inside_image = 0 <= x + kx < image_width and 0 <= y + ky < image_height

            if inside_image:
                image_data.append(image[y + ky, x + kx])

    output[y, x] = max(image_data)
