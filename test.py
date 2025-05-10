import sys
import os
import time

import numpy as np
import cv2
import yaml

from image.mask import mask
from image.crop import crop
from image.identify import identify
from image.HSV_contours import contour_area
from image.height_widht import measure_width_height
from image.detect_marker import detect_any_marker, detect_robot_in_pos, detect_marker_2, detect_robot_in_pos_l
from camera.camera_handler import init_camera, get_frame, release_camera
from id import id

# Načti YAML soubor
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Definice rozsahu pro maskování
MASK1_HIGH = tuple(config['MASK1_HIGH'])
MASK1_LOW = tuple(config['MASK1_LOW'])
MASK2_HIGH = tuple(config['MASK2_HIGH'])
MASK2_LOW = tuple(config['MASK2_LOW'])

# Nastavení
WAIT_TIME = config['WAIT_TIME']
COOLDOWN_AFTER_DETECTION = config['COOLDOWN_AFTER_DETECTION']
OBJECTS = config['OBJECTS']
INDENTIFICATION = bool(config['IDENTIFICATION'])  # Pokud je True, provede se identifikace objektu jinak se pouze maskuje a ukládá snímek do dumpu
PX_TO_MM = config['PX_TO_MM']  # Převodník px na mm
CROP_WIDTH = config['CROP_WIDTH']  # Šířka ořezu
CROP_HEIGHT = config['CROP_HEIGHT']  # Výška ořezu

def main():
    cooldown = 0
    init_camera()
    try:
        while True:
            if cooldown > 0:
                time.sleep(1)
                cooldown -= 1
                continue

            frame = get_frame()
            save_img_dump(frame)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Ukončuji...")
    finally:
        release_camera()

def main2():
    return False
    while True:
        frame = get_frame()
        time.sleep(5)
        print("Spouštím...")
        frame = crop(get_frame(), crop_x_start=x, crop_y_start=y, crop_x_end=x+CROP_WIDTH, crop_y_end=y+CROP_HEIGHT)
        cv2.imwrite("latest.jpg", frame)
        time.sleep(5)
        detect_robot_in_pos_l(frame)
        print("Konec")
        pass

def main3():
    result = 0
    img_path = 'dataset/dump/20250509_093651.jpg'
    print(f"{img_path[:13]}{result}__{img_path[13:]}")

def save_img_dump(frame=None):
    # Uložení snímku pro další zpracování do dataset/dump/YYMMDD_hhmmss.jpg
    if frame is None:
        print("Žádný snímek.")
        return 
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("webserver", "static", "latest.jpg")
    cv2.imwrite(filename, frame)
    print(f"Snímek uložen jako {filename}.")
    return filename

if __name__ == "__main__":
    main3()