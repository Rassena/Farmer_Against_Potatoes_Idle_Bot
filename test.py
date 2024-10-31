import ctypes
import win32gui
import win32ui
import win32con
from PIL import Image, ImageOps, ImageChops
import numpy as np
import pyautogui
import time


POTATO_POSITIONS = []
CLOSET_INDEX = []
POTATO_CROP_BOX_POSITIONS = []
# FROBIDDEN_COLORS = [i for i in range(168, 179)]
# for i in range(0, 51):
#     FROBIDDEN_COLORS.append(i)

ALLOWED_COLORS = []
for i in range(180, 195):
    ALLOWED_COLORS.append(i)
for i in range(152, 160):
    ALLOWED_COLORS.append(i)

for i in range(0,5):
    for j in range(3):
        POTATO_POSITIONS.append((65+131*i, 139+215*j))
        CLOSET_INDEX.append((i,j))
        POTATO_CROP_BOX_POSITIONS.append((63+131*i, 137+215*j, 67+131*i, 141+215*j))

# Replace with the hexadecimal handle of the window you want to capture
window = 0
def windows(hwnd, ctx):
    global window
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) == "Farmer Against Potatoes Idle":
            window = hwnd

win32gui.EnumWindows(windows, None)

hwnd = 0x390f5a

# print(hwnd)

for i in range(40000):
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

        # Capture the window
        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 2)
        if result == 1:
            # Retrieve the bitmap data
            bmpinfo = bitmap.GetInfo()
            bmpstr = bitmap.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            
            img_gray = ImageOps.grayscale(img)
            img_base = Image.open("grayscale.png")

            tmp = ImageChops.difference(img_base, img_gray.crop((353, 215, 1016, 849)))
            
            last_closet = (0,0)
            last_value = 0

            for i in range(len(POTATO_POSITIONS)):
                value = int(tmp.getpixel(POTATO_POSITIONS[i]))
                average_box = tmp.crop(POTATO_CROP_BOX_POSITIONS[i])
                image_array_average = int(np.average(np.array(average_box)))
                if image_array_average in ALLOWED_COLORS:
                    # print(CLOSET_INDEX[i], value, image_array_average)
                    pyautogui.click(POTATO_POSITIONS[i][0]+353, POTATO_POSITIONS[i][1]+215)
                    break
                elif value == 0:
                    pass
                # else:
                    # print("Didn't hit the forbidden color at ", CLOSET_INDEX[i], value, image_array_average)
                    # last_closet = CLOSET_INDEX[i]
                    # last_value = value

            time.sleep(0.001)
        # Convert image to a NumPy array
    #     img_np = np.array(img)

    #     # Define threshold for grayscale detection
    #     threshold = 2

    #     # Identify grayscale pixels by checking if R, G, and B values are close to each other
    #     grayscale_coords = []
    #     for y in range(height):
    #         for x in range(width):
    #             r, g, b = img_np[y, x]
    #             if abs(r - g) < threshold and abs(r - b) < threshold and abs(g - b) < threshold:
    #                 grayscale_coords.append((x, y))
                    # print(f"Grayscale pixel found at ({x}, {y})")

    #     # Optionally, save grayscale-coordinates image for reference
    #     for (x, y) in grayscale_coords:
    #         img_np[y, x] = [255, 0, 0]  # Mark grayscale pixels in red for visibility

    #     img_with_grayscale = Image.fromarray(img_np)
    #     img_with_grayscale.save("window_with_grayscale_marked.png")

    # else:
        # print("Failed to capture the window.")

    # # Clean up
    # dc.DeleteDC()
    # memdc.DeleteDC()
    # win32gui.ReleaseDC(hwnd, hdc)
    # win32gui.DeleteObject(bitmap.GetHandle())
