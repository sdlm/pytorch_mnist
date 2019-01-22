from pathlib import Path
import requests

import pickle
import gzip

DATA_PATH = Path("data")
PATH = DATA_PATH / "mnist"

URL = "http://deeplearning.net/data/mnist/"
FILENAME = "mnist.pkl.gz"


def download_data():
    PATH.mkdir(parents=True, exist_ok=True)
    if not (PATH / FILENAME).exists():
            content = requests.get(URL + FILENAME).content
            (PATH / FILENAME).open("wb").write(content)


def get_mnist_data():
    download_data()

    with gzip.open((PATH / FILENAME).as_posix(), "rb") as f:
        ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding="latin-1")

    return x_train, y_train, x_valid, y_valid
