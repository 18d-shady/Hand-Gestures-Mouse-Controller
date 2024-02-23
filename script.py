import cv2
import mediapipe as mp
import numpy as np
from math import dist
import time
import pyautogui
import sys

#to scroll let two fingers be on
#to right click used the middle finger
#to left click use the index finger
#to double click use the two fingers
#to drag close your hand and drag and then drop by opening the hand
#to zoom in or out use the index finger and thumb

points = []

fin_posx = 0
fin_posy = 0
sizex, sizey = pyautogui.size()
#print(sizex, sizey)
#pyautogui.moveTo(0, 50)
#mDown = 0

#For calculating distance between two points on a graph

def x_coordinate(landmark):  #landmark --> out of 21
    return float(str(results.multi_hand_landmarks[-1].landmark[int(landmark)]).split('\n')[0].split(" ")[1])

def y_coordinate(landmark):  #landmark --> out of 21
    return float(str(results.multi_hand_landmarks[-1].landmark[int(landmark)]).split('\n')[1].split(" ")[1])

def finger(landmark, z):   
#is z="finger, it retuens which finger is closed. If z="true coordinate", it returns the true coordinates
    if results.multi_hand_landmarks is not None:
        try:
            p0x = x_coordinate(0) #coordinates of landmark 0
            p0y = y_coordinate(0)
            p7x = x_coordinate(7) #coordinates of tip index
            p7y = y_coordinate(7)
            d07 = dist([p0x, p0y], [p7x, p7y])
          
            p8x = x_coordinate(8) #coordinates of mid index
            p8y = y_coordinate(8)
            d08 = dist([p0x, p0y], [p8x, p8y])
            p11x = x_coordinate(11) #coordinates of tip middlefinger
            p11y = y_coordinate(11)
            d011 = dist([p0x, p0y], [p11x, p11y])
            p12x = x_coordinate(12) #coordinates of mid middlefinger
            p12y = y_coordinate(12)                    
            d012 = dist([p0x, p0y], [p12x, p12y])
            p15x = x_coordinate(15) #coordinates of tid ringfinger
            p15y = y_coordinate(15)                    
            d015 = dist([p0x, p0y], [p15x, p15y])
            p16x = x_coordinate(16) #coordinates of mid ringfinger
            p16y = y_coordinate(16)
            d016 = dist([p0x, p0y], [p16x, p16y])
            p19x = x_coordinate(19) #coordinates of tip lilfinger
            p19y = y_coordinate(19)                    
            d019 = dist([p0x, p0y], [p19x, p19y])
            p20x = x_coordinate(20) #coordinates of mid lilfinger
            p20y = y_coordinate(20)                    
            d020 = dist([p0x, p0y], [p20x, p20y])
            close = []
                  
            if z == "finger":    
                if d07>d08:
                 close.append(1)
                if d011>d012:
                  close.append(2)
                if d015>d016:
                  close.append(3)
                if d019>d020:
                  close.append(4)
                return close
        
            elif z == "true coordinate":
                plandmark_x = x_coordinate(landmark)
                plandmark_y = y_coordinate(landmark)         
                return (int(640*plandmark_x), int(480*plandmark_y))
                        
                    
        except:
           pass

        
def orientation(coordinate_landmark_0, coordinate_landmark_9): 
    x0 = coordinate_landmark_0[0]
    y0 = coordinate_landmark_0[1]
    
    x9 = coordinate_landmark_9[0]
    y9 = coordinate_landmark_9[1]
    
    if abs(x9 - x0) < 0.05:      #since tan(0) --> ∞
        m = 1000000000
    else:
        m = abs((y9 - y0)/(x9 - x0))       
        
    if m>=0 and m<=1:
        if x9 > x0:
            return "Right"
        else:
            return "Left"
    if m>1:
        if y9 < y0:       #since, y decreases upwards
            return "Up"
        else:
            return "Down"
        
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
print("""
Welcome!!!
This is a hand gesture-mouse controller.
Follow the guidelines please:
- To move the cursor around raise the index finger, and move it around
- to left click lift the index finger and the little finger
- to right click lift the middle finger
- to double click lift the index and middle finger
- to drag something raise the index, middle and ring finger
- to scroll down ring and little finger
- to hold the mouse down, raise the ring finger, then use the index finger to drag
- to release the mouse when done dragging still raise little finger
- draw on the screen use thumbs up
""")
cap = cv2.VideoCapture(0)

