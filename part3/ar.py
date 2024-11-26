from drawing import draw_bounding_box, highlight_object


def process_frame(frame, detections):
    """
    Process a single frame with object detection results.
    """
    for detection in detections:
        bbox = detection["bbox"]
        label = detection["label"]  # Already resolved by `get_label_from_id`
        if not label in ['person', 'train', 'fork']: continue
        confidence = detection["score"]

        # Highlight detected object
        highlight_object(frame, bbox)

        # Draw bounding box and label
        draw_bounding_box(frame, bbox, label, confidence)

    # Apply background blur
    return frame
