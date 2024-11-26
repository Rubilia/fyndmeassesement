import argparse
import os
from utils import setup_logger


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
