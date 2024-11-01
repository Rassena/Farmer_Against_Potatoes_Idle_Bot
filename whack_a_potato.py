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
#       ? get info which buff get ?
#       ? isolate const to other file ?
#       ? update requirement ?
#       ? use LOG instead of print ?
#       ? add auto create subfolder debug ?
#       ? use git branches ?

DEBUG = True
VERBOSE = True

wack_board_grey = Image.open(WHACK_BOARD_GREY_IMAGE)
wack_ready_grey = Image.open(WHACK_READY_IMAGE)
wack_header_grey = Image.open(WHACK_HEADER_IMAGE)
wack_shop_grey = Image.open(WHACK_SHOP_GREY_IMAGE)

hwnd = win32gui.FindWindow(None, WINDOW_NAME)


def is_wack_ready(bitmap):
    """
    Return bool if game is in whack mini-game
    """
    img_difference = difference_between_images(
        bitmap,
        wack_ready_grey,
        crop_box=WHACK_POTATOES_READY_BOX,
    )
    return np.average(np.array(img_difference)) < 1


def is_in_whack(bitmap):
    """
    Return bool if game is in whack module
    """
    img_difference = difference_between_images(
        bitmap,
        wack_header_grey,
        crop_box=WHACK_HEADER_CHECK_BOX,
    )
    return np.average(np.array(img_difference)) < 1


def is_reward_granted(img_difference):
    """
    Return bool if whack reward granted
    """

    if int(
        np.average(np.array(img_difference.crop(WHACK_REWARD_POPUP_CHECK_BOX_1)))
    ) in range(50, 60) and int(
        np.average(np.array(img_difference.crop(WHACK_REWARD_POPUP_CHECK_BOX_2)))
    ) in range(
        50, 60
    ):
        return True
    else:
        return False


def is_potato_hit(average_box, potato_position):
    if int(np.average(np.array(average_box))) in ALLOWED_COLORS:
        pyautogui.click(
            potato_position[0] + WHACK_BOARD_OFFSET_X,
            potato_position[1] + WHACK_BOARD_OFFSET_Y,
        )
        return True
    else:
        return False


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
                    wack_board_grey,
                    crop_box=WHACK_CLOSET_POTATO_BOX,
                )
                for index, potato_position in enumerate(POTATO_POSITIONS):
                    average_box = img_difference.crop(POTATO_CROP_BOX_POSITIONS[index])
                    if is_potato_hit(average_box, potato_position):
                        break
                # detect reward
                if is_reward_granted(img_difference):
                    if DEBUG:
                        save_screenshot(bitmap, "Whack_finish")
                    print("Whack finished")
                    break


while True:
    # Check if player is in game (window is not minimised)
    if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
        # print("checking window")
        memdc, bitmap = get_bitmap(hwnd)
        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)
        # check if player is in whack main window
        if is_in_whack(bitmap):
            # Start whack
            if is_wack_ready(bitmap):
                if DEBUG:
                    save_screenshot(bitmap, "Whack_start")
                print("start whacking")
                pyautogui.click(
                    WHACK_START_BUTTON_COORDINATES[0], WHACK_START_BUTTON_COORDINATES[1]
                )
                game_bot()
                print("sleep 5 min")
                sleep(305)
            else:
                if VERBOSE:
                    print("Wack is not ready")
                sleep(5)
        else:
            # code for checking if player is in main game window and checking if whack has ended - to be done
            if VERBOSE:
                print("Not in Whack module")
            sleep(5)
    else:
        if VERBOSE:
            print("sleeping")
        sleep(5)
