import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.ndimage import zoom
import os
# ----- CNN 模型 -----
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64*7*7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = self.pool(x)
        x = nn.functional.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(-1, 64*7*7)
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# ----- 数据 -----
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.5,), (0.5,))])
trainset = torchvision.datasets.MNIST(root="./mnist_data", train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

# ----- 初始化模型 -----
model = CNN()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

# ----- 加载或训练 -----
if os.path.exists('cnn_mnist.pth'):
    model.load_state_dict(torch.load('cnn_mnist.pth'))
    model.eval()
    print("已加载训练好的模型，跳过训练。")
else:
    print("开始训练模型（大约需要几分钟）…")
    best_loss = float('inf')
    epochs = 10  # 增加轮数让 loss 降低
    for epoch in range(epochs):
        running_loss = 0.0
        for imgs, labels in trainloader:
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        epoch_loss = running_loss / len(trainloader)
        print(f"Epoch {epoch+1}, loss={epoch_loss:.4f}")
        if epoch_loss < best_loss:
            best_loss = epoch_loss
            torch.save(model.state_dict(), 'cnn_mnist.pth')
    model.eval()
    print(f"训练完成，最小 loss={best_loss:.4f}，模型已保存到 cnn_mnist.pth")

# ----- 画板逻辑 -----
canvas_size = 50
canvas = np.zeros((canvas_size, canvas_size))
drawing = False

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
im = ax.imshow(canvas, cmap='gray', vmin=0, vmax=1)
ax.set_xlim(0, canvas_size)
ax.set_ylim(canvas_size, 0)
ax.set_xticks([])
ax.set_yticks([])

def on_press(event):
    global drawing
    if event.inaxes != ax:
        return
    drawing = True
    draw(event)

def on_release(event):
    global drawing
    drawing = False

def on_motion(event):
    if drawing:
        draw(event)

def draw(event):
    # 只允许在画布区域画
    if event.inaxes != ax:
        return

    if event.xdata is None or event.ydata is None:
        return

    x = int(np.clip(event.xdata, 0, canvas_size-1))
    y = int(np.clip(event.ydata, 0, canvas_size-1))

    brush_size = 2

    x0 = max(0, x - brush_size)
    x1 = min(canvas_size, x + brush_size + 1)
    y0 = max(0, y - brush_size)
    y1 = min(canvas_size, y + brush_size + 1)

    canvas[y0:y1, x0:x1] = 1

    im.set_data(canvas)
    fig.canvas.draw_idle()

def predict_digit(event=None):
    small = zoom(canvas, (28/canvas_size, 28/canvas_size), order=1)
    small = small.reshape(1, 1, 28, 28)
    tensor = torch.tensor(small).float()
    tensor = (tensor - 0.5) / 0.5
    with torch.no_grad():
        outputs = model(tensor)
        pred = torch.argmax(outputs).item()
    ax.set_title(f"AI: {pred}")
    fig.canvas.draw_idle()

def clear(event):
    global canvas
    canvas = np.zeros((canvas_size, canvas_size))

    im.set_data(canvas)
    ax.set_title("AI: ?")
    fig.canvas.draw_idle()

# ----- 按钮 -----
axclear = plt.axes([0.8, 0.05, 0.1, 0.075])
btn_clear = Button(axclear, 'Clear')
btn_clear.on_clicked(clear)

axdetect = plt.axes([0.65, 0.05, 0.1, 0.075])
btn_detect = Button(axdetect, 'Detect')
btn_detect.on_clicked(predict_digit)

# ----- 绑定事件 -----
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()