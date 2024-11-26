import cv2
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from utils import category_names


def get_label_from_id(category_id):
    """
    Convert a category number to its corresponding label.
    """
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
