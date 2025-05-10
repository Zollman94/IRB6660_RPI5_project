import cv2
import os
from pathlib import Path

# Parametry střihu
crop_y_start = 100 # Y souřadnice začátku ořezu
crop_y_end = 720 # Y souřadnice konce ořezu
crop_x_start = 350 # X souřadnice začátku ořezu
crop_x_end = 1100 # X souřadnice konce ořezu
base_size = (1280, 720)  # Rozměry necropnuté fotky

# Cesta ke kořenové složce objektů
root_dir = "dataset/dump"

def main():
    # Oříznout všechny obrázky
    if input(f"Oříznout všechny obrázky ve složce {root_dir}? (a/n): ").lower() == 'a':
        crop_all(root_dir, crop_y_start, crop_y_end, crop_x_start, crop_x_end, base_size)
    else:
        crop(img_path='latest.jpg')

def crop_all(root_dir='dump', crop_y_start=crop_y_start, crop_y_end=crop_y_end, crop_x_start=crop_x_start, crop_x_end=crop_x_end, base_size=base_size):
    # Procházení všech jpg souborů ve všech podadresářích
    for img_path in Path(root_dir).rglob("*.jpg"):
        img_path = str(img_path)
        img = cv2.imread(img_path)

        if img is None:
            print(f"❗ Soubor nejde načíst: {img_path}")
            continue

        h, w = img.shape[:2]

        # Kontrola, jestli je to necropnutá fotka
        if (h, w) == base_size:
            cropped_img = img[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

            # Přepsat původní soubor (POZOR: smažeš originál!)
            cv2.imwrite(img_path, cropped_img)
            print(f"✅ Oříznuto: {img_path}")

        else:
            print(f"➡️ Přeskočeno (už oříznuté nebo jiné rozlišení): {img_path}")

def crop(img=None, img_path='input.jpg', crop_y_start=crop_y_start, crop_y_end=crop_y_end, crop_x_start=crop_x_start, crop_x_end=crop_x_end, rewrite=False):
    if img is None:
        # Načtení obrázku  
        img = cv2.imread(img_path)
    if img is None:
        print(f"❗ Soubor nejde načíst: {img_path}")
        return None

    cropped_img = img[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

    # Přepsat původní soubor (POZOR: smažeš originál!)
    print(f"✅ Oříznuto")
    if rewrite:
        cv2.imwrite(img_path, cropped_img)
    return cropped_img

            
if __name__ == "__main__":
    main()
