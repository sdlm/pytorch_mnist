import os

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

DIAMETER = 20
IMG_SIZE = 200
MARGIN = 50
TRAIN_COUNT = 10
TEST_COUNT = 10


def generate_images(subset: str, count: int):
    max_coord = IMG_SIZE - 2 * MARGIN
    x_arr = MARGIN + np.random.randint(max_coord, size=count)
    y_arr = MARGIN + np.random.randint(max_coord, size=count)
    is_empty_arr = np.random.randint(2, size=count)
    for i in range(count):
        image = Image.new('RGB', (IMG_SIZE, IMG_SIZE))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), image.size], fill='black')
        if not is_empty_arr[i]:
            coords = (x_arr[i], y_arr[i], x_arr[i] + DIAMETER, y_arr[i] + DIAMETER)
            draw.ellipse(coords, fill='white')
        image.save(f'./data/circles/{subset}/test_{i:0>5}.jpg')

    x_centers = x_arr + DIAMETER / 2.0
    y_centers = y_arr + DIAMETER / 2.0

    df = pd.DataFrame({
        'empty': is_empty_arr,
        'x': x_centers,
        'y': y_centers,
    })

    df.to_csv(f'./data/circles_{subset}.csv', index_label='index')


def create_dir():
    if not os.path.isdir('./data'):
        os.mkdir('./data')
    if not os.path.isdir('./data/circles'):
        os.mkdir('./data/circles')
    if not os.path.isdir('./data/circles/train'):
        os.mkdir('./data/circles/train')
    if not os.path.isdir('./data/circles/test'):
        os.mkdir('./data/circles/test')


if __name__ == '__main__':
    create_dir()
    generate_images('train', 20)
    generate_images('test', 10)
