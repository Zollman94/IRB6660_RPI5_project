import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import shutil

# Počet tříd
programs = 11
class_names = [str(i) for i in range(programs)]

# Vždy CPU (ARM ready)
device = torch.device("cpu")
print(f"Používám zařízení: {device}")

# Načtení modelu
model = torch.jit.load("model_scripted.pt", map_location=device)
model.eval()

# Transformace
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def transform_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)

# Složky
input_folder = "dump"
output_base = "sorted"

# Zajisti, že výstupní složky existují
for cls in class_names:
    os.makedirs(os.path.join(output_base, cls), exist_ok=True)

# Detekuj a třiď
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".jpg"):
        image_path = os.path.join(input_folder, filename)
        image_tensor = transform_image(image_path).to(device)

        with torch.no_grad():
            outputs = model(image_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            _, predicted_class = torch.max(probs, 1)

        target_class = class_names[predicted_class]
        target_dir = os.path.join(output_base, target_class)
        shutil.move(image_path, os.path.join(target_dir, filename))