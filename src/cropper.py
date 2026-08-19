"""
cropper.py
Version : 1.0 Final Edition

ROI Crop Module

Author : OpenAI + Hapylon
"""

from typing import Tuple

import numpy as np

from config import get_region


# ==========================================================
# Utility
# ==========================================================

def region_to_pixel(
    image: np.ndarray,
    name: str
) -> Tuple[int, int, int, int]:
    """
    正規化座標をピクセル座標へ変換

    Parameters
    ----------
    image : np.ndarray
        入力画像

    name : str
        Region名

    Returns
    -------
    (x1, y1, x2, y2)
    """

    region = get_region(name)

    h, w = image.shape[:2]

    x1 = int(region.left * w)
    y1 = int(region.top * h)

    x2 = int(region.right * w)
    y2 = int(region.bottom * h)

    return (
        x1,
        y1,
        x2,
        y2
    )


# ==========================================================
# Generic Crop
# ==========================================================

def crop(
    image: np.ndarray,
    name: str
) -> np.ndarray:
    """
    Region名から画像を切り抜く
    """

    x1, y1, x2, y2 = region_to_pixel(
        image,
        name
    )

    return image[
        y1:y2,
        x1:x2
    ]


# ==========================================================
# Individual Crop Functions
# ==========================================================

def crop_title(image):

    return crop(image, "title")


def crop_jacket(image):

    return crop(image, "jacket")


def crop_difficulty(image):

    return crop(image, "difficulty")


def crop_level(image):

    return crop(image, "level")


def crop_rank(image):

    return crop(image, "rank")


def crop_challenge_rate(image):

    return crop(image, "challenge_rate")


def crop_judge(image):

    return crop(image, "judge")


def crop_notes(image):

    return crop(image, "notes")


def crop_graph(image):

    return crop(image, "graph")