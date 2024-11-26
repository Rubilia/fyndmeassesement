import cv2

def draw_bounding_boxes(image, detections, class_labels=None):
    """
    Draw bounding boxes and labels on an image
    """
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection['bbox'])
        score = detection['score']
        label = detection['label']
        
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label_text = f"{class_labels[label] if class_labels else label}: {score:.2f}"
        cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return image
