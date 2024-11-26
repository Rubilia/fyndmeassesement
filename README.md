# Part 1: Object Detection CLI Tool using Faster R-CNN

This tool is a CLI application that performs object detection on images using a pre-trained Faster R-CNN model. It supports GPU/CPU execution, batch processing, confidence-based filtering, and JSON output.

## Installation

1. Clone the repository:

```
git clone https://github.com/Rubilia/fyndmeassesement.git
cd fyndmeassesement/
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
cd part1/
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
├── cli.py                   # Main CLI script
├── rcnn.py                  # Faster R-CNN model integration
├── utils.py                 # Utilities for logging, JSON, and label handling
└── visualize.py             # Visualization utilities for bounding boxes
```

# Part 2: RESTful API for Product Management

This project implements a RESTful API using Flask to manage a collection of product information. The API supports CRUD operations and utilizes a shared in-memory dictionary to store product data. The application is thread-safe when run with Gunicorn in threaded mode.

---

## Features

- Modular design for easy maintenance and scalability.

- Thread-safe in-memory storage using `threading.Lock`.

- CRUD operations (Create, Read, Update, Delete) for product management.

- JSON-based request and response formats.

- Centralized logging and error handling for better debugging.

---

## How Storage Works

### **Storage in a Shared Dictionary**

The product data is stored in a Python dictionary (`products`), with the product ID (UUID) as the key and the product details as the value. Example:

```
products = {
	"123e4567-e89b-12d3-a456-426614174000": {
		"id": "123e4567-e89b-12d3-a456-426614174000",
		"name": "Gaming Laptop",
		"description": "A laptop for gaming and work.",
		"price": 1500.99,
		"quantity": 5,
		"category": "Electronics"
	}
}
```

### **Concurrency Handling with Gunicorn**

To handle concurrency properly something more than just a Flask developement server is required. Gunicorn provides such functionality. When running Flask with Gunicorn in **threaded mode**, a single process handles multiple threads. Threads share the same memory space, which allows all threads to access the same `products` dictionary. To ensure thread safety, a `threading.Lock` is used to serialize access to the shared dictionary during write operations (`POST`, `PUT`, and `DELETE`). It would not work in non-threaded mode as gunicorn will create separate processes for each worker and they will not share any data.

### **Gunicorn Configuration**

Gunicorn is configured to use a single process with multiple threads:

```
cd part2/
gunicorn -w 1 --threads 4 -b 0.0.0.0:8000 app:create_app
```

- `-w 1`: Specifies one worker process, ensuring a single memory space for the shared dictionary.
- `--threads 4`: Enables four threads for handling concurrent requests.

---

## API Endpoints

### Create Product

- **Endpoint**: `/products`

- **Method**: `POST`

- **Description**: Adds a new product to the collection.

- **Request Body**:

```
{
	"id": "123e4567-e89b-12d3-a456-426614174000",
	"name": "Gaming Laptop",
	"description": "A high-end gaming laptop",
	"price": 1500.99,
	"quantity": 5,
	"category": "Electronics"
}
```

- **Response**:

- **201 Created**: Product successfully created.

- **409 Conflict**: Product with the given ID already exists.

- **400 Bad Request**: Invalid input data.

### Retrieve All Products

- **Endpoint**: `/products`

- **Method**: `GET`

- **Description**: Retrieves a list of all products.

- **Response**:

- **200 OK**: List of products.

### Retrieve a Product

- **Endpoint**: `/products/<product_id>`

- **Method**: `GET`

- **Description**: Retrieves details of a specific product by its ID.

- **Response**:

- **200 OK**: Product details.

- **404 Not Found**: Product with the given ID does not exist.

### Update a Product

- **Endpoint**: `/products/<product_id>`

- **Method**: `PUT`

- **Description**: Updates information for a specific product.

- **Request Body**:

```
{
	"name": "Updated Laptop",
	"price": 1600.00,
	"quantity": 3
}
```

- **Response**:

- **200 OK**: Product updated successfully.

- **404 Not Found**: Product with the given ID does not exist.

- **400 Bad Request**: Invalid input data.

### Delete a Product

- **Endpoint**: `/products/<product_id>`

- **Method**: `DELETE`

- **Description**: Deletes a product from the collection by its UUID.

- **Response**:

- **200 OK**: Product deleted successfully.

- **404 Not Found**: Product with the given ID does not exist.

---

## Limitations

1. **Product ID**:

   - Must be a valid UUID (e.g., `"123e4567-e89b-12d3-a456-426614174000"`).
   - Invalid UUIDs will result in a `400 Bad Request` error.

2. **Product Name**:

   - Must be at least 6 characters long.
   - Shorter names will result in a `400 Bad Request` error.

3. **Price**:

   - Must be a positive number greater than 0.
   - Negative or zero prices will result in a `400 Bad Request` error.

4. **Quantity**:

   - Must be an integer between 1 and 10 (inclusive).
   - Quantities outside this range will result in a `400 Bad Request` error.

5. **Category**:
   - Must be one of the following predefined categories:
     - `Electronics`
     - `Home Appliances`
     - `Books`
     - `Fashion`
     - `Toys`
     - `Furniture`
     - `Groceries`
     - `Fitness`
     - `Beauty`
     - `Automotive`
   - Invalid categories will result in a `400 Bad Request` error.

---

## Logging

- Logs all actions and errors.
- Unhandled exceptions are logged with a traceback for debugging.

# Part 3: Real time object deterction in AR

This project demonstrates AR integration with object detection using the Faster R-CNN. The application uses OpenCV to process real-time video from the camera, detect objects, and overlay visual effects such as bounding boxes, labels, and highlights on detected objects.

---

## Features

### **1. Real-Time Object Detection**

- Utilizes the Faster R-CNN model pre-trained on the COCO dataset to detect objects in real-time.
- Objects are classified into one of 80 predefined categories

### **2. Augmented Reality Effects**

- Draws **bounding boxes** around detected objects with a unique color for each category.
- Adds **labels** and confidence scores to detected objects, with font sizes dynamically scaled based on the object size.
- Highlights detected objects with a semi-transparent overlay for better visualization.

### **3. Category Color Mapping**

- Each object category is assigned a **unique color** using interpolation from a colormap.
- Ensures consistent and visually distinct colors for each category.

### **4. Modular Codebase**

- The project is structured into modular components:
  - **`rcnn.py`**: Handles object detection using Faster R-CNN.
  - **`ar.py`**: Processes frames to overlay AR effects.
  - **`drawing.py`**: Manages drawing of bounding boxes, labels, and highlights.
  - **`utils.py`**: Provides utility functions for color generation, font scaling, and category mapping.

### **5. GPU Support**

- Supports GPU acceleration via PyTorch for faster object detection.

### **6. Highly Configurable**

- Detection confidence threshold and device (`cpu` or `cuda`) can be configured when initializing the detector.
- AR effects (e.g., highlight transparency, font size scaling) are adjustable through utility functions.

---

## Usage

### Running the Application

1. Start the application:

```
cd part3/
python main.py
```

2. The camera feed will open in a new window, showing detected objects with bounding boxes, labels, and highlights.

3. Press `q` to exit the application.

---

## Project Structure

```
part3/
├── main.py         # Entry point for running the application
├── ar.py           # Processes frames and applies AR effects
├── drawing.py      # Handles bounding box and label rendering
├── rcnn.py         # Object detection using Faster R-CNN
└── utils.py        # Utility functions for scaling and color mapping
```
