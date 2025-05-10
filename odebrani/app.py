import cv2
import numpy as np
import json
import math
from snap import take_snapshot
from aruco import find_qr, home_pos, distance_qr

def main():
    while True:
        user_input = input("1-SnapShot 2-CalibrateHomePos: 3-3QR 4-4QR")
        if user_input == "1":
            take_snapshot()
        elif user_input == "2":
            home_pos()
        elif user_input == "3":
            distance_qr(3)
        elif user_input == "4":
            distance_qr(4)
        else:
            print("Chyba!")

if __name__ == "__main__":
    main()