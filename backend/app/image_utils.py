import base64
import io

import cv2
import numpy as np
from PIL import Image


def load_image(file_storage):
    img_bytes = file_storage.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Не удалось загрузить изображение. Проверьте формат файла.")

    return img


def validate_image(image):
    if image is None:
        return False
    if not isinstance(image, np.ndarray):
        return False
    if len(image.shape) < 2:
        return False
    return True


def resize_to_match(reference, test):
    target_height, target_width = reference.shape[:2]
    test_resized = cv2.resize(
        test, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4
    )
    return test_resized


def to_grayscale(image):
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def encode_to_base64(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_base64}"
