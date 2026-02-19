import cv2
import os
from flask import Flask, Response, jsonify
from flask_cors import CORS
from gesture_engine import GestureEngine

app = Flask(__name__)
CORS(app)

# Initialize your AI engine (MediaPipe & Logic)
engine = GestureEngine()

def generate_frames():
    # CHANGE: We start at 1 to skip the phone camera (usually at 0)
    camera_index = 1 
    camera = cv2.VideoCapture(camera_index)
    
    # Fallback: If 1 doesn't work, try 2. If both fail, try 0 as a last resort.
    if not camera.isOpened():
        print("Camera index 1 failed, trying index 2...")
        camera = cv2.VideoCapture(2)
    if not camera.isOpened():
        print("Camera index 2 failed, trying index 0...")
        camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # 1. Flip for mirror view (crucial for natural mouse movement)
            frame = cv2.flip(frame, 1)
            
            # 2. Extract Landmarks (The 21 points)
            # This identifies the skeleton of your hand for the 15 gestures
            processed_frame, results = engine.process_frame(frame)
            
            # 3. Encode to JPEG for the browser stream
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def home():
    return "Backend is running. Visit /video_feed to see the camera."

@app.route('/video_feed')
def video_feed():
    # This endpoint streams the processed camera feed to your React UI
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/init_folders')
def init_folders():
    # Creates the 15 folders needed for your 7,500 total samples
    gestures = [
        'vol_up', 'vol_down', 'mute', 'play', 'pause', 
        'next', 'prev', 'scroll_up', 'scroll_down', 
        'copy', 'paste', 'zoom_in', 'zoom_out', 'click', 'idle'
    ]
    for g in gestures:
        os.makedirs(f'data/{g}', exist_ok=True)
    return jsonify({"status": "Success", "message": "15 Folders Created for Data Collection"})

if __name__ == "__main__":
    # Start the Flask server
    app.run(host='0.0.0.0', port=5000)