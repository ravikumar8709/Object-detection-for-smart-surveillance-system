from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO
import cv2
import cvzone
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
cap = cv2.VideoCapture('cars.mp4')
cap.set(3, 1280)
cap.set(4, 720)

# Load both YOLO models
model_general = YOLO("../Yolo-Weights/yolov8n.pt")  # General object detection model
model_custom = YOLO("../Yolo-Weights/guns8n.pt")     # Custom model for guns

# Class names for detection (general model)
classNames_general = [
    "car", "motorbike"
]

# Class names for the custom model (if available)
classNames_custom = []  # Adjust based on your custom model's training classes

# Extended weapon classes
weapon_classes = []

# Set email cooldown time in seconds
cooldown_time = 5
last_email_time = 0  # Track last email send time

# Variables for FPS calculation
prev_frame_time = 0

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    new_frame_time = time.time()

    # Run inference on both models
    results_general = model_general(img)  # General model detection
    results_custom = model_custom(img)    # Custom model detection

    # Process results from the general model
    for r in results_general:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            if w > 0 and h > 0:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Rectangle in green for general model
                conf = box.conf[0].item()
                cls = int(box.cls[0])

                if 0 <= cls < len(classNames_general):
                    class_name = classNames_general[cls]
                    cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    # Check cooldown for email alerts
                    current_time = time.time()
                    if class_name in weapon_classes and conf > 0.7 and current_time - last_email_time > cooldown_time:
                        send_email_alert(class_name, conf)
                        last_email_time = current_time  # Update last email send time

    # Process results from the custom model
    for r in results_custom:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            if w > 0 and h > 0:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Rectangle in blue for custom model
                conf = box.conf[0].item()
                cls = int(box.cls[0])

                if 0 <= cls < len(classNames_custom):
                    class_name = classNames_custom[cls]
                    cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                    # Check cooldown for email alerts
                    current_time = time.time()
                    if class_name in weapon_classes and conf > 0.7 and current_time - last_email_time > cooldown_time:
                        send_email_alert(class_name, conf)
                        last_email_time = current_time  # Update last email send time

    # Calculate FPS
    fps = 1 / (new_frame_time - prev_frame_time) if new_frame_time - prev_frame_time > 0 else 0
    prev_frame_time = new_frame_time
    print(f"FPS: {fps:.2f}")

    # Display the image
    cv2.imshow("Image", cv2.resize(img, (640, 480)))  # Resize for display performance
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()