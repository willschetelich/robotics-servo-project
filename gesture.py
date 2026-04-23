import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import serial

# config serial
ser = serial.Serial('/dev/tty.usbmodem2101', 115200)



# config hands landmark detector
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)  # 0 is default

i = 0
while cap.isOpened():
    ret, frame = cap.read()

    # print(ret)
    if not ret:
        break

    # convert frame to mediapipe image and detect
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    result = detector.detect(mp_image)

 
    i = i+1
    # print(result.handedness, i)
    if result.hand_landmarks:
        landmarks = result.hand_landmarks[0]
        tip = landmarks[8]
        # print(tip.x, tip.y, tip.z)
        pointer_finger = landmarks[8].y
        wrist = landmarks[0].y

        difference = wrist/pointer_finger # since it's backwards
        print(f"{wrist}, {pointer_finger}")
        percentage = (pointer_finger/wrist) + .2 
        print(f"Percentage: {percentage}")
        
        angle = int(percentage * 180)
        angle = angle - 90
        angle = int(angle * 2) -50


        angle = max(70, min(200, angle))
        
        print(angle)
        ser.write(f"{angle};".encode())


        # index = 


        h, w, _ = frame.shape
        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    cv2.imshow('Feed', frame)
    # q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()