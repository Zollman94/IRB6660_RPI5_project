import cv2
import yaml
import time
import math
from camera.camera_handler import init_camera, get_frame, release_camera

def calibrate():
    init_camera()
    for i in range(10):
        time.sleep(2)
        image = get_frame()
        cv2.imwrite("latest.jpg", image)
        print(f"Načítám snímek {i+1}/10")
    # Převedení na šedotónový obrázek
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Nastavení ArUco detekce
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # Detekce značek
    corners, ids, _ = detector.detectMarkers(gray)
    img_marker = image.copy()
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
            cv2.circle(img_marker, (x, y), 5, (255, 0, 0), -1)
            cv2.putText(img_marker, f"{marker_id}", (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    else:
        print("Žádné ArUco značky nenalezeny.")
    cv2.imwrite('markers.jpg', img_marker)

    if "17" in qr and "18" in qr:
        # Vypočti vzdálenost v pixelech
        dx = qr["18"]["x"] - qr["17"]["x"]
        dy = qr["18"]["y"] - qr["17"]["y"]
        pixel_distance = math.sqrt(dx**2 + dy**2)
        scale = pixel_distance / 210.0

        print(f"[INFO] Kalibrace hotová: {scale:.4f} pixelů na mm")

        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        config['PX_TO_MM'] = scale
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
        print(f"[INFO] Uloženo do config.yaml")
        return True
    else:
        print("Nedetekován marker 17 a 18.")
    return False

if __name__ == "__main__":
    if calibrate():
        print("Kalibrace úspěšná.")
    else:
        print("Kalibrace selhala.")
    release_camera()