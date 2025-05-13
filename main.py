import sys
import os
import time
import numpy as np
import cv2
import yaml
import csv
import torch

from torchvision import models, transforms
from PIL import Image
from image.mask import mask
from image.crop import crop
from image.HSV_contours import contour_area
from measure import measure_width_height
from detect import detect_any_marker, detect_robot_in_pos, detect_marker_2, detect_robot_in_pos_l
from camera.camera_handler import init_camera, get_frame, release_camera

# Cesty
MODEL_PATH = "models/model.pth"
CLASS_NAMES = len(sorted(os.listdir("dataset/train")))  # počet tříd
CONFIG_YAML = "config.yaml"

# Načtení konfigurace
with open(CONFIG_YAML, 'r') as file:
    config = yaml.safe_load(file)

MASK1_HIGH = tuple(config['MASK1_HIGH'])
MASK1_LOW = tuple(config['MASK1_LOW'])
MASK2_HIGH = tuple(config['MASK2_HIGH'])
MASK2_LOW = tuple(config['MASK2_LOW'])
WAIT_TIME = config['WAIT_TIME']
COOLDOWN_AFTER_DETECTION = config['COOLDOWN_AFTER_DETECTION']
INDENTIFICATION = bool(config['IDENTIFICATION'])  
PX_TO_MM = config['PX_TO_MM']
CROP_WIDTH = config['CROP_WIDTH']
CROP_HEIGHT = config['CROP_HEIGHT']

