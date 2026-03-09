# 🛡️ Project: Vehicle Proximity ADAS
**Advanced Driver Assistance System with OpenVINO Optimization & Forensic Logging**

## 📌 Project Overview
This project is an AI-powered This project presents a real-time Advanced Driver Assistance System (ADAS) designed to enhance road safety through AI-based vehicle proximity and pre-collision detection by effectively serving as a low-cost safety tool for older vehicle models. It utilizes a smartphone's camera as a high-definition webcam to capture live road data. By leveraging the YOLOv8 architecture (optimized via the Intel OpenVINO toolkit) and Mobile-to-Server video stream integration, the system detects critical road entities such as vehicles and pedestrians with high precision and low latency on consumer-grade hardware. The system incorporates Dynamic Spatial Calibration and Geometric Distance Estimation to identify collision risks. Significant features of this work are the Auditory/visual alerts triggered when an object enters the "High Proximity" zones and a Data Persistence Layer utilizing SQLite to log high-risk incidents, providing a "Digital Black Box" capability for post-event forensic analysis.


### **Core Features**
* **Intelligent Object Filtering:** Optimized to specifically track Persons, Cars, Motorcycles, Buses, and Trucks while filtering out irrelevant background noise.
* **Dynamic Spatial Calibration:** Interactive mouse-driven GUI allowing users to define the "Danger Zone" (ROI) trapezoid based on specific camera mounting angles.
* **Real-Time Telemetry:**  Real-time distance calculation in meters based on object pixel height and camera focal length.
* **Active Alert System:** Visual HUD status changes and auditory beeps upon ROI breach.
* **Multi-Tiered Warning System:** Dynamic HUD color-coding (Green: Safe, Yellow: Caution, Red: Critical) based on calculated distance thresholds.
* **Mass-Based Risk Profiling:** Intelligent alert logic that triggers earlier for heavy vehicles (Trucks/Buses) to account for higher momentum and braking distances.
* **Digital Black Box (Forensics):** SQLite3-backed incident logging that automatically exports a professional `forensic_report.csv` upon session termination.
* **Performance Analytics:** Integrated benchmarking using **Pandas** and **Matplotlib** to track system latency and detection frequency.

---

## ⚙️ Technical Stack
* **AI Engine:** Ultralytics YOLOv8 (OpenVINO FP16 Quantized)
* **Inference:** Intel OpenVINO Toolkit
* **Computer Vision:** OpenCV (Spatial Geometry & HUD)
* **Data Science:** Pandas (Data Wrangling), Matplotlib (Performance Plotting)
* **Database:** SQLite3 (Relational Incident Telemetry)
* **Protocol:** IP Webcam (HTTP/JPEG Stream)

---

## 🛠️ Installation & Setup

### **1. Environment Configuration**
Ensure Python 3.10+ is installed. Create and activate your virtual environment:
```bash
# Create the environment
python -m venv proxi_venv

# Activate the environment (Windows)
proxi_venv\Scripts\activate
```

### **2. Dependency Installation** 
Install the optimized library stack:
```bash
pip install ultralytics openvino-dev opencv-python pandas matplotlib 
```

### **3. Model Weights**
This project uses an optimized **OpenVINO FP16** version of YOLOv8n. To keep the repository lightweight, these binary files are hosted in the **Releases** section.

1. Download the `yolov8n_openvino_model.zip` from [Releases](../../releases).
2. Extract the contents into the `models/` directory.

---

## 🚀 Execution Guide

1.  **Initialize Camera:** Start the **IP Webcam** app on your mobile device and select **"Start Server"**.
2.  **Verify Configuration:** Update the `CAMERA_URL` in `config.py` to match the IP provided by the app (e.g., `http://192.168.x.x:8080/video`).
3.  **Launch System:**
    ```bash
    python main.py
    ```
4.  **Calibrate ROI:** During the live feed, use the mouse to drag the 4 white anchor points. Align the **Red Trapezoid** to cover your specific driving lane/path.
5.  **Shutdown & Report:** Press **'q'** to exit. The system will automatically trigger a database dump and save `logs/forensic_report.csv` along with a performance summary graph.

---

## 📊 Mathematical Foundations

The system utilizes the **Pinhole Camera Model** for distance estimation:

                    $$d = \frac{f \cdot H}{p}$$

* **$d$ (Distance):** The estimated distance from the camera to the object in meters.
* **$f$ (Focal Length):** A constant representing the camera’s focal length in pixels, calibrated for the IP Webcam lens.
* **$H$ (Real-World Height):** The assumed physical height of the object (e.g., 1.7m for a person or 1.5m for a car).
* **$p$ (Pixel Height):** The vertical height of the bounding box as detected by the AI in the current frame.

---

### Made by Huda Naaz  