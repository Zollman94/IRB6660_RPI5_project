import cv2
import numpy as np
import time
import yaml

# Načti YAML soubor
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Definice rozsahu pro maskování
MASK1_HIGH = tuple(config['MASK1_HIGH'])
MASK1_LOW = tuple(config['MASK1_LOW'])
MASK2_HIGH = tuple(config['MASK2_HIGH'])
MASK2_LOW = tuple(config['MASK2_LOW'])

def contour_area(image_path, min_area=1000, mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW):
    img = cv2.imread(image_path)

    # Převod obrázku do HSV prostoru
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Vytvoření masky podle definovaných HSV rozsahů
    #mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    mask1 = cv2.inRange(hsv, mask1_high, mask1_low)
    mask2 = cv2.inRange(hsv, mask2_high, mask2_low)
    mask_combined = mask1 + mask2

    # Najít kontury v masce
    contours, _ = cv2.findContours(mask_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrace kontur podle minimální velikosti
    large_contours = []  # Seznam pro velké kontury
    sum_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        # Pokud je kontura dostatečně velká, přidej ji do seznamu
        if area > min_area:
            large_contours.append(contour)
            sum_area += area
    #draw_contours(large_contours, img)
    return sum_area


def draw_contours(large_contours, img):
    # Pro nakreslení kontur na obrázku
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # Pro nakreslení kontur na obrázku
    img_contours = cv2.drawContours(img.copy(), large_contours, -1, (0, 255, 0), 3)

    cv2.imwrite(f"dataset/contours/{timestamp}.jpg", img_contours)

