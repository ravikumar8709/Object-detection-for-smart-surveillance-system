import os
import time
import cv2
import cvzone
import smtplib
from ultralytics import YOLO
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from transformers import pipeline   # ✅ CHANGED (Hugging Face)

# ---------------- LOAD ENV ---------------- #
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# ---------------- FREE LLM (Hugging Face) ---------------- #
print("Loading FREE LLM model... (first run may take time)")
generator = pipeline("text-generation", model="gpt2")

def generate_alert_with_llm(object_name, confidence):
    try:
        # 🔥 Get current date & time
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time_now = now.strftime("%H:%M:%S")

        # 🔥 Threat logic
        if object_name.lower() == "gun":
            level = "HIGH"
            action = "Call security immediately."
        elif object_name.lower() == "knife":
            level = "MEDIUM"
            action = "Monitor closely and alert authorities if needed."
        else:
            level = "LOW"
            action = "No immediate threat. Continue monitoring."

        # ✅ FINAL CLEAN ALERT
        return f"""
🚨 Smart Surveillance Alert

Date: {date}
Time: {time_now}

Object: {object_name}
Confidence: {confidence*100:.2f}%

Threat Level: {level}

Message:
A {object_name} has been detected with {confidence*100:.2f}% confidence.

Action:
{action}
"""

    except Exception as e:
        print("Alert Error:", e)
        return f"{object_name} detected"

# ---------------- EMAIL FUNCTION ---------------- #
def send_email_alert(body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    msg['Subject'] = "🚨 Smart Surveillance Alert"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Email error: {e}")

# ---------------- LOAD MODELS ---------------- #
model_general = YOLO("Yolo-Weights/yolov8n.pt")
model_weapon = YOLO("yolo-weights/guns8n.pt")

# ---------------- CLASSES ---------------- #
classNames_general = [
    "person","bicycle","car","motorbike","bus","train","truck","boat",
    "traffic light","fire hydrant","stop sign","bench","bird","cat",
    "dog","horse","sheep","cow","elephant","bear","zebra","giraffe"
]

weapon_classes = ["Gun", "knife"]

# ---------------- SETTINGS ---------------- #
EMAIL_INTERVAL = 15
last_email_time = 0

# ---------------- CAMERA ---------------- #
cap = cv2.VideoCapture(0)
prev_time = 0

while True:
    success, img = cap.read()
    if not success:
        break

    current_time = time.time()

    # -------- GENERAL DETECTION -------- #
    results_general = model_general(img, stream=True)

    for r in results_general:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            if cls < len(classNames_general):
                class_name = classNames_general[cls]

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cvzone.putTextRect(img, f'{class_name} {conf:.2f}',
                                   (max(0, x1), max(35, y1)))

    # -------- WEAPON DETECTION -------- #
    results_weapon = model_weapon(img, stream=True)

    for r in results_weapon:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            class_name = weapon_classes[cls]

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cvzone.putTextRect(img, f'⚠ {class_name} {conf:.2f}',
                               (max(0, x1), max(35, y1)),
                               scale=1, thickness=2)

            # -------- FREE LLM + EMAIL -------- #
            if conf > 0.6 and time.time() - last_email_time > EMAIL_INTERVAL:
                alert_text = generate_alert_with_llm(class_name, conf)
                send_email_alert(alert_text)
                last_email_time = time.time()

    # -------- FPS -------- #
    fps = 1 / (current_time - prev_time) if current_time - prev_time > 0 else 0
    prev_time = current_time

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("🔥 Smart Surveillance (FREE LLM)", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
