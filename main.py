from typing import Callable, Tuple
import sys

from PIL import Image


def apply(image: Image, function: Callable) -> Image:
    width, height = image.size
    for w in range(width):
        for h in range(height):
            coordinate = (w, h)
            pixel = image.getpixel(coordinate)
            value = function(pixel)
            image.putpixel(coordinate, value)

    image.show()
    return image


def binary(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
    sum = pixel[0] + pixel[1] + pixel[2]
    if sum > 127 * 3:
        return (255, 255, 255)
    else:
        return (0, 0, 0)


def binary_image(image: Image) -> Image:
    grey_image = apply(image, grey_scale)
    image = apply(grey_image, binary)
    return image


def blue_filter(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (0, 0, pixel[2])


def green_filter(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (0, pixel[1], 0)


def grey_scale(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
    v = int((pixel[0] + pixel[1] + pixel[2]) / 3)
    return (v, v, v)


def red_filter(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (pixel[0], 0, 0)


def resize(image: Image, factor: int) -> Image:
    width, height = image.size
    new_image = Image.new('RGB', (int(width / factor), int(height / factor)))

    for w in range(0, width, factor):
        for h in range(0, height, factor):
            coordinate = (w, h)
            new_coordinate = tuple(int(coord / 4) for coord in coordinate)
            pixel = image.getpixel(coordinate)
            new_image.putpixel(new_coordinate, pixel)

    new_image.show()
    return new_image


def vertical_invert(image: Image) -> Image:
    width, height = image.size
    new_image = Image.new('RGB', (width, height))

    for w in range(width):
        for h in range(height):
            coordinate = (w, h)
            new_h = height - coordinate[1] - 1
            new_coordinate = w, new_h

            pixel = image.getpixel(coordinate)
            new_image.putpixel(new_coordinate, pixel)

    new_image.show()
    return new_image


def main():
    image_name = sys.argv[-1]

    try:
        with Image.open(image_name) as original:
            original.show()

            vertical_invert(original.copy())
            resize(original.copy(), 4)
            apply(original.copy(), grey_scale)
            binary_image(original.copy())
            apply(original.copy(), blue_filter)
            apply(original.copy(), green_filter)
            apply(original.copy(), red_filter)

    except IOError:
        print(f'No image found in path {image_name}')
        sys.exit(1)


if __name__ == '__main__':
    main()