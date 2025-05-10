import cv2
from snap import take_snapshot
import json
import numpy as np
import math
import time

def main():
    find_qr()

def load_calibration():
    # === Načti kalibraci ===
    try:
        with open("calibration.json", "r") as f:
            calib = json.load(f)
            pixel_per_mm = calib["pixel_per_mm"]
    except Exception as e:
        print(f"[ERROR] Nelze načíst kalibraci: {e}")
        exit()
    return pixel_per_mm

def find_qr():
    pixel_per_mm = load_calibration()
    # Načtení fotky
    take_snapshot()
    image = cv2.imread('snap.jpg')

    # Převedení na šedotónový obrázek
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Nastavení ArUco detekce
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # Detekce značek
    corners, ids, _ = detector.detectMarkers(gray)

    # Zobrazení výsledků
    qr = {}
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
        for i, corner in enumerate(corners):
            top_left = corner[0][0]  # levý horní roh
            x, y = int(top_left[0]), int(top_left[1])
            marker_id = ids[i][0]
            print(f"ID: {marker_id} -> Levý horní roh: ({x}, {y})")
            qr[f'{marker_id}'] = {'x': x, 'y': y}
    else:
        print("Žádné ArUco značky nenalezeny.")

    cv2.imwrite('output.jpg', image)
    print("Uložen output.jpg")
    #cv2.imshow('Detekované ArUco značky', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return qr, image

def home_pos():
    qr, image = find_qr()
    if "3" in qr and "4" in qr:
        with open("home_pos.json", "w") as f:
            json.dump({
                "3": qr["3"],
                "4": qr["4"]
            }, f, indent=2)
    else:
        print("Potřebuji vidět QR 3 i 4.")


def distance_qr(pas):
    pixel_per_mm = load_calibration()
    qr, image = find_qr()
    qr_3 = {}
    qr_4 = {}
    if "3" in qr and "4" in qr:
        try:
            with open("home_pos.json", "r") as f:
                home = json.load(f)
                qr_3 = home["3"]
                qr_4 = home["4"]
        except Exception as e:
            print(f"[ERROR] Nelze načíst home pozici: {e}")
        if not pas:
            print("Vyber pas")
        elif pas == 3:
            home_x = qr_3['x']
            home_y = qr_3['y']
            x = qr['3']['x']
            y = qr['3']['y']
            dx = x - home_x
            dy = y - home_y
            distance_pixels = math.sqrt(dx**2 + dy**2)
            distance_mm = distance_pixels / pixel_per_mm
            distance_mm = round(distance_mm, 1)
            print(f"[INFO] ID: 3 -> ({x}, {y}) -> {distance_mm:.1f} mm")
            # Vykreslení
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
            cv2.circle(image, (home_x, home_y), 5, (255, 0, 0), -1)
            cv2.putText(image, f"{distance_mm}mm", (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(image, f"Home pos", (home_x + 10, home_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.line(image, (home_x, home_y), (x, y), (255, 255, 255), 1)
        elif pas == 4:
            home_x = qr_4['x']
            home_y = qr_4['y']
            x = qr['4']['x']
            y = qr['4']['y']
            dx = x - home_x
            dy = y - home_y
            distance_pixels = math.sqrt(dx**2 + dy**2)
            distance_mm = distance_pixels / pixel_per_mm
            distance_mm = round(distance_mm, 1)
            print(f"[INFO] ID: 4 -> ({x}, {y}) -> {distance_mm:.1f} mm")
            # Vykreslení
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
            cv2.circle(image, (home_x, home_y), 5, (255, 0, 0), -1)
            cv2.putText(image, f"{distance_mm}mm", (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(image, f"Home pos", (home_x + 10, home_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.line(image, (home_x, home_y), (x, y), (255, 255, 255), 1)
        cv2.imwrite('distance.jpg', image)
    else:
        print("QR 3 OR QR 4 missing")
    return

        


if __name__ == "__main__":
    main()