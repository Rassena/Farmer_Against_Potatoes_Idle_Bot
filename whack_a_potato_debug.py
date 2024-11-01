import datetime
import inspect
from PIL import Image, ImageChops, ImageOps, ImageDraw

from data.whack_a_potato.whack_const import *
from utils import get_img


DEBUG_DRAW_BOX = True
DEBUG_DRAW_CLICK = True

DEBUG_WHACK_POTATO_HIT = True
DEBUG_GAME_BOT = True
DEBUG_START_GAME = True

VERBOSE = True

FORMAT = "png"
CLICK_RAD = 2

WHACK_DEBUG_DICT = {
    "is_potato_hit": DEBUG_WHACK_POTATO_HIT,
    "game_bot": DEBUG_GAME_BOT,
    "start_game": DEBUG_START_GAME,
}


def save_screenshot(bitmap, file_name_suffix, crop_box=None, click=None):
    calframe = inspect.getouterframes(inspect.currentframe(), 2)
    if calframe[1][3] in WHACK_DEBUG_DICT:
        if WHACK_DEBUG_DICT.get(calframe[1][3]):
            now = datetime.datetime.now()
            screenshot_name = now.strftime("%Y_%m_%d_%H_%M_%S") + "_" + file_name_suffix
            if VERBOSE:
                print("save_screenshot caller:", calframe[1][3])
            ImageOps.grayscale(get_img(bitmap)).save(
                DEBUG_FOLDER / (screenshot_name + "." + FORMAT), format=FORMAT
            )
            if crop_box:
                _save_crop_box(bitmap, crop_box, screenshot_name)
            if DEBUG_DRAW_CLICK and click:
                _save_red_click(bitmap, click, file_name_suffix)
            if DEBUG_DRAW_BOX and crop_box:
                _save_red_box(bitmap, crop_box, screenshot_name)
    else:
        print("save_screenshot unknown caller:", calframe[1][3])


def _save_red_box(bitmap, crop_box, screenshot_name):
    screenshot_name += "_draw_box"

    img_grey = ImageOps.grayscale(get_img(bitmap))
    img_grey = ImageOps.colorize(img_grey, black="black", white="white")

    img_with_draw = img_grey.copy()
    draw = ImageDraw.Draw(img_with_draw)
    draw.rectangle(
        ((crop_box[0], crop_box[1]), (crop_box[2], crop_box[3])), outline="red"
    )

    img_with_draw.save(DEBUG_FOLDER / (screenshot_name + "." + FORMAT), format=FORMAT)


def _save_crop_box(bitmap, crop_box, screenshot_name):
    screenshot_name += "_crop_box"
    ImageOps.grayscale(get_img(bitmap).crop(crop_box)).save(
        DEBUG_FOLDER / (screenshot_name + "." + FORMAT), format=FORMAT
    )


def _save_red_click(bitmap, click, screenshot_name):
    screenshot_name += "_draw_click"

    img_grey = ImageOps.grayscale(get_img(bitmap))
    img_grey = ImageOps.colorize(img_grey, black="black", white="white")

    img_with_draw = img_grey.copy()
    draw = ImageDraw.Draw(img_with_draw)
    draw.circle(click, CLICK_RAD, outline="red")

    img_with_draw.save(DEBUG_FOLDER / (screenshot_name + "." + FORMAT), format=FORMAT)
