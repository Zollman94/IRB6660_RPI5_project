import cv2
import json
import math
from snap import take_snapshot

calibration_file = "calibration.json"
image_path = "snap.jpg"

points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Kalibrace", img)

        if len(points) == 2:
            # Vypočti vzdálenost v pixelech
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
            pixel_distance = math.sqrt(dx**2 + dy**2)

            scale = pixel_distance / 200.0
            print(f"[INFO] Kalibrace hotová: {scale:.4f} pixelů na mm")

            # Ulož do souboru
            with open(calibration_file, "w") as f:
                json.dump({"pixel_per_mm": scale}, f)
            print(f"[INFO] Uloženo do {calibration_file}")

            cv2.destroyAllWindows()

# Načti obrázek
img = cv2.imread(image_path)
cv2.imshow("Kalibrace", img)
cv2.setMouseCallback("Kalibrace", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
