from PIL import Image

AREAS = {

    # ジャケット
    "jacket": (65, 305, 145, 410),

    # Challenge Rate
    "challenge_rate": (270, 485, 620, 545),

    # 判定数値
    "amazing": (331, 600, 432, 650),
    "perfect": (331, 665, 432, 696),
    "great": (331, 710, 432, 741),
    "good": (331, 755, 432, 786),
    "bad": (331, 800, 432, 831),
    "miss": (331, 845, 432, 876),

    # 棒グラフ
    "graph": (465, 625, 780, 885),

    # 新UI判定用
    "new_ui": (40, 210, 600, 360),
}


def crop_all(image):

    result = {}

    for key, area in AREAS.items():
        result[key] = image.crop(area)

    return result