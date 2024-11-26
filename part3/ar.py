import cv2
import numpy as np
from drawing import draw_bounding_box, highlight_object


def process_frame(frame, detections):
    """
    Process a single frame with object detection results.
    Args:
        frame (ndarray): Current video frame.
        detections (list): List of detection results with bbox, label, and confidence.
    Returns:
        ndarray: Processed frame with AR effects.
    """
    # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    for detection in detections:
        bbox = detection["bbox"]
        label = detection["label"]  # Already resolved by `get_label_from_id`
        confidence = detection["score"]

        # Highlight detected object
        highlight_object(frame, bbox)

        # Draw bounding box and label
        draw_bounding_box(frame, bbox, label, confidence)

    # Apply background blur
    return frame
