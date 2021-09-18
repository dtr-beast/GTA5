from pydirectinput      import press
from cv2                import cvtColor, imread, COLOR_BGR2GRAY, matchTemplate, TM_CCOEFF_NORMED
from PIL.ImageGrab      import grab
from numpy              import array, where
from copy               import deepcopy
from keyboard           import add_hotkey, wait
from time               import sleep
from pathlib            import Path
from os                 import chdir

# Change to Home Directory
BASE_DIR = Path(__file__).resolve().parent
chdir(BASE_DIR)


def navigate(positions):
    """Navigates and selects the matching prints"""
    x = y = 0  # Keeps track of current location
    for (index, pos) in enumerate(positions):
        if pos:
            moves = (index // 2) - x
            press('down', presses=moves)
            x += moves

            # For Right Sides (Odd Indexes)
            if (index & 1) and y == 0:
                press('right')
                y = 1

            # For Left Sides (Even Indexes)
            elif (index % 2 == 0) and y == 1:
                press('left')
                y = 0

            press('enter')

    press('tab')


def get_image(bbox=(600, 100, 900, 500)):
    """
    Returns a screenshot of the given area,
    By default returns a screenshot of the fingerprint
    """
    # Starting Point (600, 100, 900, 500)
    img = array(grab(bbox=bbox))
    return cvtColor(img, COLOR_BGR2GRAY)


# Load files for Fingerprint Hack
PHOTO_SOURCE = [[imread(f'Images/FP/F1{x}.jpg', 0) for x in range(5)],
                [imread(f'Images/FP/F2{x}.jpg', 0) for x in range(5)],
                [imread(f'Images/FP/F3{x}.jpg', 0) for x in range(5)],
                [imread(f'Images/FP/F4{x}.jpg', 0) for x in range(5)]]
PHOTO_TEMP = deepcopy(PHOTO_SOURCE)

# Location of prints for 720p Screen
boxes = [(316, 179, 396, 261), (408, 176, 493, 262),
         (314, 270, 399, 357), (410, 272, 493, 354),
         (311, 366, 399, 452), (408, 368, 493, 453),
         (312, 462, 397, 549), (409, 464, 493, 548)]


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
        for (index, image) in enumerate(PHOTO_TEMP):
            res = matchTemplate(screen, image[0], TM_CCOEFF_NORMED)
            loc = where(res >= 0.8)

            if len(loc[0]) != 0:
                match = index  # Stores the index of the match fingerprint
                break

        if match is not None:
            break

    target_list = [0 for _ in range(8)]
    # Creates a list for Navigation
    for (box_index, box) in enumerate(boxes):
        for (biometric_idx, biometric) in enumerate(PHOTO_TEMP[match]):
            screen = get_image(bbox=box)
            res = matchTemplate(screen, biometric, TM_CCOEFF_NORMED)
            loc = where(res >= 0.8)

            if len(loc[0]) != 0:
                target_list[box_index] = 1
                PHOTO_TEMP[match].pop(biometric_idx)
                break

    navigate(target_list)
    PHOTO_TEMP[match] = deepcopy(PHOTO_SOURCE[match])
    print("Done")


def idle():
    t = 3
    while t:
        press('w')
        sleep(300)
        press('s')
        sleep(300)
        t -= 1


if __name__ == '__main__':
    add_hotkey('ctrl+shift+i', finger_print)
    # add_hotkey('ctrl+shift+i', idle)
    print("Started")
    print("Make sure to start the program in 1280x720 resolution")
    wait()
