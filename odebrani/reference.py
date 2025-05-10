import cv2
import json
import math
import numpy as np
import time
from snap_win import take_snapshot


calibration_file = "calibration.json"
image_path = "snap.jpg"
points = []

def main():
    take_snapshot()
    img = cv2.imread(image_path)
    cv2.imshow("Kalibrace", img)
    cv2.setMouseCallback("Kalibrace", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Kalibrace", img)

        if len(points) == 1:
            print(f"[INFO] Vybraný výchozí bod: {points[0]}")
        elif len(points) == 2:
            # Výpočet vzdálenosti v pixelech
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
            pixel_distance = math.sqrt(dx**2 + dy**2)

            # Přepočet na pixely na mm (500 mm je známá délka)
            pixel_per_mm = pixel_distance / 500.0
            print(f"[INFO] Kalibrace hotová: {pixel_per_mm:.4f} pixelů na mm")

            # Uložení dat do JSON
            data = {
                "pixel_per_mm": pixel_per_mm,
                "reference_point": points[0]
            }

            with open(calibration_file, "w") as f:
                json.dump(data, f)

            print(f"[INFO] Kalibrace uložena do {calibration_file}")
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

