import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

DIAMETER = 20
IMG_SIZE = 200
MARGIN = 50
COUNT = 10

if __name__ == '__main__':
    max_coord = IMG_SIZE - 2 * MARGIN
    x_arr = MARGIN + np.random.randint(max_coord, size=COUNT)
    y_arr = MARGIN + np.random.randint(max_coord, size=COUNT)
    for i in range(COUNT):
        image = Image.new('RGB', (IMG_SIZE, IMG_SIZE))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), image.size], fill='black')
        draw.ellipse((x_arr[i], y_arr[i], x_arr[i] + DIAMETER, y_arr[i] + DIAMETER), fill='white')
        image.save(f'./data/circles/test_{i:0>2}.jpg')

    x_centers = x_arr + DIAMETER / 2.0
    y_centers = y_arr + DIAMETER / 2.0

    df = pd.DataFrame({
        'x': x_centers,
        'y': y_centers,
    })

    df.to_csv('./data/circles.csv')