#for moving the mouse
def moveMouse(z):
    global fin_posx, fin_posy, sizex, sizey
    #cur_posx, cur_posy = pyautogui.position()
    #print(cur_posx, cur_posy)
    #print(fin_posx, fin_posy)
    #time.sleep(2)
    newfinx = sizex * (finger(7, "true coordinate")[0]/640)
    newfiny = sizey * (finger(7, "true coordinate")[1]/480)
    #print(newfinx, newfiny)
    #if newfinx != fin_posx or newfiny != fin_posy:
    movex = newfinx - fin_posx
    movey = newfiny - fin_posy
    #print(movex, movey)
    if z == 1:
        try:
            pyautogui.move(movex, movey)
            
        except pyautogui.FailSafeException as e:
            pass

    elif z == 2:
        pyautogui.drag(movex, movey, button="left")

    elif z == 3:
        if movey > 0:
            pyautogui.scroll(20)
        else:
            pyautogui.scroll(-20)
            
        if movex > 0:
            pyautogui.hscroll(20)
        else:
            pyautogui.hscroll(-20)

    elif z == 4:
        pyautogui.mouseDown(button="left")
    elif z == 5:
        pyautogui.mouseUp(button="left")
        
            
    fin_posx = newfinx
    fin_posy = newfiny


with mp_hands.Hands( static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        height = image.shape[0]
        width = image.shape[1]
        #print(height)
        #print(width)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        #image = cv2.flip(image, 1)
        results = hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            #to check if the left hand is a thumbs up
            #whenever there is a thumbs up draw line on the screen
            #to check if all the fingers are bent
            if finger(None, "finger") == [1,2,3,4]:
                if orientation(finger(0, "true coordinate"), finger(9, "true coordinate")) == "Right":
                    #to check for the thumb positionb
                    if finger(4,"true coordinate")[0] < finger(5,"true coordinate")[0]:
                        cv2.putText(image, "Okay!!", (500, 200), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 2, cv2.LINE_AA)
                        points.append(finger(8, "true coordinate"))
                        #since landmark 8 is the tip of index finger

            for i in range(len(points) - 1):
                cv2.line(image, (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]), color = (255, 255, 0), thickness = 1)
                        
            #to check if the orientation is down
            #if orientation(finger(0, "true coordinate"), finger(9, "true coordinate")) == "Down":
                #cv2.putText(image, "Down!!", (300, 200), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 2, cv2.LINE_AA)

            #to check if index finger is up
            if finger(None, "finger") == [2,3,4]:
                #if orientation(finger(0, "true coordinate"), finger(9, "true coordinate")) == "Up":
                #cv2.putText(image, "index!!", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 2, cv2.LINE_AA)
                moveMouse(1)

            #to left click
            if finger(None, "finger") == [2,3]:
                #if orientation(finger(0, "true coordinate"), finger(9, "true coordinate")) == "Up":
                pyautogui.click(button='left')

            #to right click
            if finger(None, "finger") == [1,3,4]:
                pyautogui.click(button='right')

            #to double click
            if finger(None, "finger") == [3,4]:
                pyautogui.doubleClick()

            #to drag
            if finger(None, "finger") == [4]:
                moveMouse(2)

            #to scroll
            if finger(None, "finger") == [1, 2]:
                moveMouse(3) 
        

            #to hold the mouse down 
            if finger(None, "finger") == [1,2,4]:
                moveMouse(4)

            #to release
            if finger(None, "finger") == [1,2,3]:
                moveMouse(5)

                
                
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks( image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            """
            #print(results.multi_hand_landmarks[-1].landmark[0])
            x = str(results.multi_hand_landmarks[-1].landmark[0]).split('\n')[0]
            y = str(results.multi_hand_landmarks[-1].landmark[0]).split('\n')[1]
            z = str(results.multi_hand_landmarks[-1].landmark[0]).split('\n')[2]
            x = float(x.split(" ")[1])
            y = float(y.split(" ")[1])
            z = float(z.split(" ")[1])
            x_real = x * width
            y_real = y * height
            print(x)
            print(y)
            print(z)
            print(x_real)
            print(y_real)
            """
            
            break
cap.release()

