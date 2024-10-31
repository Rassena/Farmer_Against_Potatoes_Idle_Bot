import ctypes
import win32gui
import win32ui
from PIL import Image, ImageOps, ImageChops
import numpy as np
import pyautogui

WINDOW_NAME = "Farmer Against Potatoes Idle"

POTATO_POSITIONS = []
CLOSET_INDEX = []
POTATO_CROP_BOX_POSITIONS = []

NORMAL_POTATO_COLORS = list(range(180, 195))
GREAT_POTATO_COLORS = list(range(152, 160))
ALLOWED_COLORS = NORMAL_POTATO_COLORS + GREAT_POTATO_COLORS

FIRST_CLOSET_CENTER = (65, 139)
CLOSET_COL_OFFSET = 131
CLOSET_ROW_OFFSET = 215

CROP_BOX_RAD = 2

WHACK_OFFSET_0 = 353
WHACK_OFFSET_1 = 215

WHACK_WIDTH = 663
WHACK_HEIGHT = 634

img_base = Image.open("grayscale.png")
hwnd = 0x23108A


def fill_lists():
    for col in range(0, 5):
        for row in range(3):
            CLOSET_INDEX.append((col, row))

            closet_center = (
                FIRST_CLOSET_CENTER[0] + CLOSET_COL_OFFSET * col,
                FIRST_CLOSET_CENTER[1] + CLOSET_ROW_OFFSET * row,
            )
            POTATO_POSITIONS.append(closet_center)

            POTATO_CROP_BOX_POSITIONS.append(
                (
                    closet_center[0] - CROP_BOX_RAD,
                    closet_center[1] - CROP_BOX_RAD,
                    closet_center[0] + CROP_BOX_RAD,
                    closet_center[1] + CROP_BOX_RAD,
                )
            )


def get_img(bitmap):
    """Retrieve the bitmap data"""
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        "RGB",
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
        bmpstr,
        "raw",
        "BGRX",
        0,
        1,
    )
    return img


fill_lists()

if win32gui.IsWindow(hwnd):
    # Get the window's dimensions
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # Set up device context for the window
    hdc = win32gui.GetWindowDC(hwnd)
    dc = win32ui.CreateDCFromHandle(hdc)
    memdc = dc.CreateCompatibleDC()

    # Create a bitmap to hold the screenshot
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(dc, width, height)
    memdc.SelectObject(bitmap)

    for i in range(40000):
        # Capture the window
        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)

        if result == 1:
            img = get_img(bitmap)
            img_gray = ImageOps.grayscale(img)
            img_difference = ImageChops.difference(
                img_base,
                img_gray.crop(
                    (
                        WHACK_OFFSET_0,
                        WHACK_OFFSET_1,
                        WHACK_OFFSET_0 + WHACK_WIDTH,
                        WHACK_OFFSET_1 + WHACK_HEIGHT,
                    )
                ),
            )

            for index, potato_position in enumerate(POTATO_POSITIONS):
                average_box = img_difference.crop(POTATO_CROP_BOX_POSITIONS[index])
                if int(np.average(np.array(average_box))) in ALLOWED_COLORS:
                    # print(CLOSET_INDEX[i], value, image_array_average)
                    pyautogui.click(
                        potato_position[0] + WHACK_OFFSET_0,
                        potato_position[1] + WHACK_OFFSET_1,
                    )
                    break

            # elif value == 0:
            #     pass
            # else:
            # print("Didn't hit the forbidden color at ", CLOSET_INDEX[i], value, image_array_average)
            # last_closet = CLOSET_INDEX[i]
            # last_value = value


# window = 0
# def windows(hwnd, ctx):
#     global window
#     if win32gui.IsWindowVisible(hwnd):
#         if win32gui.GetWindowText(hwnd) == "Farmer Against Potatoes Idle":
#             window = hwnd

# win32gui.EnumWindows(windows, None)
