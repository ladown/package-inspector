import cv2
import numpy as np

from app.config import Config
from app.image_utils import resize_to_match, to_grayscale


class ImageComparator:
    def __init__(self):
        self.similarity_threshold = Config.SIMILARITY_THRESHOLD
        self.min_defect_area = Config.MIN_DEFECT_AREA
        self.diff_threshold = Config.DIFF_THRESHOLD
        self.kernel_size = Config.MORPHOLOGY_KERNEL_SIZE

    def compare(self, reference, test):
        test_resized = resize_to_match(reference, test)
        ref_gray = to_grayscale(reference)
        test_gray = to_grayscale(test_resized)
        similarity_score = self._calculate_similarity(ref_gray, test_gray)
        defects = self._find_defects(ref_gray, test_gray)
        status = self._determine_status(similarity_score, defects)

        return {
            "status": status,
            "similarity_score": similarity_score,
            "defects": defects,
            "test_resized": test_resized,
        }

    def _calculate_similarity(self, ref_gray, test_gray):
        result = cv2.matchTemplate(test_gray, ref_gray, cv2.TM_CCOEFF_NORMED)
        similarity_score = float(np.max(result))
        similarity_score = max(0.0, min(1.0, similarity_score))
        return similarity_score

    def _find_defects(self, ref_gray, test_gray):
        diff = cv2.absdiff(ref_gray, test_gray)
        _, thresh = cv2.threshold(diff, self.diff_threshold, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (self.kernel_size, self.kernel_size)
        )
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(
            cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        defects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_defect_area:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            defect_type = self._classify_defect(ref_gray, test_gray, x, y, w, h)

            defects.append(
                {
                    "bbox": [int(x), int(y), int(w), int(h)],
                    "area": int(area),
                    "type": defect_type,
                }
            )

        return defects

    def _classify_defect(self, ref_gray, test_gray, x, y, w, h):
        ref_roi = ref_gray[y : y + h, x : x + w]
        test_roi = test_gray[y : y + h, x : x + w]
        ref_mean = np.mean(ref_roi)
        test_mean = np.mean(test_roi)

        if abs(ref_mean - test_mean) > 50:
            if test_mean < ref_mean:
                return "missing_element"
            else:
                return "extra_element"

        return "difference"

    def _determine_status(self, similarity_score, defects):
        if similarity_score >= self.similarity_threshold and len(defects) == 0:
            return "OK"
        else:
            return "FAIL"
