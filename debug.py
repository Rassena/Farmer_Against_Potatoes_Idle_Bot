import win32gui
import win32ui
import win32con
from win32gui import FindWindow

def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, 'test.bmp')
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


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
