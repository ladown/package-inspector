import numpy as np
import pytest
from app.comparator import ImageComparator
from app.config import Config


@pytest.fixture
def comparator():
    return ImageComparator()


def test_compare_identical_images(comparator, sample_image):
    result = comparator.compare(sample_image, sample_image)
    assert result["similarity_score"] > 0.99
    assert len(result["defects"]) == 0


def test_compare_different_images(comparator, sample_image, sample_image_with_defect):
    result = comparator.compare(sample_image, sample_image_with_defect)
    assert result["similarity_score"] < 1.0
    assert len(result["defects"]) > 0


def test_compare_with_defects(comparator, sample_image, sample_image_with_defect):
    result = comparator.compare(sample_image, sample_image_with_defect)
    assert "defects" in result
    assert isinstance(result["defects"], list)
    for defect in result["defects"]:
        assert "type" in defect
        assert "bbox" in defect
        assert "area" in defect


def test_similarity_threshold(comparator, sample_image):
    different_image = np.zeros_like(sample_image)
    result = comparator.compare(sample_image, different_image)
    assert result["similarity_score"] < comparator.similarity_threshold
