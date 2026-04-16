# 🚨 Object Detection for Smart Surveillance System (YOLOv8)

## 📌 Overview
This project presents a Smart Surveillance System that uses YOLO (You Only Look Once) for real-time object detection and threat identification.  

The system is designed to automatically detect dangerous objects like **guns and knives** and send instant email alerts to authorities.

It eliminates the need for continuous human monitoring and improves **security, efficiency, and response time**.

---

## 🎯 Features
- 🔍 Real-time object detection using YOLOv8  
- 🔫 Custom weapon detection (guns, knives)  
- 📧 Automated email alert system  
- 🎥 Live video stream processing using OpenCV  
- ⚡ High-speed detection (~30 FPS)  
- 🧠 Dual-model architecture (General + Custom YOLO)  

---

## 🛠️ Tech Stack

| Category            | Technologies Used |
|--------------------|------------------|
| Programming        | Python |
| Computer Vision    | OpenCV |
| Object Detection   | YOLOv8 (Ultralytics) |
| Visualization      | cvzone |
| Alerts             | SMTP (Email) |
| Libraries          | NumPy, time |

---

## 🧠 System Architecture
- 📷 Capture live video from CCTV / webcam  
- 🧠 Process frames using YOLO models  
- 🎯 Detect objects + weapons  
- ⚠️ Identify threats with confidence score  
- 📧 Send alert email if threat detected  

---
Start
↓
Capture Video
↓
Run YOLO Detection
↓
Weapon Detected?
↓ ↓
Yes No
↓ ↓
Send Email Continue Monitoring
↓
End

---

## 🤖 Models Used

### 1. General Object Detection
- Pretrained YOLOv8 model (`yolov8l.pt`)  
- Detects multiple objects in real-time  

### 2. Custom Weapon Detection Model
- Trained on weapon dataset (guns, knives)  
- High precision (~95% accuracy)  

---

## 📊 Results
- ✅ Detection Accuracy: ~95% (weapon detection)  
- ⚡ Real-Time Performance: ~30 FPS  
- 📧 Instant email alerts on threat detection  
- 🌗 Works in different lighting conditions  

---

## 📂 Project Structure

models/
├── yolov8l.pt
├── guns8l.pt
app.py
utils/
dataset/
requirements.txt
README.md

---

## ⚙️ Installation
```bash
git clone https://github.com/ravikumar8709/Object-detection-for-smart-surveillance-system.git
cd smart-surveillance-yolo
pip install -r requirements.txt

## 🔄 Workflow
▶️ Usage
python app.py

Press 'q' to exit.

📧 Email Configuration
sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
password = "your_app_password"
⚠️ Limitations
Depends on video quality
Needs good hardware
Initial setup is complex
Privacy concerns
👨‍💻 Author

Ravi Kumar

