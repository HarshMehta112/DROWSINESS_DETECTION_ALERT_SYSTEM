##########################################################################################

                # DROWSINESS-DETECTION & ALERT SYSTEM
                # CODE BY HARSH MEHTA
                # Github :- https://github.com/HarshMehta112/

##########################################################################################

import cv2
import pyglet.media
import math
from cvzone.FaceMeshModule import FaceMeshDetector

def findDistance(p1, p2):

    x1, y1 = p1
    x2, y2 = p2
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)
    info = (x1, y1, x2, y2, cx, cy)
    return length,info

def alert():
    cv2.rectangle(img, (700, 20), (1250, 80), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "DROWSINESS ALERT!!!", (710, 60),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)


cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)

breakcount_s, breakcount_y = 0, 0
counter_s, counter_y = 0, 0
state_s, state_y = False, False

sound = pyglet.media.load("alarm.wav", streaming=False)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        eyeLeft = [27, 23, 130, 243]  # up, down, left, right
        eyeRight = [257, 253, 463, 359]  # up, down, left, right
        mouth = [11, 16, 57, 287]  # up, down, left, right
        faceId = [27, 23, 130, 243, 257, 253, 463, 359, 11, 16, 57, 287] # All Points

        # calculate eye left distance ratio

        eyeLeft_ver, _ = findDistance(face[eyeLeft[0]], face[eyeLeft[1]])
        eyeLeft_hor, _ = findDistance(face[eyeLeft[2]], face[eyeLeft[3]])
        eyeLeft_ratio = int((eyeLeft_ver/eyeLeft_hor) * 100)

        # calculate eye right distance ratio

        eyeRight_ver, _ = findDistance(face[eyeRight[0]], face[eyeRight[1]])
        eyeRight_hor, _ = findDistance(face[eyeRight[2]], face[eyeRight[3]])
        eyeRight_ratio = int((eyeRight_ver / eyeRight_hor) * 100)

        # calculate mouth distance ratio

        mouth_ver, _ = findDistance(face[mouth[0]], face[mouth[1]])
        mouth_hor, _ = findDistance(face[mouth[2]], face[mouth[3]])
        mouth_ratio = int((mouth_ver / mouth_hor) * 100)

        # display text on image

        print(f'Eye Left Ratio: {eyeLeft_ratio}')
        print(f'Eye Right Ratio: {eyeRight_ratio}')
        # print(f'Eye Mouth Ratio: {mouth_ratio}')

        cv2.rectangle(img, (20, 10), (350, 150), (255,0,0), cv2.FILE_NODE_FLOAT)
        cv2.putText(img, f'Sleep Count: {counter_s}', (50, 60),cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 2)
        cv2.putText(img, f'Yawn Count: {counter_y}', (50, 120),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

        #drowsiness detection logic

        #------------------------Eye-----------------------------

        if eyeLeft_ratio <= 50 and eyeRight_ratio <= 50:
            breakcount_s += 1
            if breakcount_s >= 30:
                alert()
                if state_s == False:
                    counter_s += 1
                    sound.play()
                    state_s = not state_s
        else:
            breakcount_s = 0
            if state_s:
                state_s = not state_s

        # ------------------------Mouth-----------------------------

        if mouth_ratio > 40:
            breakcount_y += 1
            if breakcount_y >= 30:
                alert()
                if state_y == False:
                    counter_y += 1
                    alert()
                    sound.play()
                    state_y = not state_y
        else:
            breakcount_y = 0
            if state_y:
                state_y = not state_y



        for id in faceId:
            cv2.circle(img,face[id], 3, (128,255,0), cv2.FILLED)


    cv2.imshow("Image", img)
    cv2.waitKey(1)