import cv2
import mediapipe as mp
import pyautogui
import math
import time

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ----------------------------
# Video Capture and Screen Setup
# ----------------------------
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Tracking", 640, 480)


# ----------------------------
# Settings and Thresholds
# ----------------------------
smoothening = 0.5                    # Smoothing factor for pointer movement.
movement_threshold = 40              # Maximum index finger movement (in frame pixels) allowed for click actions.
thumb_threshold_factor = 1.2         # Factor to determine when the thumb is "substantially" away from the index base.
middle_raise_threshold = 0.05         # Base threshold for middle finger raise.
middle_raise_buffer = 0.05            # Additional buffer so slight raises won’t trigger right click.
DRAG_HOLD_TIME = 0.5                 # Time to hold a gesture to count as dragging.
PINCH_THRESHOLD = 40                 # Maximum distance (in pixels) between thumb and index for pinch (scroll) mode.
SCROLL_FACTOR = 5.0                  # Multiplier to convert vertical offset to scroll amount.




prev_screen_x, prev_screen_y = screen_width // 2, screen_height // 2
prev_index_x, prev_index_y = None, None


left_click_start_time = None
left_dragging = False
right_click_start_time = None
right_dragging = False


scroll_mode = False
scroll_base_y = None  

while True:
    ret, frame = cap.read()
    if not ret:
        break


    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[8]
            index_mcp = hand_landmarks.landmark[5]  
            thumb_tip = hand_landmarks.landmark[4]
            middle_tip = hand_landmarks.landmark[12]
            middle_mcp = hand_landmarks.landmark[9]
            wrist = hand_landmarks.landmark[0]

            # Convert normalized coordinates to pixel positions.
            index_x = int(index_tip.x * frame_width)
            index_y = int(index_tip.y * frame_height)
            index_base_x = int(index_mcp.x * frame_width)  
            index_base_y = int(index_mcp.y * frame_height)  
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)
            middle_x = int(middle_tip.x * frame_width)
            middle_y = int(middle_tip.y * frame_height)
            wrist_x = int(wrist.x * frame_width)
            wrist_y = int(wrist.y * frame_height)

            # Draw a circle on the index finger tip for visual feedback.
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            # -----------------------------------------------
            # Map Index Finger Tip Position to Screen Coordinates
            # (Smoothing is applied to reduce jitter.)
            # -----------------------------------------------
            new_screen_x = int(index_tip.x * screen_width)
            new_screen_y = int(index_tip.y * screen_height)
            smoothed_x = int(prev_screen_x + (new_screen_x - prev_screen_x) * smoothening)
            smoothed_y = int(prev_screen_y + (new_screen_y - prev_screen_y) * smoothening)

            # -----------------------------------------------
            # Determine Movement Speed (for stable gestures)
            # -----------------------------------------------
            if prev_index_x is not None and prev_index_y is not None:
                speed = math.hypot(index_x - prev_index_x, index_y - prev_index_y)
            else:
                speed = 0
            click_allowed = speed < movement_threshold

            # -----------------------------------------------
            # Scroll Gesture: 
            # -----------------------------------------------
            pinch_distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
            if pinch_distance < PINCH_THRESHOLD and click_allowed:
                scroll_mode = True
                # Set the scroll base point only when entering scroll mode.
                if scroll_base_y is None:
                    scroll_base_y = index_y
                # Calculate vertical offset from the scroll start point.
                delta_y = scroll_base_y - index_y  
                scroll_amount = int(delta_y * SCROLL_FACTOR)
                if scroll_amount != 0:
                    pyautogui.scroll(scroll_amount)
                cv2.putText(frame, "Scrolling", (index_x, index_y - 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                scroll_mode = False
                scroll_base_y = None

            # -----------------------------------------------
            # Left Click/Drag Gesture: 
            # -----------------------------------------------
            if not scroll_mode:
                # Estimate hand size using the distance between the middle finger and the wrist.
                hand_size = math.hypot(middle_x - wrist_x, middle_y - wrist_y)
                # Compute the Euclidean distance between the index finger base and the thumb tip.
                thumb_distance = math.hypot(index_base_x - thumb_x, index_base_y - thumb_y)
                # Trigger if the thumb tip is substantially away from the index base.
                thumb_fully_extended = thumb_distance > (thumb_threshold_factor * hand_size)

                if thumb_fully_extended and click_allowed:
                    if left_click_start_time is None:
                        left_click_start_time = current_time
                    duration = current_time - left_click_start_time
                    if duration >= DRAG_HOLD_TIME:
                        if not left_dragging:
                            pyautogui.mouseDown(button='left')
                            left_dragging = True
                        cv2.putText(frame, "Dragging Left", (index_x, index_y - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    else:
                        cv2.putText(frame, "Left Click", (index_x, index_y - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                else:
                    if left_click_start_time is not None:
                        duration = current_time - left_click_start_time
                        if left_dragging:
                            pyautogui.mouseUp(button='left')
                        else:
                            if duration < DRAG_HOLD_TIME:
                                pyautogui.click(button='left')
                        left_click_start_time = None
                        left_dragging = False

                # -----------------------------------------------
                # Right Click/Drag Gesture: Middle Finger Raise.
                # -----------------------------------------------
                if (middle_mcp.y - middle_tip.y) > (middle_raise_threshold + middle_raise_buffer) and click_allowed:
                    if right_click_start_time is None:
                        right_click_start_time = current_time
                    duration = current_time - right_click_start_time
                    if duration >= DRAG_HOLD_TIME:
                        if not right_dragging:
                            pyautogui.mouseDown(button='right')
                            right_dragging = True
                        cv2.putText(frame, "Dragging Right", (index_x, index_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    else:
                        cv2.putText(frame, "Right Click", (index_x, index_y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                else:
                    if right_click_start_time is not None:
                        duration = current_time - right_click_start_time
                        if right_dragging:
                            pyautogui.mouseUp(button='right')
                        else:
                            if duration < DRAG_HOLD_TIME:
                                pyautogui.click(button='right')
                        right_click_start_time = None
                        right_dragging = False


            # -----------------------------------------------
            # Update Pointer Position and Save Previous Coordinates.
            # -----------------------------------------------
            pyautogui.moveTo(smoothed_x, smoothed_y)
            prev_screen_x, prev_screen_y = smoothed_x, smoothed_y
            prev_index_x, prev_index_y = index_x, index_y

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



