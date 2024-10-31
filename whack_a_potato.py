import ctypes
import win32gui
import win32ui
from PIL import Image, ImageOps, ImageChops, ImageDraw
import numpy as np
import pyautogui
from pathlib import Path

DEBUG = True
DEBUG_IMG_PATH = Path(".").joinpath("data", "whack_a_potato", "debug")

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

CLOSET_COLS = 5
CLOSET_ROWS = 3

CROP_BOX_RAD = 2

WHACK_OFFSET_0 = 353
WHACK_OFFSET_1 = 215

WHACK_WIDTH = 663
WHACK_HEIGHT = 634

BASE_IMG_PATH = Path(".").joinpath("data", "whack_a_potato", "grayscale.png")
img_base = Image.open(BASE_IMG_PATH)

hwnd = 0x23108A


def fill_lists():
    for col in range(CLOSET_COL_OFFSET):
        for row in range(CLOSET_ROWS):
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

    debug_index = 0

    for i in range(40000):
        # Capture the window
        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)

        if result == 1:
            img = get_img(bitmap)
            img_gray = ImageOps.grayscale(img)
            img_gray_crop = img_gray.crop(
                (
                    WHACK_OFFSET_0,
                    WHACK_OFFSET_1,
                    WHACK_OFFSET_0 + WHACK_WIDTH,
                    WHACK_OFFSET_1 + WHACK_HEIGHT,
                )
            )
            img_difference = ImageChops.difference(img_base, img_gray_crop)

            for index, potato_position in enumerate(POTATO_POSITIONS):
                average_box = img_difference.crop(POTATO_CROP_BOX_POSITIONS[index])
                if int(np.average(np.array(average_box))) in ALLOWED_COLORS:
                    # Click at the potato position
                    click_x = potato_position[0] + WHACK_OFFSET_0
                    click_y = potato_position[1] + WHACK_OFFSET_1
                    pyautogui.click(click_x, click_y)
                    if DEBUG:
                        print(
                            "click",
                            str(debug_index).zfill(6),
                            ":",
                            CLOSET_INDEX[index],
                            int(np.average(np.array(average_box))),
                        )

                        # Copy the image to draw on it
                        img_gray = ImageOps.colorize(
                            img_gray, black="black", white="white"
                        )
                        draw = ImageDraw.Draw(img_gray)

                        # Draw a red circle at the click position
                        dot_radius = 5
                        draw.ellipse(
                            (
                                click_x - dot_radius,
                                click_y - dot_radius,
                                click_x + dot_radius,
                                click_y + dot_radius,
                            ),
                            fill="red",
                            outline="red",
                        )

                        img_name = "".join(
                            ["click_", str(debug_index).zfill(6), ".png"]
                        )
                        img_gray.save(DEBUG_IMG_PATH / img_name)
                        debug_index += 1
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
