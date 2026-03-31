# 🛡️ Project: Vehicle Proximity ADAS
**Advanced Driver Assistance System with OpenVINO Optimization & Forensic Logging**

## 📌 Project Overview
This project presents a real-time Advanced Driver Assistance System (ADAS) designed to enhance road safety through AI-based vehicle proximity and pre-collision detection by effectively serving as a low-cost safety tool for older vehicle models. It utilizes a smartphone's camera as a high-definition webcam to capture live road data. By leveraging the YOLOv8 architecture (optimized via the Intel OpenVINO toolkit) and Mobile-to-Server video stream integration, the system detects critical road entities such as vehicles and pedestrians with high precision and low latency on consumer-grade hardware. The system incorporates Dynamic Spatial Calibration and Geometric Distance Estimation to identify collision risks. Significant features of this work are the Auditory/visual alerts triggered when an object enters the "High Proximity" zones and a Data Persistence Layer utilizing SQLite to log high-risk incidents, providing a "Digital Black Box" capability for post-event forensic analysis.


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

## 📊 Mathematical Foundations

The system utilizes the **Pinhole Camera Model** for distance estimation:

                          d = (f . H) / p

* **$d$ (Distance):** Estimated distance from the camera to the object in meters.
* **$f$ (Focal Length):** Calibrated camera constant in pixels> 
* **$H$ (Real-World Height):** The assumed physical height of the object (e.g., 1.7m for a person or 1.5m for a car).
* **$p$ (Pixel Height):** The vertical height of the detection bounding box.

---

## 📈 Performance & Accuracy

Through Intel OpenVINO FP16 Quantization, the model achieves a significant performance leap over standard inference methods.

* **Optimization Impact:** Achieved a ~70% reduction in latency compared to the original .pt model (which averaged 5–8 FPS). 
* **Inference Latency:** 35ms – 47ms per frame (Hardware: Consumer-grade CPU). 
* **Real-Time Throughput:** 21 FPS – 28 FPS. 
* **Distance Accuracy:** Validated via iterative calibration of the Pinhole Camera Model, achieving a functional Mean Absolute Error (MAE) of < 10% within the critical safety range (2m–15m). Accuracy was verified against static ground-truth markers. 

### **Drawbacks**

While the system maintains high functional reliability, users should account for standard computer vision variances: 

* **Bounding Box Jitter:** Small pixel fluctuations in the AI bounding box affect the denominator ($p$), leading to minor distance variances. 
* **Vehicle Pitch & Roll:** Road bumps or braking can alter the camera angle relative to the horizon, slightly distorting the perceived object height. 
* **Pixel Resolution Constraints:** At 640x480 resolution, distant objects occupy fewer pixels; a 1-pixel detection error at 20m is mathematically more significant than at 2m. 

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


### Made by Huda Naaz  