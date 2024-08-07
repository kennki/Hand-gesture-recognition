import cv2
import mediapipe as mp
import keyboard
import math
from math import atan2, degrees

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      if len(results.multi_hand_landmarks) == 2:#If two hands are detected
        thumb_point_0 = results.multi_hand_landmarks[0].landmark[4]
        thumb_point_1 = results.multi_hand_landmarks[1].landmark[4]

        thumb_point_0_x, thumb_point_0_y = thumb_point_0.x, thumb_point_0.y
        thumb_point_1_x, thumb_point_1_y = thumb_point_1.x, thumb_point_1.y

        handle_angle = atan2(thumb_point_0_x- thumb_point_1_x, thumb_point_0_y-thumb_point_1_y)
        handle_angle = degrees(handle_angle) # 80 and 100 , mid is 90
        
        # if abs(handle_angle)<70:
        #   keyboard.press_and_release('left')
        #   print('left')
        # elif abs(handle_angle)>120:
        #   keyboard.press_and_release('right')
        #   print('right')
 


      for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
        idx_tip = hand_landmarks.landmark[8]#index finger tip,value:0-1
        idx_mcp = hand_landmarks.landmark[5]#index finger mcp  
        idx_pip = hand_landmarks.landmark[6]
        thmb_tip = hand_landmarks.landmark[4]#thumb finger tip
        mid_mcp = hand_landmarks.landmark[9]
        mid_pip = hand_landmarks.landmark[10]
        mid_tip = hand_landmarks.landmark[12]#middle finger tip
        ring_pip = hand_landmarks.landmark[14]
        # thub_cmc=hand_landmarks.landmark[1]
        wrist=hand_landmarks.landmark[0]
        thmb_mcp=hand_landmarks.landmark[2]
       
        thmb_x, thmb_y = (1-thmb_tip.x)*640, thmb_tip.y * 480
        idxm_x, idxm_y = (1-idx_mcp.x)*640, idx_mcp.y * 480
        idx_x, idx_y = (1-idx_tip.x) * 640, idx_tip.y * 480
        mid_x, mid_y = mid_tip.x * 640, mid_tip.y * 480
        wrist_x, wrist_y= wrist.x*640, wrist.y*480 
        thmbm_x, thmbm_y = (1-thmb_mcp.x)*640, thmb_mcp.y * 480
        idxp_x,idxp_y = (1-idx_pip.x)*640, idx_pip.y * 480 
        midp_x, midp_y = (1-mid_pip.x)*640, mid_pip.y * 480        
        ringp_x, ringp_y = (1-ring_pip.x)*640, ring_pip.y * 480  
        
        hand_angle = atan2(mid_x- wrist_x, mid_y-wrist_y)
        hand_angle = degrees(hand_angle)

        thmb_x, thmb_y = (1-thmb_tip.x)*640, thmb_tip.y * 480
        idx_x, idx_y = (1-idx_tip.x) * 640, idx_tip.y * 480
        # Setting the threshold range (adjusted according to the actual situation)
        threshold_min = 0.08*640
        threshold_max = 0.12*640

        # Calculate the distance between the index finger and the thumb
        thmb_idx_dist = math.dist((thmb_x, thmb_y),(idx_x, idx_y))
        #Calculate the distance between the index and middle fingers
        idxp_midp_dist = math.dist((idxp_x,idxp_y),(midp_x, midp_y))
        #Calculate the distance between the middle and ring fingers
        midp_ringp_dist = math.dist((midp_x, midp_y),(ringp_x, ringp_y))
        hand_space = 0
        hand_stone = 0

        #print hand_angle                                                                                   
         # stop  
        if thmb_idx_dist < threshold_max and hand_space == 0 :
             keyboard.release('up')
             keyboard.release('left')
             keyboard.release('right')
             keyboard.release('down')
             keyboard.release('space')
             print("stop")
             hand_stone = 1
         #space key press
        if hand_stone == 0 and idxp_midp_dist > threshold_min and midp_ringp_dist > threshold_min :
             keyboard.press('space')
             print("space")
             hand_space = 1
        #left key press
        if hand_stone == 0 and hand_space == 0 and 60<hand_angle<120:
             keyboard.press("left")
             print("left")
            #  hand_space = 0
        #up key press
        if hand_stone == 0 and hand_space == 0 and 150<hand_angle<200:
             keyboard.press('up')
             print('up')

        #right key press
        if -120<hand_angle<-60 and hand_space == 0:
          keyboard.press('right')
          print('right')
          hand_space= 0
        
        #down key press                                    
        if hand_stone == 0 and hand_space == 0 and -30<hand_angle<30: 
          keyboard.press('down')
          print("down")
          hand_space= 0
  
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()



