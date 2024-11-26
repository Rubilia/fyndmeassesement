import cv2
from utils import get_color_for_category, scale_font_size


def draw_bounding_box(image, bbox, label, confidence):
    """
    Draw bounding box, label, and confidence on the image
    """
    x1, y1, x2, y2 = map(int, bbox)
    color = get_color_for_category(label)
    font_scale = scale_font_size(bbox)

    # Draw the bounding box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    # Prepare and draw the label text
    text = f"{label}: {confidence:.2f}"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)[0]
    text_x, text_y = x1, y1 - 10 if y1 - 10 > 0 else y1 + 10
    cv2.rectangle(image, (text_x, text_y - text_size[1] - 4),
                  (text_x + text_size[0] + 4, text_y + 4), color, -1)
    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)


def highlight_object(image, bbox, alpha=0.4):
    """
    Apply a semi-transparent highlight to a detected object
    """
    assert len(bbox) == 4, f"Expected bbox of length 4, got {len(bbox)}: {bbox}"
    x1, y1, x2, y2 = map(int, bbox)

    overlay = image.copy()
    color = get_color_for_category("highlight")
    assert len(color) == 3, f"Expected color of length 3, got {len(color)}: {color}"

    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