def main():
    cooldown = 0
    init_camera()
    try:
        while True:
            if cooldown > 0:
                time.sleep(1)
                frame = get_frame()
                cv2.imwrite("latest.jpg", frame)
                cooldown -= 1
                continue
            if os.path.exists('latest.jpg'):
                os.remove('latest.jpg')
            frame = None
            time.sleep(1)
            frame = get_frame()
            cv2.imwrite("latest.jpg", frame)

            if frame is not None and detect_any_marker(frame):
                print("Marker nalezen")
                if detect_robot_in_pos(get_frame()):
                    print("Robot je v pozici, pokračuji s identifikací...")
                    x = 0
                    y = 0
                    x, y = detect_marker_2(get_frame())
                    if x == 0 and y == 0:
                        print("Marker 2 nenalezen, zkouším znovu...")
                        continue
                    #cv2.imwrite("crop_test.jpg", crop(get_frame(), crop_x_start=x, crop_y_start=y, crop_x_end=x+CROP_WIDTH, crop_y_end=y+CROP_HEIGHT)) # Testování Cropu
                    frame = mask(crop(get_frame(), crop_x_start=x, crop_y_start=y, crop_x_end=x+CROP_WIDTH, crop_y_end=y+CROP_HEIGHT), mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW)
                    # Uložení snímku do dumpu pro další trénování modelu
                    img_path = save_img_dump(frame)

                    # Identifikace objektu
                    if INDENTIFICATION:
                        result = identify(img_path)
                        if result is None:
                            print("Identifikace selhala.")
                        else:
                            # Spočítání plochy kontur pro další zpracování
                            area = contour_area(img_path, min_area=500, mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW)
                            print(f"Celková plocha kontur: {area}")
                            
                            # Změření výšky a šířky objektu
                            width, height = measure_width_height(img_path, min_area=500, mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW)
                            width = width / PX_TO_MM
                            height = height / PX_TO_MM
                            print(f"Šířka: {width} mm, Výška: {height} mm")
                            
                            # Měření délky objektu
                            in_pos_L = False
                            error = False
                            timeout = 0
                            while in_pos_L == False:
                                print("Čekám na délku.")
                                time.sleep(1)
                                if detect_robot_in_pos_l(crop(get_frame(), crop_x_start=x, crop_y_start=y, crop_x_end=x+CROP_WIDTH, crop_y_end=y+CROP_HEIGHT)):
                                    in_pos_L = True
                                else:
                                    timeout += 1
                                    if timeout == 20:
                                        in_pos_L = True
                                        error = True
                            if not error:
                                cv2.imwrite("length.jpg", crop(get_frame(), crop_x_start=x, crop_y_start=y, crop_x_end=x+CROP_WIDTH, crop_y_end=y+CROP_HEIGHT))
                                # Změření délky a výšky objektu
                                length, height_2 = measure_width_height("length.jpg", min_area=500, mask1_high=MASK1_HIGH, mask1_low=MASK1_LOW, mask2_high=MASK2_HIGH, mask2_low=MASK2_LOW)
                                length = length / PX_TO_MM
                                height_2 = height_2 / PX_TO_MM
                                print(f"Délka: {length} mm, Výška 2: {height_2} mm")
                                
                                #final_id = classify(
                                #    input_object=result,
                                #    input_width=width,
                                #    input_length=length
                                #)
                                #print(final_id)

                                # Uložení výsledků do CSV souboru
                                data = [img_path[13:],result , round(length,0), round(width,0), round(height,0), round(height_2,0), area]
                                with open("logs.csv", "a", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow(data)
                                    
                                # Přejmenování snímku podle výsledku identifikace
                                # if len(final_id) == 1:
                                #     new_img_path = f"{img_path[:13]}{result}--{img_path[13:]}"
                                #     print(f"Identifikace se zdařila: {final_id}")
                                # elif len(final_id) == 0:
                                #     new_img_path = f"{img_path[:13]}00--{img_path[13:]}"
                                #     print("Identifikace se nezdařila.")
                                # else:
                                #     str_final_id = "_".join(map(str, final_id))
                                #     new_img_path = f"{img_path[:13]}{result}--{img_path[13:]}"
                                #     print(f"Identifikace se nezdařila: {str_final_id}")
                                
                                new_img_path = f"{img_path[:13]}{result}--{img_path[13:]}"
                                os.rename(img_path, new_img_path)
                                print(f"Snímek přejmenován na {new_img_path[13:]}.")
                            else:
                                print("Identifikace délky se nezdařila. Timeout")
                    else:
                        # Uložení snímku do dumpu bez identifikace
                        print("Identifikace je vypnuta, ukládám snímek do dumpu...")
                    
                    # Cooldown po detekci markeru
                    print("Detekce dokončena, čekám 60 sekund na další detekci...")
                    cooldown = COOLDOWN_AFTER_DETECTION
                    frame = None
                    if os.path.exists('latest.jpg'):
                        os.remove('latest.jpg')
                    continue
            else:
                time.sleep(WAIT_TIME)
                print("Marker nenalezen, zkusím znovu za 2 sekundy...")
                
    except KeyboardInterrupt:
        print("Ukončuji...")
    finally:
        release_camera()


def identify(img_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_NAMES))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
    model.eval()
    image = Image.open(img_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = output.max(1)
        class_idx = predicted.item()
        class_name = CLASS_NAMES[class_idx]

    print(f"Predikovaná třída: {class_name}")
    return int(class_name)

def classify(input_object, input_width, input_length):
    objects = {}
    threshold = 15
    with open('objects.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            detect_id = int(row['detect_id'])
            item_id = int(row['item_id'])
            try:
                width = int(row['width'])
            except TypeError:
                width = 0
            try:
                length = int(row['length'])
            except TypeError:
                length = 0
            trafo = {"object":detect_id,"width":width,"length":length}
            objects[item_id]=trafo
            
    # find items based on length
    out_length = []
    for item_id, measures in objects.items():
        if abs(measures["length"] - input_length) <= threshold:
            out_length.append(item_id)
    # find items based on width
    out_width = []
    for item_id, measures in objects.items():
        if abs(measures["width"] - input_width) <= threshold:
            out_width.append(item_id)
    # find items based on detection
    out_detection = []
    for item_id, measures in objects.items():
        if measures["object"] == input_object:
            out_detection.append(item_id)
    # find items that are in both lists: out_length and out_width
    based_on_dimensions = []
    for item_id, measures in objects.items():
        if item_id in out_length and item_id in out_width:
            based_on_dimensions.append(item_id)
    #return based_on_dimensions
    if len(based_on_dimensions) == 1:
        return based_on_dimensions[0]
    else:
        # find items that are in both lists: based_on_detection and out_detection
        id = []
        for item_id, measures in objects.items():
            if item_id in based_on_dimensions and item_id in out_detection:
                id.append(item_id)
        return id
    
def save_img_dump(frame=None):
    # Uložení snímku pro další zpracování do dataset/dump/YYMMDD_hhmmss.jpg
    if frame is None:
        print("Žádný snímek.")
        return 
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("dataset", "dump", f"{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Snímek uložen jako {filename}.")
    return filename
    


if __name__ == "__main__":
    main()
