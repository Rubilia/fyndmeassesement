from flask import Blueprint, jsonify, request
from models import products, product_lock, validate_product_update
from utils import validate_product_data
from pydantic import ValidationError
from uuid import UUID
import logging

# Initialize Blueprint
products_bp = Blueprint("products", __name__)
logger = logging.getLogger("part2_api")


def format_response(message=None, data=None, error=None):
    """
    Format API response with consistent structure.
    """
    return {
        "message": message,
        "data": data,
        "error": error
    }


@products_bp.route("/", methods=["POST"])
def create_product():
    """
    Create a new product
    """
    data = request.json
    validation_result = validate_product_data(data)
    if isinstance(validation_result, str):
        return jsonify(format_response(
            message="Validation failed",
            error=validation_result
        )), 400

    product = validation_result.model_dump()
    with product_lock:
        if str(product["id"]) in products:
            return jsonify(format_response(
                message="Conflict",
                error=f"Product with ID {product['id']} already exists"
            )), 409
        products[str(product["id"])] = product
    logger.info(f"Product {product['id']} created successfully.")
    return jsonify(format_response(
        message="Product created successfully",
        data=product,
        error=None
    )), 201


@products_bp.route("/", methods=["GET"])
def get_all_products():
    """
    Retrieve all products
    """
    with product_lock:
        all_products = list(products.values())
    return jsonify(format_response(
        message="Retrieved all products successfully",
        data={"products": all_products},
        error=None
    )), 200


@products_bp.route("/<product_id>", methods=["GET"])
@products_bp.route("/<product_id>/", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a specific product by ID
    """
    with product_lock:
        product = products.get(product_id)
    if not product:
        logger.warning(f"Product ID {product_id} not found.")
        return jsonify(format_response(
            message="Product not found",
            error=f"No product found with ID {product_id}"
        )), 404
    return jsonify(format_response(
        message="Product retrieved successfully",
        data=product,
        error=None
    )), 200


@products_bp.route("/<product_id>", methods=["PUT"])
@products_bp.route("/<product_id>/", methods=["PUT"])
def update_product(product_id):
    """
    Update a specific product
    """
    # Validate if the product_id is a valid UUID
    try:
        UUID(product_id)
    except ValueError:
        logger.warning(f"Invalid product ID format: {product_id}")
        return jsonify(format_response(
            message="Validation failed",
            error="Invalid product ID format"
        )), 400

    # Parse and validate the JSON payload
    data = request.json
    try:
        validation_result = validate_product_update(data)  # Use partial update schema
    except ValidationError as e:
        logger.warning(f"Validation error for product update: {str(e)}")
        return jsonify(format_response(
            message="Validation failed",
            error=str(e)
        )), 400

    product_updates = validation_result.dict(exclude_unset=True)  # Allow partial updates

    # Lock and update the product
    with product_lock:
        if product_id not in products:
            logger.warning(f"Product ID {product_id} not found.")
            return jsonify(format_response(
                message="Product not found",
                error=f"No product found with ID {product_id}"
            )), 404

        # Update only the provided fields
        products[product_id].update(product_updates)

    logger.info(f"Product {product_id} updated successfully.")
    return jsonify(format_response(
        message="Product updated successfully",
        data=products[product_id],
        error=None
    )), 200


@products_bp.route("/<product_id>", methods=["DELETE"])
@products_bp.route("/<product_id>/", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a specific product
    """
    with product_lock:
        if product_id not in products:
            logger.warning(f"Product ID {product_id} not found.")
            return jsonify(format_response(
                message="Product not found",
                error=f"No product found with ID {product_id}"
            )), 404
        del products[product_id]
    logger.info(f"Product {product_id} deleted successfully.")
    return jsonify(format_response(
        message="Product deleted successfully",
        error=None
    )), 200


@products_bp.errorhandler(Exception)
def handle_exception(e):
    """
    Handle exceptions and log them.
    """
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify(format_response(
        message="An internal server error occurred",
        error="Unknown server error"
    )), 500
