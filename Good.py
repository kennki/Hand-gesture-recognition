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


      for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
        idx_tip = hand_landmarks.landmark[8]#index finger tip,value:0-1
        idx_mcp = hand_landmarks.landmark[5]#index finger mcp  
        thmb_tip = hand_landmarks.landmark[4]#thumb finger tip
        mid_tip = hand_landmarks.landmark[12] #middle finger tip
        ring_tip=hand_landmarks.landmark[16]
        pinky_tip=hand_landmarks.landmark[20]
        wrist=hand_landmarks.landmark[0]
        thmb_mcp=hand_landmarks.landmark[2]
       
        thmb_x, thmb_y = (1-thmb_tip.x)*640, thmb_tip.y * 480
        idx_mcp_x, idx_mcp_y = (1-idx_mcp.x)*640, idx_mcp.y * 480
        idx_x, idx_y = (1-idx_tip.x) * 640, idx_tip.y * 480
        mid_x, mid_y = mid_tip.x * 640, mid_tip.y * 480
        wrist_x, wrist_y= wrist.x*640, wrist.y*480 
        thmbm_x, thmbm_y = (1-thmb_mcp.x)*640, thmb_mcp.y * 480
        ring_x, ring_y = (1-ring_tip.x)*640, ring_tip.y * 480
        pinky_x, pinky_y = (1-pinky_tip.x)*640, pinky_tip.y * 480
         
        # hand_angle = atan2(mid_x- wrist_x, mid_y-wrist_y)
        # hand_angle = degrees(hand_angle)
        hand1_angle = atan2(thmb_x- thmbm_x, thmb_y-thmbm_y)
        hand1_angle = degrees(hand1_angle)
        hand2_angle = atan2(idx_x- idx_mcp_x, idx_y-idx_mcp_y)
        hand2_angle = degrees(hand2_angle)
        # thmb_idx_dist = math.dist((thmb_x, thmb_y),(idx_x, idx_y))
        # mid_idx_dist = math.dist((mid_x, mid_y),(idx_x, idx_y))
        # idx_to_mcp_dist = math.dist((thmb_x, thmb_y),(idx_mcp_x, idx_mcp_y))
        # print(idx_to_mcp_dist) # 70 mid
        # ifidx_to_mcp_dist<70:
        #   if hand_id == 0:
        #     keyboard.press_and_release('down')
        #     print('down')
        #   else:
        #     keyboard.press_and_release('up')
        #     print('up')
        #Recognising fist gestures
        # 假设已经获取了手部关键点的列表 hand_landmarks

        thmb_x, thmb_y = (1-thmb_tip.x)*640, thmb_tip.y * 480
        idx_x, idx_y = (1-idx_tip.x) * 640, idx_tip.y * 480
        # 设定阈值范围（根据实际情况进行调整）
        threshold_min = 0.02*640
        threshold_max = 0.10*640

        # 计算食指和大拇指之间的距离
        thmb_idx_dist = math.dist((thmb_x, thmb_y),(idx_x, idx_y))
        
        # 判断是否为拳头手势
        # if threshold_min < thmb_idx_dist < threshold_max:
        #   keyboard.release('up')
        #   keyboard.press_and_release('space')
        #   print("space")

        hand_space = 0
        hand_stone = 0

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
        if hand_stone == 0 and 140<hand2_angle<220:
             keyboard.press('space')
             print("space")
             hand_space = 1
        #print hand_angle
       #left key press
        if hand_stone == 0 and -110<hand1_angle<-70:
            # left key
            #  keyboard.release('space')
            #  keyboard.release('up')
            #  keyboard.release('down')
            #  keyboard.release('right')
             keyboard.press('left')
             print("left")
        # else:
        #      keyboard.release('left')
        #      #keyboard.release('space')
        
        # up key press
        if hand_stone == 0  and 170<hand1_angle<210:
            #up key 
            #  keyboard.release('space')
            #  keyboard.release('left')
            #  keyboard.release('right')
            #  keyboard.release('down')
             keyboard.press('up')
             print('up')
        # else:
        #      keyboard.release('up')
        #      #keyboard.release('space')
        #right key press
        if hand_stone == 0 and hand_space == 0 and 110<hand1_angle<150:
          # right key press
            #  keyboard.release('space')
            #  keyboard.release('left')
            #  keyboard.release('up')
            #  keyboard.release('down')
             keyboard.press('right')
             print('right')
        # else:
        #      keyboard.release('right')
        #      # keyboard.release('space')
        #down key press                                     
        if hand_stone == 0 and -20<hand1_angle<20: 
            #  keyboard.release('space')
            #  keyboard.release('left')
            #  keyboard.release('up')
            #  keyboard.release('right')
             keyboard.press('down')
             print("down")
        # else:
        #      keyboard.release('down')
        #      # keyboard.release('space')

       
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



