import cv2

# RTSP adresa kamery (nahraď podle své kamery)
rtsp_url = "rtsp://192.168.50.121:36065/eb17b5716a35c880?rtsp_transport=tcp"

# Použij dictionary (4x4_50 je dobrý pro vzdálenosti)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
parameters = cv2.aruco.DetectorParameters()

# Vytvoření detektoru
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Otevření RTSP streamu
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Nepodařilo se otevřít RTSP stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Chyba při čtení snímku.")
        break

    # Detekce ArUco značek
    corners, ids, rejected = detector.detectMarkers(frame)

    # Vykreslení značek
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # Zobrazení náhledu
    cv2.imshow("Aruco Detekce", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
