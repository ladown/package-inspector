import io

import cv2
import numpy as np
import pytest
from PIL import Image

from app.image_utils import (
    encode_to_base64,
    load_image,
    resize_to_match,
    to_grayscale,
    validate_image,
)


def test_load_image(temp_image_file):
    with open(temp_image_file, 'rb') as f:
        image = load_image(f)
    assert image is not None
    assert isinstance(image, np.ndarray)
    assert len(image.shape) == 3


def test_load_image_invalid():
    invalid_file = io.BytesIO(b'invalid image data')
    with pytest.raises(ValueError):
        load_image(invalid_file)


def test_validate_image_valid(sample_image):
    assert validate_image(sample_image) is True


def test_validate_image_none():
    assert validate_image(None) is False


def test_validate_image_empty():
    empty_image = np.array([])
    assert validate_image(empty_image) is False


def test_validate_image_wrong_shape():
    wrong_shape = np.zeros((100,))
    assert validate_image(wrong_shape) is False


def test_resize_to_match(sample_image):
    reference = np.zeros((200, 200, 3), dtype=np.uint8)
    resized = resize_to_match(reference, sample_image)
    assert resized.shape[:2] == reference.shape[:2]


def test_to_grayscale(sample_image):
    gray = to_grayscale(sample_image)
    assert len(gray.shape) == 2
    assert gray.dtype == np.uint8


def test_encode_to_base64(sample_image):
    encoded = encode_to_base64(sample_image)
    assert encoded.startswith("data:image/jpeg;base64,")
    assert len(encoded) > 50
