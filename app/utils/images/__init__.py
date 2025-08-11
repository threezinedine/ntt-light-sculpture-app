from PIL import Image
import numpy as np
import cv2 as cv


def LoadImage(imagePath: str) -> cv.Mat | None:
    try:
        return cv.cvtColor(np.array(Image.open(imagePath)), cv.COLOR_RGB2BGR)  # type: ignore
    except:
        return None
