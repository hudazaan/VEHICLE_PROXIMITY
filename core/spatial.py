
import cv2
import numpy as np
import config
import os

class SpatialAnalyzer:
    def __init__(self):
        self.w, self.h = 640, 480
        self.calib_file = "logs/calibration_points.npy"
        self.focal_length = 600  # calibration constant for distance

        # Room Test Mode: set to True for testing with a 0.25m object (like a bottle) and set to False when outside for real cars (1.5m)
        self.TEST_MODE = True
        
        # load or fallback
        if os.path.exists(self.calib_file):
            self.pts = np.load(self.calib_file)
        else:
            self.pts = np.array([[int(p[0]*self.w), int(p[1]*self.h)] for p in config.ROI_POLYGON], np.int32)
        
        self.selected_point = -1

    def update_frame_size(self, w, h):
        if w != self.w or h != self.h:
            scale_x, scale_y = w / self.w, h / self.h
            self.pts = (self.pts * [scale_x, scale_y]).astype(np.int32)
            self.w, self.h = w, h

    def estimate_distance(self, label, pixel_height):
        # d = (Real H * Focal) / Pixel H
        if self.TEST_MODE:
            real_height = 0.25 
        else:
            heights = {"person": 1.7, "car": 1.5, "truck": 3.5, "bus": 3.5}
            real_height = heights.get(label, 1.5)
            
        distance = (real_height * self.focal_length) / max(pixel_height, 1)
        return round(distance, 1)

    def get_risk_level(self, label, distance):
        """ 
        Risk Profile Calibration:
        Heavier objects (Trucks/Buses) have longer braking distances.
        """
        # thresholds based on object type
        if self.TEST_MODE:
            critical_zone, warning_zone = 0.5, 1.5 # 0.5m for Red, 1.5m for Yellow
        else:
            # road thresholds
            if label in ["truck", "bus"]:
                critical_zone = 7.0  # beep earlier for heavy vehicles
                warning_zone = 15.0
            else:
                critical_zone = 4.0  # standard for cars/people
                warning_zone = 10.0

        if distance <= critical_zone:
            return "CRITICAL", (0, 0, 255) # Red
        elif distance <= warning_zone:
            return "WARNING", (0, 255, 255) # Yellow/Amber
        else:
            return "SAFE", (0, 255, 0) # Green

    def handle_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i in range(4):
                if np.linalg.norm(self.pts[i] - [x, y]) < 20:
                    self.selected_point = i
                    break
        elif event == cv2.EVENT_MOUSEMOVE and self.selected_point != -1:
            self.pts[self.selected_point] = [x, y]
        elif event == cv2.EVENT_LBUTTONUP:
            if self.selected_point != -1:
                np.save(self.calib_file, self.pts)
            self.selected_point = -1

    def is_in_danger_zone(self, point):
        return cv2.pointPolygonTest(self.pts, point, False) >= 0

    def draw_zones(self, frame):
        overlay = frame.copy()
        cv2.fillPoly(overlay, [self.pts], (0, 0, 255))
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        cv2.polylines(frame, [self.pts], True, (0, 255, 255), 2)
        for p in self.pts:
            cv2.circle(frame, tuple(p), 5, (255, 255, 255), -1)