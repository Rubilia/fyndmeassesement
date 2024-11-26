import cv2
from rcnn import RCNNDetector
from ar import process_frame


def main():
    # Initialize R-CNN
    detector = RCNNDetector(device='cuda', conf_thresh=0.5)

    # Open the camera
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Do object detection
        detections = detector.predict([frame])[0]

        # Process the frame with detections
        processed_frame = process_frame(frame, detections)

        # Display the frame
        cv2.imshow("AR Object Detection", processed_frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
