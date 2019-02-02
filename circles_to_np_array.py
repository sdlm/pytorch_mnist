import numpy as np
from PIL import Image, ImageDraw

DIAMETER = 20
IMG_SIZE = 200
MARGIN = 50
TRAIN_COUNT = 10
TEST_COUNT = 10


def generate_image(is_not_empty: int, x: int, y: int) -> Image:
    image = Image.new('L', (IMG_SIZE, IMG_SIZE))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), image.size], fill='black')
    if is_not_empty:
        coords = (x, y, x + DIAMETER, y + DIAMETER)
        draw.ellipse(coords, fill='white')
    return image


def generate_images(count: int):
    max_coord = IMG_SIZE - 2 * MARGIN
    x_arr = MARGIN + np.random.randint(max_coord, size=count)
    y_arr = MARGIN + np.random.randint(max_coord, size=count)
    is_not_empty_arr = np.random.randint(2, size=count)
    images = [
        generate_image(is_not_empty_arr[i], x_arr[i], y_arr[i])
        for i in range(count)
    ]
    arr = np.array([
        np.array(im)
        for im in images
    ])

    # x_centers = x_arr + DIAMETER / 2.0
    # y_centers = y_arr + DIAMETER / 2.0
    #
    # df = pd.DataFrame({
    #     'empty': is_not_empty_arr,
    #     'x': x_centers,
    #     'y': y_centers,
    # })

    return arr, is_not_empty_arr


if __name__ == '__main__':
    train, train_labels = generate_images(20)
    test, test_labels = generate_images(10)
