
import cv2
import time
import config
import threading
from core.detector import RoadDetector
from core.spatial import SpatialAnalyzer
from utils.alerts import Alerter
from utils.logger import DataLogger
from utils.database import IncidentDB
from utils.analytics import generate_session_summary

class VideoStream:
    def __init__(self, url):
        self.url = url
        self.cap = cv2.VideoCapture(self.url)
        self.ret, self.frame = False, None
        self.stopped = False
       
    def read(self):
        self.ret, self.frame = self.cap.read()
        return self.ret, self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()

def main():
    # initialized Components
    detector = RoadDetector(model_path="models/yolov8n_openvino_model")
    spatial = SpatialAnalyzer() 
    alerter = Alerter()
    logger = DataLogger()
    db = IncidentDB()
    
    # threaded Stream
    stream = VideoStream(config.CAMERA_URL)
    time.sleep(2) # Buffer time

    alert_counter = 0
    print(f"--- ADAS SYSTEM LIVE: {config.CAMERA_URL} ---")

    cv2.namedWindow("ADAS Demo")
    cv2.setMouseCallback("ADAS Demo", spatial.handle_mouse)

    try:
        while True:
            ret, frame = stream.read()
            if not ret or frame is None:
                stream.cap.release()
                stream.cap = cv2.VideoCapture(config.CAMERA_URL)
                continue

            start_time = time.time()
            # dynamic ROI scaling based on frame size
            spatial.update_frame_size(frame.shape[1], frame.shape[0])

            # AI detection
            results = detector.get_detections(
                frame, 
                classes=config.TARGET_CLASSES, 
                conf=config.CONFIDENCE_THRESHOLD
            )
            
            collision_detected = False
            detected_label = "None"
            max_conf = 0.0
            current_dist = 0.0
            
            # process Detections
            if results and len(results[0].boxes) > 0:
                for box in results[0].boxes:
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    
                    # check if object is in our TARGET_CLASSES (0, 2, 3, 5, 7)
                    if cls_id not in config.TARGET_CLASSES:
                        continue
                        
                        [0, 2, 3, 5, 7]  # Person, Car, Motorcycle, Bus, Truck
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    label = results[0].names[cls_id]
                    
                    # distance math
                    pixel_height = y2 - y1
                    dist_m = spatial.estimate_distance(label, pixel_height)

                    risk_text, risk_color = spatial.get_risk_level(label, dist_m)

                    # bottom-center of bounding box for ROI test
                    det_point = (int((x1 + x2) / 2), int(y2))
                    in_zone = spatial.is_in_danger_zone(det_point)
                    
                    # check if point is inside the Trapezoid
                    if in_zone or risk_text == "CRITICAL":
                        collision_detected = True
                        detected_label = label
                        max_conf = conf
                        current_dist = dist_m # capture for DB log
                        current_risk = "CRITICAL" # force critical for DB if in zone
                        active_risk_color = (0, 0, 255) # red for HUD status

                        # red bounding box for danger
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), risk_color, 3)
                        cv2.putText(frame, f"{risk_text}: {label.upper()} {dist_m}m", 
                                    (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, risk_color, 2)
                    else:
                        # green bounding box for safe
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), risk_color, 1)
                        cv2.putText(frame, f"{dist_m}m", (int(x1), int(y1)-5), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # alert & database Logic
            if collision_detected:
                alert_counter += 1
                if alert_counter == 2: 
                    if risk_text == "CRITICAL":
                        alerter.trigger_collision_warning()
                    db.save_incident(detected_label, max_conf, f"{current_dist}m - {risk_text}")
            else:
                alert_counter = 0

            # UI rendering (HUD)
            latency_ms = (time.time() - start_time) * 1000
            spatial.draw_zones(frame)

            # HUD top bar
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], 60), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

            # status and REC icon
            status_text = "SYSTEM ACTIVE" if not collision_detected else "!! COLLISION WARNING !!"
            status_color = (0, 255, 0) if not collision_detected else (0, 0, 255)
            cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, status_color, 2)
            
            cv2.putText(frame, f"{latency_ms:.1f}ms", (frame.shape[1]-180, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            if int(time.time()) % 2 == 0: # blinking REC dot
                cv2.circle(frame, (frame.shape[1]-30, 30), 8, (0, 0, 255), -1)

            logger.log_frame(latency_ms, "YES" if alert_counter >= 2 else "NO")
            cv2.imshow("ADAS Demo", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        stream.stop()
        cv2.destroyAllWindows()
        db.export_to_csv()

        generate_session_summary()

if __name__ == "__main__":
    main()