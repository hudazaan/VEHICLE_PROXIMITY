
from ultralytics import YOLO

class RoadDetector:
    def __init__(self, model_path):
        # load the OpenVINO model correctly
        self.model = YOLO(model_path, task='detect') 
        print(f"--- Model Loaded: {model_path} ---")

    def get_detections(self, frame, classes, conf):
        return self.model.predict(
            source=frame,
            classes=classes,
            conf=conf,
            verbose=False,
            device='cpu'  # OpenVINO runs on CPU
        )