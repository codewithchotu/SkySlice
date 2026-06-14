import cv2
import sys
from hand_tracker import HandTracker

def test_camera_and_tracker():
    print("Testing camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("FAILED: Camera not found or could not be opened.")
        sys.exit(1)
        
    ret, frame = cap.read()
    if not ret or frame is None:
        print("FAILED: Could not read a frame from the camera.")
        cap.release()
        sys.exit(1)
        
    print("Camera test passed. Frame shape:", frame.shape)
    
    print("Testing HandTracker...")
    try:
        tracker = HandTracker()
        finger = tracker.get_index_finger(frame)
        print("HandTracker initialized successfully.")
        print("Finger detection result (None expected if no hand present):", finger)
    except Exception as e:
        print("FAILED: HandTracker threw an exception:", e)
        cap.release()
        sys.exit(1)
        
    print("SUCCESS: Camera and hand tracking are functioning correctly!")
    cap.release()

if __name__ == "__main__":
    test_camera_and_tracker()
