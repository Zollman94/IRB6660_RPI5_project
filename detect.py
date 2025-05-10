import cv2
import yaml

def detect_any_marker(image=None):
    if image is None:
        try:
            print("Načítám input.jpg")
            image = cv2.imread("input.jpg")
        except Exception as e:
            print(f"Chyba při načítání obrázku: {e}")
            return False

    # Převedení na šedotónový obrázek
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Nastavení ArUco detekce
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # Detekce značek
    corners, ids, _ = detector.detectMarkers(gray)

    return True if ids is not None else False

def detect_robot_in_pos(image=None):
    if image is None:
        try:
            print("Načítám input.jpg")
            image = cv2.imread("input.jpg")
        except Exception as e:
            print(f"Chyba při načítání obrázku: {e}")
            return False

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
    if "2" in qr:
        # Načti YAML soubor
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        x = config['ROBOT_IN_POS']['X']
        y = config['ROBOT_IN_POS']['Y']
        threshold = config['ROBOT_IN_POS']['THRESHOLD']
        # Zkontroluj, zda je robot v pozici
        if abs(qr["2"]['x'] - x) < threshold and abs(qr["2"]['y'] - y) < threshold:
            print("Robot je v pozici.")
            return True
        else:
            print("Robot není v pozici.")
            return False
    else:
        print("Nedetekován marker 2.")
    return False
        
def detect_marker_2(image=None):
    if image is None:
        try:
            print("Načítám input.jpg")
            image = cv2.imread("input.jpg")
        except Exception as e:
            print(f"Chyba při načítání obrázku: {e}")
            return False

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
    if "2" in qr:
        # Načti YAML soubor
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        x = config['ROBOT_IN_POS']['X']
        y = config['ROBOT_IN_POS']['Y']
        threshold = config['ROBOT_IN_POS']['THRESHOLD']
        # Zkontroluj, zda je robot v pozici
        if abs(qr["2"]['x'] - x) < threshold and abs(qr["2"]['y'] - y) < threshold:
            print("Robot je v pozici. Vracím souřadnice pro crop.")
            return qr["2"]['x'], qr["2"]['y']
        else:
            print("Robot není v pozici.")
            return 0, 0
    else:
        print("Nedetekován marker 2.")
    return 0, 0

def detect_robot_in_pos_l(image=None):
    if image is None:
        try:
            print("Načítám input.jpg")
            image = cv2.imread("input.jpg")
        except Exception as e:
            print(f"Chyba při načítání obrázku: {e}")
            return False

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
    if "1" in qr:
        # Načti YAML soubor
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        x = config['ROBOT_IN_POS_L']['X']
        y = config['ROBOT_IN_POS_L']['Y']
        threshold = config['ROBOT_IN_POS_L']['THRESHOLD']
        # Zkontroluj, zda je robot v pozici
        if abs(qr["1"]['x'] - x) < threshold and abs(qr["1"]['y'] - y) < threshold:
            print("Robot je v pozici.")
            return True
        else:
            print("Robot není v pozici.")
            return False
    else:
        print("Nedetekován marker 1.")
    return False

if __name__ == "__main__":
    pass