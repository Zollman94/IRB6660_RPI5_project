import cv2
import time

cap = None
CAMERA_INDEX = 0
RECONNECT_DELAY = 2  # sekundy

def init_camera():
    global cap
    if cap is not None:
        cap.release()

    print("[KAMERA] Inicializuji kameru...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if cap.isOpened():
        print("[KAMERA] Kamera úspěšně otevřena.")
    else:
        print("[KAMERA] Nelze otevřít kameru!")

def get_frame():
    global cap
    if cap is None or not cap.isOpened():
        print("[KAMERA] Kamera není připojena. Pokouším se znovu připojit...")
        init_camera()
        time.sleep(RECONNECT_DELAY)
        return None

    ret, frame = cap.read()
    if not ret:
        print("[KAMERA] Chyba při čtení snímku.")
        return None

    return frame

def release_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None
        print("[KAMERA] Kamera uvolněna.")
