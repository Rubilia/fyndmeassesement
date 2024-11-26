import os
import cv2
import argparse

from rcnn import RCNNDetector
from utils import save_to_json, setup_logger
from visualize import draw_bounding_boxes


logger = setup_logger("part1")


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description="Part 1: object detection using R-CNN")
    parser.add_argument('-i', '--input', required=True, nargs='+', help="Input file(s) or folder(s) with images")
    parser.add_argument('-o', '--output', default="data/output", help="Output folder for images with bounding boxes")

    parser.add_argument('--conf-thresh', '-c', type=float, default=0.5, help="Confidence threshold for R-CNN")
    parser.add_argument('--batch-size', '-b', type=int, default=1, help="Batch size for processing images")
    parser.add_argument('--save-json', action='store_true', help="Save results to JSON")
    parser.add_argument('--device', '-d', choices=['cpu', 'cuda'], default='cpu', help="Device for PyTorch")
    args = parser.parse_args()

    # Get a list of files to be processed
    image_files = collect_image_files(args.input)
    if not image_files:
        logger.error("No valid image files found. Exiting.")
        exit(1)

    logger.info(f"Collected {len(image_files)} image file(s) for processing.")
    
    # Create output Dir if it doesn't exist
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize R-CNN detector
    detector = RCNNDetector(device=args.device, conf_thresh=args.conf_thresh)

    # Process images
    process_images(image_files, output_dir, detector, args.save_json, args.batch_size)


def process_images(image_files, output_dir, detector, save_json, batch_size):
    """
    Process a list of images using the R-CNN detector.
    Args:
        image_files (list[str]): List of image file paths.
        output_dir (str): Directory to save outputs.
        detector (RCNNDetector): Initialized R-CNN detector.
        save_json (bool): Whether to save results to JSON.
        batch_size (int): Batch size for processing images.
    """
    all_detections = []
    for i in range(0, len(image_files), batch_size):
        batch_files = image_files[i:i+batch_size]
        batch_images = [cv2.imread(file) for file in batch_files]
        predictions = detector.predict(batch_images)

        for image_path, image, prediction in zip(batch_files, batch_images, predictions):
            logger.info(f"Processing {image_path}...")
            # Save results
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            annotated_image = draw_bounding_boxes(image, prediction)
            cv2.imwrite(output_path, annotated_image)
            if save_json:
                all_detections.append({"image": image_path, "detections": prediction})
    if save_json:
        json_path = os.path.join(output_dir, "results.json")
        save_to_json(all_detections, json_path)
        logger.info(f"Results saved to {json_path}")


def collect_image_files(input_paths):
    """
    This function gets a list of all *.jpg and *.png images in provided folders
    """
    valid_extensions = ('.jpg', '.jpeg', '.png')
    image_files = []
    for path in input_paths:
        if os.path.isfile(path) and path.endswith(valid_extensions):
            image_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                image_files.extend([os.path.join(root, f) for f in files if f.endswith(valid_extensions)])
        else:
            logger.warning(f"Invalid path or unsupported file type: {path}")
    return image_files



if __name__ == "__main__":
    main()
