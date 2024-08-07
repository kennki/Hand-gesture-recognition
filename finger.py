import cv2
from HandTrackingModule import HandDetector
import keyboard

class Main:
    def __init__(self):
        self.camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.camera.set(3, 480)
        self.camera.set(4, 480)

    def Gesture_recognition(self):
        while True:
            self.detector = HandDetector()
            frame, img = self.camera.read()
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img)

            if lmList:
                x_1, y_1 = bbox["bbox"][0], bbox["bbox"][1]
                x1, x2, x3, x4, x5 = self.detector.fingersUp()
                #space key press
                if x1 == 0 and x2 == 0 and x3 == 0 and x4 == 0 and x5 == 0:
                  keyboard.release('up')
                  keyboard.release('left')
                  keyboard.release('right')
                  keyboard.release('down')
                  keyboard.release('space')
                  print("stop")
               # left key press  
                elif (x2 == 1 and x3 == 1 and x4 == 1 and x5 ==1) and (x1 == 0):
                #   keyboard.release('up')
                #   keyboard.release('space')
                #   keyboard.release('right')
                #   keyboard.release('down')
                  keyboard.press('left')
                  print("left")
               # right key press                 
                elif (x3 == 1 and x4 == 1 and x5 == 1) and (x1 == 0 and x2 == 0):
                  keyboard.press('right')
                  print("right")
               # up key press   
                elif (x4 == 1 and x5 == 1) and (x1 == 0, x2 ==0, x3 == 0):
                  keyboard.press('up')
                  print("up")
               # down key press  
                elif x5 and (x1 == 0, x2 ==0, x3 == 0, x4 == 0):
                  keyboard.press('down')
                  print("down")
                elif x2 and (x1 == 0, x3 ==0, x4 == 0, x5 == 0):
                  keyboard.press('space')  
                  print("space")

            frame_flipped_horizontal = cv2.flip(img, 1)
            cv2.imshow('camera', frame_flipped_horizontal)
            
            if cv2.getWindowProperty('camera', cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(5) & 0xFF == 27:
                break

if __name__ == '__main__':
    Solution = Main()
    Solution.Gesture_recognition()
