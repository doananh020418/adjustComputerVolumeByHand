import cv2
import numpy as np
import HandTrackingModule as hm
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]


cap = cv2.VideoCapture(0)
pTime = 0
if cap.isOpened():
    while True:
        success, img = cap.read()
        if success:
            img = cv2.flip(img, 1)
            detector = hm.handDetector(detectionCon=0.7,trackCon=0.7)
            hands = detector.findHands(img,draw= True)
            lmList = detector.findPosition(hands,draw= False)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'FPS: {str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 1, )

            if len(lmList) != 0 :
                x1,y1 = lmList[4][1],lmList[4][2]
                x2,y2 = lmList[8][1],lmList[8][2]
                cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0),cv2.FILLED)

                cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
                length = math.hypot(x2-x1,y2-y1)
                if length < 20:
                    length = 20
                if length >200:
                    length = 200
                vol = np.interp(length,[20,200],[minVol,maxVol])
                volume.SetMasterVolumeLevel(vol, None)

            cv2.imshow("cam", img)
            cv2.waitKey(1)

        