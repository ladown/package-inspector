import traceback

import cv2
from flask import Blueprint, jsonify, render_template, request

from app.annotator import ImageAnnotator
from app.comparator import ImageComparator
from app.config import Config
from app.image_utils import encode_to_base64, load_image, validate_image

bp = Blueprint("main", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "opencv_version": cv2.__version__})


@bp.route("/api/compare", methods=["POST"])
def compare():
    try:
        if "reference" not in request.files or "test" not in request.files:
            return jsonify({"error": "Отсутствуют файлы изображений"}), 400

        reference_file = request.files["reference"]
        test_file = request.files["test"]

        if reference_file.filename == "" or test_file.filename == "":
            return jsonify({"error": "Файлы не выбраны"}), 400

        if not allowed_file(reference_file.filename) or not allowed_file(
            test_file.filename
        ):
            return jsonify(
                {
                    "error": "Неподдерживаемый формат файла. Используйте JPG, JPEG или PNG"
                }
            ), 400

        reference_img = load_image(reference_file)
        test_img = load_image(test_file)

        if not validate_image(reference_img) or not validate_image(test_img):
            return jsonify({"error": "Ошибка валидации изображений"}), 400

        comparator = ImageComparator()
        result = comparator.compare(reference_img, test_img)

        annotated_image_base64 = None
        if result["status"] == "FAIL" and len(result["defects"]) > 0:
            annotator = ImageAnnotator()
            annotated_img = annotator.annotate_image(
                result["test_resized"], result["defects"]
            )
            annotated_image_base64 = encode_to_base64(annotated_img)

        return jsonify(
            {
                "status": result["status"],
                "similarity_score": result["similarity_score"],
                "defects_count": len(result["defects"]),
                "defects": result["defects"],
                "annotated_image": annotated_image_base64,
            }
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error in /api/compare: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500
