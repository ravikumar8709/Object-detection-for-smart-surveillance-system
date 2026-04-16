# 🚨 Smart Surveillance System using YOLOv8

## 📌 Overview

This project implements a **real-time Smart Surveillance System** that leverages **YOLOv8** for object detection and automated threat monitoring.

The system detects potentially dangerous objects such as **guns and knives** and generates **structured security alerts** with metadata (timestamp, confidence score, threat level). Alerts are automatically sent via email, enabling rapid response without continuous human supervision.

---

## 🎯 Key Features

* 🔍 **Real-time object detection** using YOLOv8
* 🔫 **Custom weapon detection** (guns, knives)
* 🚨 **Automated alert generation system**
* 📧 **Email notifications with structured alerts**
* 🕒 **Timestamp + confidence-based reporting**
* 🎥 **Live video stream processing (OpenCV)**
* ⚡ **High-speed inference (~30 FPS)**
* 🧠 **Rule-based threat classification (HIGH / MEDIUM / LOW)**
* 🧩 **Modular architecture (detection, alerting, utilities)**

---

## 🛠️ Tech Stack

| Category         | Technologies Used    |
| ---------------- | -------------------- |
| Programming      | Python               |
| Computer Vision  | OpenCV               |
| Object Detection | YOLOv8 (Ultralytics) |
| Visualization    | cvzone               |
| Alerts           | SMTP (Email)         |
| Utilities        | dotenv, datetime     |
| Libraries        | NumPy, time          |

---

## 🧠 System Architecture

```
📷 Video Input (Webcam/CCTV)
        ↓
🧠 YOLO Detection (General + Weapon Model)
        ↓
🎯 Object Classification + Confidence Score
        ↓
⚠️ Threat Evaluation (Rule-Based Logic)
        ↓
📧 Alert Generation (Structured Format)
        ↓
🚨 Email Notification Sent
```

---

## 🤖 Models Used

### 1. General Object Detection

* YOLOv8 pretrained model (`yolov8n.pt` / `yolov8l.pt`)
* Detects common objects (person, vehicle, etc.)

### 2. Custom Weapon Detection

* Custom-trained YOLO model (`guns8n.pt` / `guns8l.pt`)
* Focused on detecting:

  * 🔫 Guns
  * 🔪 Knives

---

## 📊 Results

* ✅ **Weapon Detection Accuracy**: ~95%
* ⚡ **Real-Time Performance**: ~30 FPS
* 📧 **Instant alert generation and delivery**
* 🌗 Robust performance under varying lighting conditions

---

## 📂 Project Structure

```
project/
│
├── main.py          # Main execution file
├── detection.py     # YOLO detection logic
├── alert.py         # Alert creation + email system
├── utils.py         # Helper functions (time, threat level, ID)
├── yolo-weights/    # Model weights
├── .env             # Environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/ravikumar8709/Object-detection-for-smart-surveillance-system.git
cd Object-detection-for-smart-surveillance-system
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python main.py
```

Press **'q'** to exit the application.

---

## 📧 Email Configuration

Create a `.env` file:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

> ⚠️ Use Gmail App Passwords (not your actual password)

---

## 🚨 Sample Alert Output

```
🚨 Smart Surveillance Alert

Alert ID: A1B2C3D4
Date: 2026-04-16
Time: 23:01:43

Object: Gun
Confidence: 69.06%

Threat Level: HIGH

Message:
A Gun has been detected with high confidence.

Action:
Call security immediately.
```

---

## ⚠️ Limitations

* Performance depends on hardware capabilities
* Accuracy depends on training dataset quality
* May struggle in extremely low-light or occluded environments
* Requires proper camera positioning for optimal detection
* Privacy considerations in real-world deployment

---

## 🚀 Future Improvements

* 📊 Web dashboard for monitoring alerts
* 🗂️ Logging system (database integration)
* 📱 SMS / WhatsApp alert integration
* 🧠 AI-based threat analysis (LLM / RAG integration)
* ☁️ Cloud deployment for scalability

---

## 👨‍💻 Author

**Ravi Kumar**
🎓 B.Tech Graduate – AI/ML Enthusiast
💡 Interested in Computer Vision, Deep Learning & Intelligent Systems

---
