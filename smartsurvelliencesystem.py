from flask import Flask, render_template, request, redirect, url_for, Response
from ultralytics import YOLO
import cv2
import cvzone
import time
import os

app = Flask(__name__)

# Load YOLO models
model_general = YOLO("../Yolo-Weights/yolov8n.pt")
model_custom = YOLO("../Yolo-Weights/guns8n.pt")

# Class names for detection
classNames_general = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                      "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
                      "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie",
                      "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
                      "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon",
                      "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut",
                      "cake", "chair", "sofa", "potted plant", "bed", "dining table", "toilet", "TV monitor", "laptop",
                      "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
                      "book", "clock", "vase", "scissors", "teddy bear", "hair dryer", "toothbrush", "helmet", "watch",
                      "ring", "wallet", "gloves", "mirror", "printer", "fan", "water bottle", "hat", "drone", "speaker",
                      "microphone", "stapler", "furniture", "treadmill", "dumbbell", "kettle", "umbrella", "pen", "pencil",
                      "chair", "broom", "mop", "plate", "shovel", "bucket", "calculator", "jacket", "shoe", "sneaker", "boot",
                      "drill", "toolbox", "saw", "plunger", "can", "pail", "lamp", "table lamp", "light bulb", "switch",
                      "power strip", "trash can", "Gun", "knife"]

classNames_custom = ["Gun", "hand"]

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle video upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        return redirect(url_for('video_feed', path=filepath))
    return redirect(request.url)

# Route to handle video feed
@app.route('/video_feed')
def video_feed():
    path = request.args.get('path', default=0, type=str)
    return Response(gen_frames(path), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to generate video frames
def gen_frames(source):
    cap = cv2.VideoCapture(source)
    while True:
        success, frame = cap.read()
        if not success:
            break
        # Process frame with YOLO models
        results_general = model_general(frame)
        results_custom = model_custom(frame)
        # Add detection logic here
        # ...
        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)