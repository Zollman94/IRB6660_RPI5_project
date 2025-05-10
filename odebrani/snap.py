import cv2
import time

def main():
    take_snapshot()

def take_snapshot():
    # Otevře první připojenou kameru (0 je výchozí kamera)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

    # Zkontroluj, že kamera se otevřela
    if not cap.isOpened():
        print("Nelze otevřít kameru")
        exit()
    for _ in range(20):
        cap.read()
        time.sleep(0.05)  # malá pauza, aby se expozice stihla dopočítat
    ret, frame = cap.read()

    if ret:
        # Ulož snapshot
        cv2.imwrite("snap.jpg", frame)
        #frame_yuyv = frame  # původní snímek
        #frame_bgr = cv2.cvtColor(frame_yuyv, cv2.COLOR_YUV2BGR_YUY2)
        #cv2.imwrite("snapshot.jpg", frame_bgr)
        print("Snapshot uložen jako snapshot.jpg")
    else:
        print("Nepodařilo se získat snímek")
    cap.release()

if __name__ == "__main__":
    main()
