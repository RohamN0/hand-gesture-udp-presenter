import mediapipe as mp
import cv2, socket, time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
windows_ip = "172.16.0.3"
udp_port = 5005
cooldown = 1.0
last_action_time = 0

mediapipe_hands = mp.solutions.hands
hands = mediapipe_hands.Hands(min_detection_confidence=0.75)
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_landmark_list = []

while True:
    success, frame = cap.read()
    if not success:
        break
        
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(frame_rgb)

    current_landmark_list = []
    if res.multi_hand_landmarks:
        for handlandmarks in res.multi_hand_landmarks:
            draw.draw_landmarks(frame, handlandmarks, mediapipe_hands.HAND_CONNECTIONS) 
            
            for i, lm in enumerate(handlandmarks.landmark):
                h, w, _ = frame.shape
                x, y = int(lm.x * w), int(lm.y * h)
                current_landmark_list.append([i, x, y])

    if len(current_landmark_list) >= 21 and len(last_landmark_list) >= 21:
        is_page_down = True
        is_page_up = True

        for pos in [20, 16]:
            last_y_tip = last_landmark_list[pos][2]
            last_y_joint = last_landmark_list[pos - 2][2]
            curr_y_tip = current_landmark_list[pos][2]
            curr_y_joint = current_landmark_list[pos - 2][2]

            if not (last_y_tip > last_y_joint and curr_y_tip > curr_y_joint):
                is_page_down = False
            
            if not (last_y_tip < last_y_joint and curr_y_tip > curr_y_joint):
                is_page_up = False

        for pos in [12, 8]:
            last_y_tip = last_landmark_list[pos][2]
            last_y_joint = last_landmark_list[pos - 2][2]
            curr_y_tip = current_landmark_list[pos][2]
            curr_y_joint = current_landmark_list[pos - 2][2]

            condition_open_to_closed = (last_y_tip < last_y_joint) and (curr_y_tip > curr_y_joint)
            
            if not condition_open_to_closed:
                is_page_down = False
                is_page_up = False

        current_time = time.time()
        if current_time - last_action_time > cooldown:
            if is_page_down:
                print('Sending: Page Down')
                sock.sendto(b"PGDN", (windows_ip, udp_port))
                last_action_time = current_time

            elif is_page_up:
                print('Sending: Page Up')
                sock.sendto(b"PGUP", (windows_ip, udp_port))
                last_action_time = current_time

    last_landmark_list = current_landmark_list
            
    cv2.imshow('webcam', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

