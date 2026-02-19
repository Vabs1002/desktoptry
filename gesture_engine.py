import cv2
import mediapipe as mp

class GestureEngine:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.cap = None

    def start(self):
        # CHANGE 0 to 1 if the camera doesn't open
        self.cap = cv2.VideoCapture(0) 
        
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Flip the image for a selfie-view (makes cursor control easier)
            frame = cv2.flip(frame, 1)
            
            # Process the frame for landmarks
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # If hands are found, draw the 21 points
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # This is where your 15-gesture logic will live!
                    print("Hand detected!") 

            cv2.imshow('Gesture Control Window', frame)
            if cv2.waitKey(5) & 0xFF == 27: # Press 'ESC' to quit
                break

        self.cap.release()
        cv2.destroyAllWindows()