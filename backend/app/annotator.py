import cv2
import numpy as np


class ImageAnnotator:
    def annotate_image(self, image, defects):
        annotated = image.copy()

        for defect in defects:
            x, y, w, h = defect["bbox"]
            area = defect["area"]

            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 0, 255), 3)

            label = f"Area: {area} px"
            text_y = y - 10 if y > 30 else y + h + 25

            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                annotated,
                (x, text_y - text_height - 5),
                (x + text_width + 5, text_y + 5),
                (0, 0, 255),
                -1,
            )

            cv2.putText(
                annotated,
                label,
                (x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

        return annotated
