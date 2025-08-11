from PIL import Image
import numpy as np
import cv2 as cv


def LoadImage(imagePath: str) -> cv.Mat | None:
    try:
        return cv.cvtColor(np.array(Image.open(imagePath)), cv.COLOR_RGB2BGR)  # type: ignore
    except:
        return None


def ConvertToBinary(image: cv.Mat | None) -> cv.Mat | None:
    if image is None:
        return None

    return cv.threshold(image, 127, 255, cv.THRESH_BINARY)[1]  # type: ignore
