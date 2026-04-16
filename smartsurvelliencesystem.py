import os
import time
import cv2
import cvzone
import smtplib
from pathlib import Path
from ultralytics import YOLO
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- LOAD ENV ---------------- #
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("✅ GROQ KEY loaded:", bool(GROQ_API_KEY))

client = Groq(api_key=GROQ_API_KEY)

# ---------------- LLM FUNCTION (Groq) ---------------- #
def generate_alert_with_llm(object_name, confidence):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    prompt = f"""
You are an AI-based smart surveillance system.

A suspicious object has been detected by our security cameras.

Object Detected: {object_name}
Detection Confidence: {confidence*100:.2f}%
Date: {date}
Time: {time_now}

Your task:
- Analyze the threat level realistically (HIGH / MEDIUM / LOW)
- Explain why this object is dangerous in this context
- Write a professional security alert message
- Suggest immediate action for security personnel

Be specific, realistic, and professional. Do NOT be generic.
    """

    try:
        print("🔍 Calling Groq LLM...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        llm_message = response.choices[0].message.content
        print("✅ LLM response received!")

        return f"""
🚨 SMART SURVEILLANCE ALERT 🚨

Date: {date}
Time: {time_now}
Object: {object_name}
Confidence: {confidence*100:.2f}%

--- AI ANALYSIS ---
{llm_message}
"""

    except Exception as e:
        print("❌ LLM error:", e)

        if object_name.lower() == "gun":
            level = "HIGH"
            action = "Call security immediately. Evacuate the area."
        elif object_name.lower() == "knife":
            level = "MEDIUM"
            action = "Alert nearby personnel. Monitor closely."
        else:
            level = "LOW"
            action = "Continue monitoring the area."

        return f"""
🚨 SMART SURVEILLANCE ALERT 🚨

Date: {date}
Time: {time_now}
Object: {object_name}
Confidence: {confidence*100:.2f}%

Threat Level: {level}
Message: A {object_name} has been detected on camera.
Action: {action}
"""

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
        print("❌ Email error:", e)

# ---------------- LOAD MODELS ---------------- #
model_general = YOLO("Yolo-Weights/yolov8n.pt")
model_weapon = YOLO("yolo-weights/guns8n.pt")

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

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cvzone.putTextRect(img, f'{cls} {conf:.2f}',
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

            # -------- LLM + EMAIL -------- #
            if conf > 0.6 and time.time() - last_email_time > EMAIL_INTERVAL:
                alert_text = generate_alert_with_llm(class_name, conf)
                send_email_alert(alert_text)
                last_email_time = time.time()

    # -------- FPS -------- #
    fps = 1 / (current_time - prev_time) if current_time - prev_time > 0 else 0
    prev_time = current_time

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("🔥 Smart Surveillance (Groq LLM)", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
