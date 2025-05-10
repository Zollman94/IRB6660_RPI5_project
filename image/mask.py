import cv2
import os
from pathlib import Path
import numpy as np
import yaml

root_dir = "dataset/dump" # Cesta ke kořenové složce objektů
min_area=1000  # Minimální plocha kontury pro zahrnutí

# Načti YAML soubor
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Definice rozsahu pro maskování
MASK1_HIGH = tuple(config['MASK1_HIGH'])
MASK1_LOW = tuple(config['MASK1_LOW'])
MASK2_HIGH = tuple(config['MASK2_HIGH'])
MASK2_LOW = tuple(config['MASK2_LOW'])


def main():
    pass

def mask(img=None, img_path='input.jpg', rewrite=False, mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW, min_area=min_area):
    if img is None:
        # Načtení obrázku
        img = cv2.imread(img_path)

    if img is None:
        print(f"❗ Soubor nejde načíst: {img_path}")
        return None
    
    # Převod obrázku do HSV prostoru
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    mask1 = cv2.inRange(hsv, mask1_high, mask1_low)
    mask2 = cv2.inRange(hsv, mask2_high, mask2_low)
    mask_combined = mask1 + mask2

    # Najít kontury v masce
    contours, _ = cv2.findContours(mask_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filtrace kontur podle minimální velikosti
    large_contours = []  # Seznam pro velké kontury

    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Pokud je kontura dostatečně velká, přidej ji do seznamu
        if area > min_area:
            large_contours.append(contour)

    # Pro nakreslení kontur na obrázku
    img_contours = img.copy()

    for contour in large_contours:
        # Získání obdélníku, který obklopuje konturu
        x, y, w, h = cv2.boundingRect(contour)
        
        # Kreslení obdélníku na obrázku
        cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Vytvoření masky pro vybranou oblast mimo bounding boxu
        mask = np.zeros_like(img)
        mask[y:y+h, x:x+w] = img[y:y+h, x:x+w]
        img = cv2.bitwise_and(img, mask)

    print(f"✅ Maska aplikována")
    if rewrite:
        cv2.imwrite(img_path, img)
    return img

def mask_all(root_dir=root_dir, mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW):
    # Procházení všech jpg souborů ve všech podadresářích
    for img_path in Path(root_dir).rglob("*.jpg"):
        img_path = str(img_path)
        img = cv2.imread(img_path)

        if img is None:
            print(f"❗ Soubor nejde načíst: {img_path}")
            continue
        
        # Převod obrázku do HSV prostoru
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

        mask1 = cv2.inRange(hsv, mask1_high, mask1_low)
        mask2 = cv2.inRange(hsv, mask2_high, mask2_low)
        mask_combined = mask1 + mask2
        # Najít kontury v masce
        contours, _ = cv2.findContours(mask_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filtrace kontur podle minimální velikosti
        large_contours = []  # Seznam pro velké kontury

        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Pokud je kontura dostatečně velká, přidej ji do seznamu
            if area > min_area:
                large_contours.append(contour)

        # Pro nakreslení kontur na obrázku
        img_contours = img.copy()

        for contour in large_contours:
            # Získání obdélníku, který obklopuje konturu
            x, y, w, h = cv2.boundingRect(contour)
            
            # Kreslení obdélníku na obrázku
            cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Vytvoření masky pro vybranou oblast mimo bounding boxu
        mask = np.zeros_like(img)
        mask[y:y+h, x:x+w] = img[y:y+h, x:x+w]
        img = cv2.bitwise_and(img, mask)

        cv2.imwrite(img_path, img)
        print(f"✅ Maska aplikována: {img_path}")



if __name__ == "__main__":
    main()