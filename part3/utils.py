import cv2
import random
import numpy as np
import matplotlib.pyplot as plt


# Category color mapping
CATEGORY_COLORS = {}


def generate_unique_colors(labels):
    """
    Generate unique colors for each label using interpolation
    """
    num_labels = len(labels)
    cmap = plt.get_cmap("rainbow")  # Use a colormap for better color distribution
    for i, label in enumerate(labels):
        # Interpolate colors across the colormap
        color = cmap(i / num_labels)  # Normalized position in the colormap
        CATEGORY_COLORS[label] = tuple(int(c * 255) for c in color[:3])  # Convert to RGB


def get_color_for_category(category):
    """
    Assign or retrieve a unique color for a category
    """
    if category not in CATEGORY_COLORS:
        CATEGORY_COLORS[category] = tuple(random.randint(0, 255) for _ in range(3))
    return CATEGORY_COLORS[category]


def scale_font_size(bbox, min_size=0.5, max_size=2.0):
    """
    Scale font size based on object size with min and max limits
    """
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    scale = max(min_size, min(max_size, width * 0.002))
    return scale



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

generate_unique_colors(category_names.values())
