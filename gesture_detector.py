import cv2
import mediapipe as mp
from enum import Enum, auto

# NEW: An Enum to represent the different gesture states clearly.
class Gesture(Enum):
    NONE = auto()
    FIST = auto()
    PALM = auto()

class GestureDetector:
    """
    Handles webcam-based gesture recognition using MediaPipe to detect an open palm or a closed fist.
    """
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Error: Camera not accessible.")
            self.camera = None

    def is_palm_open(self, hand_landmarks):
        """Determines if the palm is open by checking if fingertips are extended."""
        try:
            # MediaPipe's y-coordinate decreases as you go up the screen.
            # For an open palm, the tip of the finger is higher (lower y-value) than its lower joint.
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            middle_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
            ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y
            ring_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y
            pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y
            pinky_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP].y

            return (
                index_tip < index_pip and
                middle_tip < middle_pip and
                ring_tip < ring_pip and
                pinky_tip < pinky_pip
            )
        except:
            return False

    # NEW: Logic to detect a closed fist.
    def is_fist_closed(self, hand_landmarks):
        """Determines if the fist is closed by checking if fingertips are curled in."""
        try:
            # For a closed fist, the tip of the finger is lower (higher y-value) than its lower joint.
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            middle_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
            
            # We also check the tip against the base of the palm (MCP joint) for a more robust check.
            index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

            return (
                index_tip > index_pip and index_tip > index_mcp and
                middle_tip > middle_pip and middle_tip > middle_mcp
            )
        except:
            return False

    def process_frame(self):
        """
        MODIFIED: Processes a single frame and returns the detected gesture state (FIST, PALM, or NONE).
        """
        if not self.camera or not self.camera.isOpened():
            return Gesture.NONE, None

        success, frame = self.camera.read()
        if not success:
            return Gesture.NONE, None

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        # MODIFIED: Default gesture is NONE.
        detected_gesture = Gesture.NONE
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # MODIFIED: Check for fist first, then open palm.
                if self.is_fist_closed(hand_landmarks):
                    detected_gesture = Gesture.FIST
                elif self.is_palm_open(hand_landmarks):
                    detected_gesture = Gesture.PALM
        
        # MODIFIED: Return the gesture state and the camera frame.
        return detected_gesture, frame

    def cleanup(self):
        """Releases the camera and closes OpenCV windows."""
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()