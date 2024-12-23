import json
import logging

def setup_logger(name, level=logging.INFO):
    """Set up a logger with a given name and level."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def save_to_json(data, filepath):
    """Save data to a JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def get_label_from_id(category_id):
    """
    Convert a category number to its corresponding label.
    """
    category_names = {
        0: "bicycle", 1: "person", 2: "car", 3: "motorcycle", 4: "airplane", 5: "bus",
        6: "truck", 7: "train", 8: "boat", 9: "traffic light", 10: "fire hydrant",
        11: "stop sign", 12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
        16: "dog", 17: "horse", 18: "sheep", 19: "cow", 20: "elephant", 21: "bear",
        22: "zebra", 23: "giraffe", 24: "backpack", 25: "umbrella", 26: "handbag",
        27: "tie", 28: "suitcase", 29: "frisbee", 30: "skis", 31: "snowboard",
        32: "sports ball", 33: "kite", 34: "baseball bat", 35: "baseball glove",
        36: "skateboard", 37: "surfboard", 38: "tennis racket", 39: "bottle",
        40: "wine glass", 41: "cup", 42: "sandwich", 43: "knife", 44: "spoon", 45: "bowl",
        46: "banana", 47: "apple", 48: "fork", 49: "orange", 50: "broccoli",
        51: "carrot", 52: "hot dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair",
        57: "couch", 58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet",
        62: "tv", 63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard",
        67: "cell phone", 68: "microwave", 69: "oven", 70: "toaster", 71: "sink",
        72: "refrigerator", 73: "book", 74: "clock", 75: "vase", 76: "scissors",
        77: "teddy bear", 78: "hair drier", 79: "toothbrush"
    }
    return category_names.get(category_id, "unknown")