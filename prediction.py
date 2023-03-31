#from types import NoneType
import cv2
import numpy as np
import mediapipe as mp
import constants as c
from tensorflow.python.keras.models import load_model
import utils as util
from apscheduler.schedulers.background import BackgroundScheduler
import time
import types
import kakao_send
import arduino_send

#Python실행 > 
#Warning Area가 2개로 설정되어 있고, 하나는 전기차단 및 소리알림 기능영역이고, 
# 나머지 하나는 카카오톡 전송 기능입니다.#
#첫번째로 전기차단 영역으로 들어가게 되면, 멀티탭 전기가 꺼지게 되고, 소리알람이 울립니다.
#두번재로 카카오톡 전송 영역으로 들어가게 되면, 보호자에게 카카오톡이 전송되게 됩니다.

#Declarations
prev_result_time = time.time()
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
model = load_model('model/model_baby_99acc_22-8_4.h5')
sequence = []
global kakao_mesg
global arduino_mesg
                        
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
WHITE_COLOR = (255, 255, 255)
mbox_w_2, mbox_h_2 = 180, 420
gl_activity_pred = "Please wait"

# Prediction Function
def predict_activity():
    print("**************************predict_activity()")
    global kakao_mesg
    global arduino_mesg
    kakao_mesg = True
    arduino_mesg = True
    arduino_send.on()

    return

# Convert positive number to negative
def negate(x):
    return x * -1


clicked_points = []
clone = None
def MouseLeftClick(event, x, y, flags, param):
    	# 왼쪽 마우스가 클릭되면 (x, y) 좌표를 저장한다.
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((y, x))

		# 원본 파일을 가져 와서 clicked_points에 있는 점들을 그린다.
        #image = clone.copy()
        for point in clicked_points:
            cv2.circle(image, (point[1], point[0]), 2, (0, 255, 255), thickness = -1)
        cv2.imshow("image", image)
        print(clicked_points)
    
    print(clicked_points)


def warning_check(cx_kakao,cy_kakao,cx_arduino,cy_arduino,landmarks,frame_width,frame_height):
    
    warning_detection(cx_kakao,cy_kakao,landmarks,frame_width,frame_height,"kakao")
    warning_detection(cx_arduino,cy_arduino,landmarks,frame_width,frame_height,"arduino")

                
def warning_detection(cx,cy,landmarks,frame_width,frame_height,flag):
    global kakao_mesg
    global arduino_mesg
    left_x = cx-100
    right_x = cx+50
    up_y = cy+50
    down_y = cy-50
    
    i=0
    for landmark in landmarks:
        check_x = landmark.x*frame_width
        check_y = landmark.y*frame_height
        #print(left_x, right_x, up_y, down_y)
        #print(i, check_x, check_y)
        i = i+1
        if(check_x > left_x and check_x < right_x and check_y < up_y and check_y > down_y):
            if(flag == "kakao"):
                #print("warning!!!!!!!!!!!!!!!!!!--kakao")
                if(kakao_mesg):    
                    print("warning-kakao")
                    kakao_send.send_mesg()
                    kakao_mesg = False
            else:
                #print("warning!!!!!!!!!!!!!!!!!!--arduino")
                if(arduino_mesg):
                    print("warning-arduino")
                    arduino_send.off()
                    arduino_mesg = False



# Prediction runs every secq
sched = BackgroundScheduler()
sched.add_job(predict_activity, 'interval', seconds=7)
sched.start()

# cap = cv2.VideoCapture('https://192.168.29.176:8080/video') 

#cv2.namedWindow("image")
#cv2.setMouseCallback("areaSelect",MouseLeftClick)
arduino_send.on()
cap = cv2.VideoCapture('raw/input3.mp4')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
#frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("framewidth : "+str(frame_width)+"frameheight : "+str(frame_height))

out = cv2.VideoWriter('output/video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
#clone = image.copy()

time_flag = True

flag = False
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():

        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = util.mediapipe_detection(frame, holistic)
        
            
        # Draw landmarks
        util.draw_styled_landmarks(mp_holistic, mp_drawing, image, results)
    
        
        # Add keypoints
        keypoints = util.extract_keypoints(results)
        sequence.append(keypoints)
    
        # Select last SEQUENCE_LEN sequences only
        sequence = sequence[negate(c.SEQUENCE_LEN):]
        #print("sequence length: ",len(sequence))
        #print("sequence: ",sequence)
        if(len(clicked_points)>2):
            cv2.rectangle(image, clicked_points[0], clicked_points[1], (0, 0, 0), -1)
        
        try:
            poseLandmark = results.pose_landmarks.landmark[15]
            cx_kakao = 500
            cy_kakao = 900
            cx_arduino = 1350
            cy_arduino = 400
            warning_check(cx_kakao,cy_kakao,cx_arduino,cy_arduino,results.pose_landmarks.landmark,frame_width,frame_height)

        except:
            pass
        
        # Display
        
        cv2.rectangle(image, (cx_kakao-100, cy_kakao-50), (cx_kakao+50, cy_kakao+50), (255, 10, 10), -1)
        cv2.rectangle(image, (cx_arduino-100, cy_arduino-50), (cx_arduino+50, cy_arduino+50), (10, 255, 10), -1)
        cv2.putText(image, 'Warning Area - KakaoTalk', (cx_kakao-100, cy_kakao-50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200,200,200), 2)
        cv2.putText(image, 'Warning Area - Arduino', (cx_arduino-100, cy_arduino-50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200,200,200), 2)
        cv2.imshow('Frame', image)        
        #clone = image.copy()
        #cv2.setMouseCallback('Frame', MouseLeftClick)

        # write to file
        out.write(image)

        # Exit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        if(time_flag):
            time.sleep(15)
            time_flag=False
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()