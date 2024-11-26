from flask import jsonify, request
from models import products
from utils import validate_product_data
from threading import Lock

product_lock = Lock()

def register_routes(app):
    @app.route("/products", methods=["POST"])
    def create_product():
        """Create a new product."""
        data = request.json
        validation_result = validate_product_data(data)
        if isinstance(validation_result, str):
            return jsonify({"error": "Validation failed", "details": validation_result}), 400

        product = validation_result.dict()
        with product_lock:
            if product["id"] in products:
                return jsonify({"error": "Product ID already exists"}), 409
            products[str(product["id"])] = product
        return jsonify({"message": "Product created", "product": product}), 201

    @app.route("/products", methods=["GET"])
    def get_all_products():
        """Retrieve all products."""
        with product_lock:
            all_products = list(products.values())
        return jsonify({"products": all_products}), 200

    @app.route("/products/<product_id>", methods=["GET"])
    def get_product(product_id):
        """Retrieve a specific product by ID."""
        with product_lock:
            product = products.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"product": product}), 200

    @app.route("/products/<product_id>", methods=["PUT"])
    def update_product(product_id):
        """Update a specific product."""
        data = request.json
        validation_result = validate_product_data(data)
        if isinstance(validation_result, str):
            return jsonify({"error": "Validation failed", "details": validation_result}), 400

        product = validation_result.dict()
        with product_lock:
            if product_id not in products:
                return jsonify({"error": "Product not found"}), 404
            products[product_id].update(product)
        return jsonify({"message": "Product updated", "product": products[product_id]}), 200

    @app.route("/products/<product_id>", methods=["DELETE"])
    def delete_product(product_id):
        """Delete a specific product."""
        with product_lock:
            if product_id not in products:
                return jsonify({"error": "Product not found"}), 404
            del products[product_id]
        return jsonify({"message": "Product deleted"}), 200
