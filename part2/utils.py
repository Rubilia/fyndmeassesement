import logging

from models import Product
from pydantic import ValidationError


def setup_logger(name, level=logging.INFO):
    """Set up a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def validate_product_data(data):
    """
    Validate product data using Pydantic.
    Args:
        data (dict): Product data.
    Returns:
        Product: Validated Product instance.
    Raises:
        ValidationError: If validation fails.
    """
    try:
        return Product(**data)
    except ValidationError as e:
        return str(e)
