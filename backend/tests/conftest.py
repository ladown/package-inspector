import os
import sys

import cv2
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_image():
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    image[50:150, 50:150] = [255, 255, 255]
    return image


@pytest.fixture
def sample_image_with_defect():
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    image[50:150, 50:150] = [255, 255, 255]
    image[10:30, 10:30] = [255, 255, 255]
    return image


@pytest.fixture
def temp_image_file(tmp_path, sample_image):
    file_path = tmp_path / "test_image.jpg"
    cv2.imwrite(str(file_path), sample_image)
    return file_path
