import cv2
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F


def get_label_from_id(category_id):
    """
    Convert a category number to its corresponding label.
    """
    category_names = {
        0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane", 5: "bus",
        6: "train", 7: "truck", 8: "boat", 9: "traffic light", 10: "fire hydrant",
        11: "stop sign", 12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
        16: "dog", 17: "horse", 18: "sheep", 19: "cow", 20: "elephant", 21: "bear",
        22: "zebra", 23: "giraffe", 24: "backpack", 25: "umbrella", 26: "handbag",
        27: "tie", 28: "suitcase", 29: "frisbee", 30: "skis", 31: "snowboard",
        32: "sports ball", 33: "kite", 34: "baseball bat", 35: "baseball glove",
        36: "skateboard", 37: "surfboard", 38: "tennis racket", 39: "bottle",
        40: "wine glass", 41: "cup", 42: "fork", 43: "knife", 44: "spoon", 45: "bowl",
        46: "banana", 47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli",
        51: "carrot", 52: "hot dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair",
        57: "couch", 58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet",
        62: "tv", 63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard",
        67: "cell phone", 68: "microwave", 69: "oven", 70: "toaster", 71: "sink",
        72: "refrigerator", 73: "book", 74: "clock", 75: "vase", 76: "scissors",
        77: "teddy bear", 78: "hair drier", 79: "toothbrush"
    }
    return category_names.get(category_id, "unknown")

class RCNNDetector:
    def __init__(self, device='cpu', conf_thresh=0.5):
        """
        Initialize the Faster R-CNN
        """
        self.device = torch.device(device)
        self.conf_thresh = conf_thresh
        self.model = fasterrcnn_resnet50_fpn(pretrained=True)
        self.model.to(self.device)
        self.model.eval()

    def preprocess(self, image):
        """
        Preprocess an image for the model
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        return F.to_tensor(image).to(self.device)

    def postprocess(self, outputs):
        """
        Filter predictions by confidence
        """
        results = []
        for box, score, label in zip(outputs['boxes'], outputs['scores'], outputs['labels']):
            if score >= self.conf_thresh:
                results.append({
                    "bbox": box.cpu().numpy().tolist(),
                    "score": float(score.cpu().numpy()),
                    "label": get_label_from_id(int(label.cpu().numpy()))
                })
        return results

    def predict(self, images):
        """
        Predict bounding boxes for images
        """
        tensors = [self.preprocess(image) for image in images]
        with torch.no_grad():
            outputs = self.model(tensors)
        return [self.postprocess(output) for output in outputs]
