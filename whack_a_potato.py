import ctypes
from time import sleep

import numpy as np
import pyautogui
import win32gui
from PIL import Image

from data.const import WINDOW_NAME
from data.whack_a_potato.whack_const import *
from utils import difference_between_images, get_bitmap
from whack_a_potato_debug import *

#   TODO:
#       get all whack buff icon
#       fix if whack can start
#       add check if in wack by "WHACK A POTATO" header screenshot
#       use asyncio for debug
#
#
#       ? isolate const to other file ?
#       ? update requirement ?
#       ? use LOG instead of print ?
#       ? add auto create subfolder debug ?
#       ? use git branches ?

DEBUG = True

img_base = Image.open(WHACK_BOARD_GREY_IMAGE)
hwnd = win32gui.FindWindow(None, WINDOW_NAME)


def is_board_visible():
    """
    Return bool if game is in whack mini-game
    """
    pass


def is_in_whack():
    """
    Return bool if game is in whack module
    """
    pass

def is_reward_granted():
    """
    Return bool if whack reward granted
    """
    pass


def game_bot():
    """
    Whack playing bot
    """
    if win32gui.IsWindow(hwnd):

        memdc, bitmap = get_bitmap(hwnd)
        while True:
            # Capture the window
            result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)

            if result == 1:
                img_difference = difference_between_images(
                    bitmap,
                    img_base,
                    crop_box=WHACK_CLOSET_POTATO_BOX,
                )
                for index, potato_position in enumerate(POTATO_POSITIONS):
                    average_box = img_difference.crop(POTATO_CROP_BOX_POSITIONS[index])
                    if int(np.average(np.array(average_box))) in ALLOWED_COLORS:
                        # print(CLOSET_INDEX[i], value, image_array_average)
                        pyautogui.click(
                            potato_position[0] + WHACK_OFFSET_X,
                            potato_position[1] + WHACK_OFFSET_Y,
                        )
                        break
                # detect reward
                if int(
                    np.average(
                        np.array(img_difference.crop(WHACK_REWARD_POPUP_CHECK_BOX_1))
                    )
                ) in range(50, 60) and int(
                    np.average(
                        np.array(img_difference.crop(WHACK_REWARD_POPUP_CHECK_BOX_2))
                    )
                ) in range(
                    50, 60
                ):
                    save_screenshot(bitmap, "Whack_finish") if DEBUG else 0
                    print("Whack finished")
                    break


while True:
    # Check if player is in game (window is not minimised)
    if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
        # print("checking window")
        memdc, bitmap = get_bitmap(hwnd)
        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)
        img_difference = difference_between_images(
            bitmap,
            img_base,
            crop_box=WHACK_CLOSET_POTATO_BOX,
        )
        shop_image = difference_between_images(
            bitmap,
            img_base=Image.open(WHACK_SHOP_IMAGE),
            crop_box=(1474, 909, 1654, 994),
        )
        # check if player is in whack main window or in whack shop
        if (
            int(np.average(np.array(img_difference))) <= 1
            or int(np.average(np.array(shop_image))) <= 10
        ):
            # Start whack
            print("starting whacking")
            save_screenshot(bitmap, "Whack_start") if DEBUG else 0
            pyautogui.click(START_BUTTON_COORDINATES[0], START_BUTTON_COORDINATES[1])
            game_bot()
            # sleep(305)
        else:
            pass
            # code for checking if player is in main game window and checking if whack has ended - to be done
    else:
        print("sleeping")
        sleep(5)
