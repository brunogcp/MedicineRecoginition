import multiprocessing
import time

import cv2
import numpy as np
from pyzbar.pyzbar import decode

URL = 'http://192.168.1.101:8080'
vs = cv2.VideoCapture(URL + "/video")

with open('myDataFile.txt') as file:
    myDataList = file.read().splitlines()


def func(number):
    for i in range(1, 6):
        time.sleep(1)
        print('Processing ' + str(number) + ': prints ' + str(number * i))


def bar_decode():
    count = 0
    while True:
        ret, frame = vs.read()
        frame_copy = frame.copy()
        if not ret:
            continue
        fps = vs.get(cv2.CAP_PROP_FPS)
        barcode = None
        for barcode in decode(frame):
            count += 1
            # print(barcode.data)
            myData = barcode.data.decode('utf-8')
            #print(myData)
            #print(count)

            myOutput = 'Scanning'
            myColor = (0, 255, 255)

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(frame, myOutput, (pts2[0], pts2[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)
            cv2.putText(frame, str(count), (pts2[0], pts2[1] - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

            if myData in myDataList:
                myOutput = 'Authorized'
                myColor = (0, 255, 0)
            else:
                myOutput = 'Un-Authorized'
                myColor = (0, 0, 255)

        if not barcode:
            count = 0
        if count >= fps / 2:
            frame = frame_copy.copy()
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(frame, myOutput, (pts2[0], pts2[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)
            cv2.putText(frame, str(count), (pts2[0], pts2[1] - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

            print(myData)
            if myData == '3662042000331':
                medicine = 'Hyabak'
            elif myData == '7896676432909':
                medicine = 'Flutinol'
            elif myData == '7896676432817':
                medicine = 'Maxiflox-D'
            else:
                medicine = 'Unknow'

            cv2.putText(frame, medicine, (pts2[0], pts2[1] - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)
            break

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
    cv2.imshow('Frame', frame)


if __name__ == '__main__':
    bar_decode()
    while True:
        if cv2.waitKey(0) & 0xFF == ord('r'):
            bar_decode()
        else:
            exit()
