import os

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset

from download_data import get_mnist_data

bs = 64  # batch size
lr = 0.1  # learning rate
epochs = 2  # how many epochs to train for

loss_func = F.cross_entropy

MODEL_PATH = 'model.pt'


class Mnist_CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1)
        self.conv2 = nn.Conv2d(16, 16, kernel_size=3, stride=2, padding=1)
        self.conv3 = nn.Conv2d(16, 10, kernel_size=3, stride=2, padding=1)

    def forward(self, xb):
        xb = xb.view(-1, 1, 28, 28)
        xb = F.relu(self.conv1(xb))
        xb = F.relu(self.conv2(xb))
        xb = F.relu(self.conv3(xb))
        xb = F.avg_pool2d(xb, 4)
        return xb.view(-1, xb.size(1))

    def save(self, path):
        torch.save(self.state_dict(), path)
        print('model saved')


def loss_batch(model, loss_func, xb, yb, opt=None):
    loss = loss_func(model(xb), yb)

    if opt is not None:
        loss.backward()
        opt.step()
        opt.zero_grad()

    return loss.item(), len(xb)


def fit(epochs, model, loss_func, opt, train_dl, valid_dl):
    for epoch in range(epochs):
        model.train()
        for xb, yb in train_dl:
            loss_batch(model, loss_func, xb, yb, opt)

        model.eval()
        with torch.no_grad():
            losses, nums = zip(
                *[loss_batch(model, loss_func, xb, yb) for xb, yb in valid_dl]
            )
        val_loss = np.sum(np.multiply(losses, nums)) / np.sum(nums)

        print(epoch, val_loss)

        if (epoch + 1) % 2 == 0:
            model.save(path=MODEL_PATH)


def get_data(train_ds, valid_ds, bs):
    return (
        DataLoader(train_ds, batch_size=bs, shuffle=True),
        DataLoader(valid_ds, batch_size=bs * 2),
    )


if __name__ == '__main__':
    use_cuda = torch.cuda.is_available()

    if use_cuda:
        dev = torch.device('cuda')
        print('use GPU !!')
        print(f'device_count: {torch.cuda.device_count()}')
        print(f'current_device: {torch.cuda.current_device()}')
        print(f'get_device_name: {torch.cuda.get_device_name(0)}')
    else:
        torch.set_num_threads(4)

    x_train, y_train, x_valid, y_valid = get_mnist_data()

    x_train, y_train, x_valid, y_valid = map(
        torch.tensor, (x_train, y_train, x_valid, y_valid)
    )

    train_ds = TensorDataset(x_train, y_train)
    valid_ds = TensorDataset(x_valid, y_valid)

    train_dl, valid_dl = get_data(train_ds, valid_ds, bs)

    model = Mnist_CNN()
    if os.path.isfile(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()
        print('model loaded')

    if use_cuda:
        model = model.to(dev)

    opt = optim.SGD(model.parameters(), lr=lr, momentum=0.9)

    fit(epochs, model, loss_func, opt, train_dl, valid_dl)
