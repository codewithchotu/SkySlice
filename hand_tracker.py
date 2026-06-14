import cv2
import mediapipe as mp

class HandTracker:

    def __init__(self):

        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def get_index_finger(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            h,w,_ = frame.shape

            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)

            return (x,y)

        return None