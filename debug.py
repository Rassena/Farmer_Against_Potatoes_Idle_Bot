import ctypes
from time import sleep

import numpy as np
import pyautogui
import win32gui
import win32ui
from PIL import Image, ImageChops, ImageOps

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

WHACK_OFFSET_X = 353
WHACK_OFFSET_Y = 215

WHACK_WIDTH = 663
WHACK_HEIGHT = 634

WHACK_REWARD_POPUP_CHECK_BOX_1 = (387, 200, 405, 212)
WHACK_REWARD_POPUP_CHECK_BOX_2 = (512, 200, 531, 212)
START_BUTTON_COORDINATES = (661, 987)

img_base = Image.open("grayscale.png")
hwnd = win32gui.FindWindow(None, WINDOW_NAME)


def fill_lists():
    """
    Fill lists with closet data
    """
    for col in range(5):
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

def diffrence_between_images(bitmap, crop_box, img_base=img_base):
    """    Crop ingame image for comparasion to whack grayscale.png

    Args:
        bitmap (bitmap): Bitmap of game window

        img_base (Image, optional): Different image used as a base
        
        crop_box (tuple, optional): where to crop the bitmap to

    Returns:
        Image: Image difference between bitmap and grayscale.png
    """
    img = get_img(bitmap)
    img_gray = ImageOps.grayscale(img)
    img_difference = ImageChops.difference(
        img_base,
        img_gray.crop(
                crop_box
        ),
    )
    return img_difference

def get_bitmap(hwnd):
    """Get game window bitmap for further processing

    Args:
        hwnd (hex): Game window hwnd

    Returns:
        tuple (PyDC, PyDC): ja nie wiem co to jest xD, Bitmap of game window
    """
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
    
    return memdc, bitmap

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
                img_difference = diffrence_between_images(bitmap, 
                                    crop_box=(WHACK_OFFSET_X, WHACK_OFFSET_Y, WHACK_OFFSET_X + WHACK_WIDTH, WHACK_OFFSET_Y + WHACK_HEIGHT)
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
                if int(np.average(np.array(img_difference.crop(WHACK_REWARD_POPUP_CHECK_BOX_1)))) in range (50, 60) and int(np.average(np.array(img_difference.crop(WHACK_REWARD_POPUP_CHECK_BOX_2)))) in range (50, 60):
                    img_difference.save("last_img.png")
                    # print("Broke!")
                    break

    # Check if player is in game (window is not minimised)
    if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
        # print("checking window")
        memdc, bitmap = get_bitmap(hwnd)
        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)
        img_difference = diffrence_between_images(bitmap, 
                            crop_box=(WHACK_OFFSET_X, WHACK_OFFSET_Y, WHACK_OFFSET_X + WHACK_WIDTH, WHACK_OFFSET_Y + WHACK_HEIGHT)
                            )
        shop_image = diffrence_between_images(bitmap, 
                            img_base=Image.open("grayscale_shop.png"), 
                            crop_box=(1474, 909, 1654, 994)
                            )
        #check if player is in whack main window or in whack shop
        if int(np.average(np.array(img_difference))) <= 1 or int(np.average(np.array(shop_image))) <= 10:
            # Start whack
            print("starting whacking")
            pyautogui.click(
                START_BUTTON_COORDINATES[0],
                START_BUTTON_COORDINATES[1]
            )
            game_bot()
            # sleep(305)
        else:
            pass 
            # code for checking if player is in main game window and checking if whack has ended - to be done
    else:
        print("sleeping")
        sleep(5)



# def background_screenshot(hwnd, width, height):
#     wDC = win32gui.GetWindowDC(hwnd)
#     dcObj=win32ui.CreateDCFromHandle(wDC)
#     cDC=dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
#     dataBitMap.SaveBitmapFile(cDC, 'test.bmp')
#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC)
#     win32gui.DeleteObject(dataBitMap.GetHandle())


# windowname="Farmer Against Potatoes Idle"

# hwnd = FindWindow(None, windowname)
# print(hex(hwnd))
# background_screenshot(hwnd, 1280, 780)

# def windows(hwnd, ctx):
#     if win32gui.IsWindowVisible(hwnd):
#         if win32gui.GetWindowText(hwnd) == windowname:
#             print(hex(hwnd), win32gui.GetWindowText(hwnd))

# win32gui.EnumWindows(windows, None)