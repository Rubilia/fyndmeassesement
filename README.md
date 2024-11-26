# Part 1: Object Detection CLI Tool using Faster R-CNN

This tool is a CLI application that performs object detection on images using a pre-trained Faster R-CNN model. It supports GPU/CPU execution, batch processing, confidence-based filtering, and JSON output.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-repository/part1.git
cd part1
```

2. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

### Command-Line Arguments

| Option              | Description                                       | Example          |
| ------------------- | ------------------------------------------------- | ---------------- |
| `-i, --input`       | Input file(s) or folder(s) with images (required) | `-i data/images` |
| `-o, --output`      | Output folder for results                         | `-o data/output` |
| `-c, --conf-thresh` | Confidence threshold for filtering predictions    | `-c 0.6`         |
| `-b, --batch-size`  | Batch size for processing images                  | `-b 4`           |
| `--save-json`       | Save detection results to a JSON file             | `--save-json`    |
| `-d, --device`      | Device to run the model (`cpu` or `cuda`)         | `-d cuda`        |

### Example Usage

Detect objects in a folder of images and save results:

```
python cli.py -i data/images -o data/output --conf-thresh 0.7 --save-json -d cuda
```

## How It Works

1. **Input Handling**:

   - The tool accepts multiple files or directories as input.
   - Recursively searches directories for `.jpg`, `.jpeg`, and `.png` images.

2. **Model**:

   - The Faster R-CNN model is pre-trained on the COCO dataset.

3. **Processing**:

   - Images are processed in batches.
   - Bounding boxes, confidence scores, and class labels are generated.

4. **Output**:
   - Annotated images are saved in the output directory.
   - JSON results (if enabled) are saved to `results.json` in the output directory.

## File Structure

```
part1/
├── cli.py # Main CLI script
├── rcnn.py # Faster R-CNN model integration
├── utils.py # Utilities for logging, JSON, and label handling
├── visualize.py # Visualization utilities for bounding boxes
├── data/
│ ├── input/ # Sample input images
│ └── output/ # Output directory for results
├── requirements.txt # Python dependencies
└── README.md # Documentation
```
