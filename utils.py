import win32gui
import win32ui
from PIL import Image, ImageOps, ImageChops

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

def difference_between_images(bitmap,img_base, crop_box):
    """Crop ingame image for comparison to whack grayscale.png

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
        img_gray.crop(crop_box),
    )
    return img_difference

def is_game_open():
    pass