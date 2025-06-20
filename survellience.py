from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import smtplib


# Email configuration
def send_email_alert(object_name, confidence):
    sender_email = "99220040181@klu.ac.in"
    receiver_email = "99220040181@klu.ac.in"  # Can be the same or different
    password = "wsmk ogbj xmvn iysm"  # Use your app password here

    subject = "Alert: Object Detected!"
    body = f"A {object_name} has been detected with a confidence of {confidence * 100:.2f}%."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)  # Log in with the sender's email and password
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email alert sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Initialize video capture
# cap = cv2.VideoCapture("guns3.jpg")
cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# Load the YOLO model
model = YOLO("../Yolo-Weights/guns8l.pt")

# Class names for detection
classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
    "potted plant", "bed", "dining table", "toilet", "TV monitor", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair dryer", "toothbrush", "helmet", "watch", "ring", "wallet", "gloves", "mirror",
    "printer", "fan", "water bottle", "hat", "drone", "speaker", "microphone", "stapler", "furniture",
    "treadmill", "dumbbell", "kettle", "umbrella", "pen", "pencil", "chair", "broom", "mop", "plate",
    "shovel", "bucket", "calculator", "jacket", "shoe", "sneaker", "boot", "drill", "toolbox", "saw",
    "plunger", "can", "pail", "lamp", "table lamp", "light bulb", "switch", "power strip", "trash can"
]

# Extended weapon classes (add more based on model training and requirement)
weapon_classes = ["knife"]

prev_frame_time = 0
new_frame_time = 0

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Ensure all coordinates are integers
            w, h = x2 - x1, y2 - y1

            # Check for valid coordinates
            if w > 0 and h > 0:  # Ensure width and height are positive
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw the rectangle with color and thickness

                conf = box.conf[0].item()  # Get confidence as a scalar
                cls = int(box.cls[0])

                if 0 <= cls < len(classNames):
                    class_name = classNames[cls]
                    cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    if class_name in weapon_classes:
                        send_email_alert(class_name, conf)

    fps = 1 / (new_frame_time - prev_frame_time) if new_frame_time - prev_frame_time > 0 else 0
    prev_frame_time = new_frame_time
    print(f"FPS: {fps:.2f}")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Allow quitting with 'q'
        break

cap.release()
cv2.destroyAllWindows()
