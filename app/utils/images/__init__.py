from PIL import Image
import numpy as np
import cv2 as cv
from utils.logger import logger


def LoadImage(imagePath: str) -> cv.Mat | None:
    try:
        return cv.cvtColor(np.array(Image.open(imagePath)), cv.COLOR_RGB2BGR)  # type: ignore
    except:
        return None


def ConvertToBinary(image: cv.Mat | None, threshold: int = 128) -> cv.Mat | None:
    if image is None:
        return None

    grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    try:
        _, binaryImage = cv.threshold(grayImage, threshold, 255, cv.THRESH_BINARY)
        return binaryImage  # type: ignore
    except:
        return grayImage  # type: ignore
