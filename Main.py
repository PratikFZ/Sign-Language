import numpy as np
import mediapipe as mp
from Function import *

holy_hands = mp.solutions.hands
cap = cv.VideoCapture(0)

with holy_hands.Hands(
    max_num_hands=1 # Here only one hand is going to be detect (You can change it if you want more hands to be detected)
                      ) as hands:
   index_cord=[] # This list stores values for pointer
   while cap.isOpened():
     success, image = cap.read()
     if not success:
       print("Ignoring empty camera frame.")
       continue

     # To improve performance, optionally mark the image as not writeable 
     image.flags.writeable = False
     image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
     results = hands.process(image)

     # Draw the hand annotations on the image.
     image.flags.writeable = True
     image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
     
     # Images shape
     imgH,imgW=image.shape[:2]
     string=''
     if results.multi_hand_landmarks:
       for hand_landmarks in results.multi_hand_landmarks:
         # Get Hand Cordinates (HC values)
         hand_cordinate=[]
         for index , landmark in enumerate(hand_landmarks.landmark):
            x_cordinate , y_cordinate = int(landmark.x*imgW) , int(landmark.y*imgH)
            hand_cordinate.append([index,x_cordinate,y_cordinate])
         hand_cordinate=np.array(hand_cordinate)
         # Working on image 
         string=persons_input(hand_cordinate)
         image=get_fram(image,hand_cordinate,string)
     # For pointer
     if string==" D" :
          index_cord.append([15,hand_cordinate[8][1],hand_cordinate[8][2]])
     if string==" I" or string==" J":
          index_cord.append([15,hand_cordinate[20][1],hand_cordinate[20][2]])
     for val in index_cord:
          image=cv.circle(image,(val[1],val[2]),val[0],(255,255,255),1)
          val[0]=val[0]-1
          if val[0]<=0:
              index_cord.remove(val)
     # Flip the image horizontally for a selfie-view display.
     cv.imshow('Sign Language detection', cv.flip(image,1))

     if cv.waitKey(5) & 0xFF == ord('x'):
       break
cap.release()

