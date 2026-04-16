# 🚨 Smart Surveillance System using YOLOv8 + Groq LLM

## 📌 Overview

This project implements a **real-time AI-powered Smart Surveillance System** that leverages **YOLOv8** for object detection and **Groq LLM (LLaMA 3.1)** for intelligent threat analysis.

The system detects potentially dangerous objects such as **guns and knives**, generates **AI-analyzed security alerts** with metadata (timestamp, confidence score, threat level), and automatically sends them via email — enabling rapid response without continuous human supervision.

---

## 🎯 Key Features

* 🔍 **Real-time object detection** using YOLOv8
* 🔫 **Custom weapon detection** (guns, knives)
* 🧠 **AI-powered threat analysis** using Groq LLM (LLaMA 3.1)
* 🚨 **Automated intelligent alert generation**
* 📧 **Email notifications with AI-analyzed alerts**
* 🕒 **Timestamp + confidence-based reporting**
* 🎥 **Live video stream processing (OpenCV)**
* ⚡ **High-speed inference (~30 FPS)**
* 🔁 **Rule-based fallback if LLM is unavailable**
* 🧩 **Modular architecture (detection, alerting, utilities)**

---

## 🛠️ Tech Stack

| Category         | Technologies Used            |
| ---------------- | ---------------------------- |
| Programming      | Python                       |
| Computer Vision  | OpenCV                       |
| Object Detection | YOLOv8 (Ultralytics)         |
| Visualization    | cvzone                       |
| LLM / AI         | Groq API (LLaMA 3.1-8b)      |
| Alerts           | SMTP (Email)                 |
| Utilities        | dotenv, datetime, pathlib    |
| Libraries        | NumPy, time                  |

---

## 🧠 System Architecture

```
📷 Video Input (Webcam/CCTV)
        ↓
🧠 YOLO Detection (General + Weapon Model)
        ↓
🎯 Object Classification + Confidence Score
        ↓
🤖 Groq LLM Threat Analysis (LLaMA 3.1-8b-instant)
        ↓
⚠️ AI-Generated Alert (Threat Level + Action + Reasoning)
        ↓
📧 Email Notification Sent
        ↓
🔁 Rule-Based Fallback (if LLM unavailable)
```

---

## 🤖 Models Used

### 1. General Object Detection

* YOLOv8 pretrained model (`yolov8n.pt`)
* Detects common objects (person, vehicle, etc.)

### 2. Custom Weapon Detection

* Custom-trained YOLO model (`guns8n.pt`)
* Focused on detecting:
  * 🔫 Guns
  * 🔪 Knives

### 3. Groq LLM — LLaMA 3.1-8b-instant

* Analyzes detected threats in real-time
* Generates professional security alert messages
* Provides threat level assessment and recommended actions
* Falls back to rule-based logic if API is unavailable

---

## 📊 Results

* ✅ **Weapon Detection Accuracy**: ~95%
* ⚡ **Real-Time Performance**: ~30 FPS
* 🧠 **AI-generated detailed threat analysis per detection**
* 📧 **Instant alert generation and email delivery**
* 🌗 **Robust performance under varying lighting conditions**

---

## 📂 Project Structure

```
project/
│
├── objectdetection.py   # Main execution file (detection + LLM + email)
├── yolo-weights/        # Model weights (yolov8n.pt, guns8n.pt)
├── .env                 # Environment variables (API keys, email)
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
python objectdetection.py
```

Press **'q'** to exit the application.

---

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
```

> ⚠️ Use Gmail App Passwords (not your actual Gmail password)
> 🔑 Get your free Groq API key at: https://console.groq.com

---

## 🚨 Sample Alert Output

```
🚨 SMART SURVEILLANCE ALERT 🚨

Date: 2026-04-17
Time: 01:47:49

Object: Gun
Confidence: 86.34%

--- AI ANALYSIS ---
THREAT LEVEL: HIGH

A firearm has been detected within the monitored area with high
confidence. This poses an immediate risk to personnel and property.
The presence of a weapon in this location is unauthorized and
requires immediate intervention.

RECOMMENDED ACTION:
→ Alert security personnel immediately
→ Initiate lockdown protocol if applicable
→ Contact law enforcement if situation escalates
→ Do not approach the subject without proper backup
```

---

## ⚠️ Limitations

* Performance depends on hardware capabilities
* Accuracy depends on training dataset quality
* May struggle in extremely low-light or occluded environments
* Requires proper camera positioning for optimal detection
* Groq API requires internet connection (falls back to rule-based if offline)
* Privacy considerations in real-world deployment

---

## 🚀 Future Improvements

* 📊 Web dashboard for real-time monitoring
* 🗂️ Database logging system for all alerts
* 📱 SMS / WhatsApp alert integration
* 🧠 RAG-based threat history analysis
* ☁️ Cloud deployment for scalability
* 📷 Multi-camera support (CCTV integration)

---

## 👨‍💻 Author

**Ravi Kumar**
🎓 B.Tech Graduate — AI/ML Enthusiast
💡 Interested in Computer Vision, Deep Learning & Intelligent Systems
🔗 GitHub: [ravikumar8709](https://github.com/ravikumar8709)

---
