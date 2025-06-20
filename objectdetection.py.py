from flask import Flask, render_template, Response, request, redirect, url_for
from ultralytics import YOLO
import cv2
import cvzone
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLO models
model_general = YOLO("../Yolo-Weights/yolov8l.pt")
model_custom = YOLO("../Yolo-Weights/guns8l.pt")

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

classNames_custom = ["Gun"]

def send_email_alert(object_name, confidence):
    sender_email = "ravikumarraj01010@gmail.com"  # Your email
    receiver_email = "99220040181@gmail.com"  # Alerting email
    password = "ndpv bsfb xreh kson"  # Your email password or app-specific password

    subject = "Alert: Object Detected!"
    body = f"A {object_name} has been detected with a confidence of {confidence * 100:.2f}%."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email alert sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def generate_frames(source=0):
    cap = cv2.VideoCapture(source)
    frame_count = 0
    while True:
        success, img = cap.read()
        if not success:
            break

        frame_count += 1

        # Run inference on both models
        results_general = model_general(img)
        results_custom = model_custom(img)

        # Process results from the general model
        for r in results_general:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1

                if w > 0 and h > 0:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    conf = box.conf[0].item()
                    cls = int(box.cls[0])

                    if 0 <= cls < len(classNames_general):
                        class_name = classNames_general[cls]
                        cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                        # Send email alert if a specific object is detected with confidence > 60%
                        if class_name in ["Gun", "knife"] and conf > 0.4 and frame_count % 5 == 0:
                            send_email_alert(class_name, conf)

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('uploaded_video', filename=file.filename))

@app.route('/uploaded_video/<filename>')
def uploaded_video(filename):
    return Response(generate_frames(os.path.join(app.config['UPLOAD_FOLDER'], filename)), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)