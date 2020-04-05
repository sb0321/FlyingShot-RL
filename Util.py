import numpy as np
import cv2
from PIL import Image

def img_resize(state):

    state_out = cv2.resize(state, (80, 80))
    state_out = cv2.cvtColor(state_out, cv2.COLOR_BGR2GRAY)
    state_out = np.reshape(state_out, (80, 80))
    return state_out

