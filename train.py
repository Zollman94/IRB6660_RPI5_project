import os
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torchvision import models
from torch import nn, optim
from torch.utils.data import DataLoader

# === PARAMETRY ===
DATA_DIR = "dataset/train"
NUM_CLASSES = len(sorted(os.listdir("dataset/train")))  # ["0", "1", ..., "13"]
BATCH_SIZE = 8
NUM_EPOCHS = 25
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === TRANSFORMACE ===
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# === DATASET ===
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# === MODEL ===
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model = model.to(DEVICE)

# === OPTIMALIZÁTOR A LOSS ===
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# === TRÉNINK ===
for epoch in range(NUM_EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    acc = 100 * correct / total
    print(f"Epoch {epoch+1}/{NUM_EPOCHS}, Loss: {running_loss:.4f}, Accuracy: {acc:.2f}%")

# === ULOŽENÍ MODELU ===
torch.save(model.state_dict(), "model.pth")
print("Model uložen do model.pth")