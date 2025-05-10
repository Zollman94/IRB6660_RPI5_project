import cv2

def detect_aruco_dictionary(image_path="snap.jpg"):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dicts_to_test = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    }

    for name, dict_type in dicts_to_test.items():
        aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)
        parameters = cv2.aruco.DetectorParameters()
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if ids is not None and len(ids) > 0:
            print(f"Detekováno: {name}, ID: {ids.flatten().tolist()}")
            return name, ids.flatten().tolist()

    print("Žádné značky detekovány.")
    return None, []

if __name__ == "__main__":
    image_path = "snap.jpg"  # Zde zadejte cestu k obrázku
    detect_aruco_dictionary(image_path)