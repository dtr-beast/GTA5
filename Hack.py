from pydirectinput import press
from cv2 import imread, COLOR_BGR2GRAY, TM_CCOEFF_NORMED, INTER_CUBIC
from PIL import Image, ImageGrab
from copy import deepcopy
from time import sleep
from pathlib import Path
from os import chdir
from typing import List

import cv2
import numpy as np
import keyboard as kb

debug = False

# For conversion to 720p
new_width = 1280

# Load files for Fingerprint Hack
PHOTO_SOURCE = [
    [imread(f"Images/FP/F1{x}.jpg", 0) for x in range(5)],
    [imread(f"Images/FP/F2{x}.jpg", 0) for x in range(5)],
    [imread(f"Images/FP/F3{x}.jpg", 0) for x in range(5)],
    [imread(f"Images/FP/F4{x}.jpg", 0) for x in range(5)],
]
PHOTO_TEMP = deepcopy(PHOTO_SOURCE)

# Location of prints for 720p Screen
boxes = [
    (316, 179, 396, 261),
    (408, 176, 493, 262),
    (314, 270, 399, 357),
    (410, 272, 493, 354),
    (311, 366, 399, 452),
    (408, 368, 493, 453),
    (312, 462, 397, 549),
    (409, 464, 493, 548),
]


def finger_print():
    """
    Fingerprint Hack!
    Spoofs print to match the Finger impression
    """

    print("Starting Fingerprint Hack")
    match = None

    # Searches for Matches across the four Fingerprints
    while True:
        screen = get_image()
        screen = resize_image(screen)

        target_finger_print = screen[100:500, 600:900].copy()

        # Find main Fingerprint
        for (idx, image) in enumerate(PHOTO_TEMP):
            res = cv2.matchTemplate(target_finger_print, image[0], 5)
            loc = np.where(res >= 0.8)

            if len(loc[0]) != 0:
                if debug:
                    print(f'Fingerprint Match: F{idx + 1}0.jpg')
                match = idx  # Stores the index of the match fingerprint
                break

        if match is not None:
            break

    target_list = create_target_list(screen, PHOTO_TEMP[match])

    if debug:
        print(f"Target List: {target_list}")
    else:
        navigate(target_list)
    PHOTO_TEMP[match] = deepcopy(PHOTO_SOURCE[match])
    print("Done")


def resize_image(screen):
    (h, w) = screen.shape[:2]

    # Resize all images to 1280x720
    r = float(new_width) / float(w)

    if debug:
        print(f"Resizing Image: {h}x{w} -> {int(h * r)}x{new_width}")

    # Resize image to 720p
    return cv2.resize(screen, (new_width, int(h * r)), interpolation=INTER_CUBIC)


def navigate(positions):
    """Navigates and selects the matching prints"""
    print(f'Navigating Target List: {positions}')

    if debug:
        return

    x = y = 0  # Keeps track of current location
    for (index, pos) in enumerate(positions):
        if pos:
            moves = (index // 2) - x
            press("down", presses=moves)
            x += moves

            # For Right Sides (Odd Indexes)
            if (index & 1) and y == 0:
                press("right")
                y = 1

            # For Left Sides (Even Indexes)
            elif (index % 2 == 0) and y == 1:
                press("left")
                y = 0

            press("enter")

    press("tab")


def get_image():
    """
    Returns a screenshot of the given area,
    By default returns a screenshot of the fingerprint
    """
    # Starting Point (600, 100, 900, 500)
    img = Image.open("TestImage.png") if debug else ImageGrab.grab()
    return cv2.cvtColor(np.array(img), COLOR_BGR2GRAY)


def create_target_list(screen, matches) -> List[int]:
    """Creates a list for Navigation, processed by navigate()"""
    target_list = [0 for _ in range(8)]

    for (box_index, box) in enumerate(boxes):
        for (biometric_idx, biometric) in enumerate(matches):
            # Get all fingerprint components
            # components = component[0:550, 0:500].copy()

            print_component = screen[box[1]:box[3], box[0]:box[2]].copy()

            res = cv2.matchTemplate(print_component, biometric, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.8)

            if len(loc[0]) != 0:
                target_list[box_index] = 1
                matches.pop(biometric_idx)
                break

    return target_list


def idle():
    t = 3
    while t:
        press("w")
        sleep(300)
        press("s")
        sleep(300)
        t -= 1


if __name__ == "__main__":
    print("Started")
    # Change to Current Directory
    BASE_DIR = Path(__file__).resolve().parent
    chdir(BASE_DIR)
    kb.add_hotkey("ctrl+shift+h", finger_print)
    print('Activated Hotkeys: ctrl+shift+h => Fingerprint Hack ')
    if debug:
        print("Debug Mode Enabled")
        print("Initializing finger_print()")
        finger_print()

    kb.wait()
