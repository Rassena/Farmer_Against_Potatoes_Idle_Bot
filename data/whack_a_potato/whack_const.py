from pathlib import Path

WHACK_FOLDER = Path(__file__).parent
DEBUG_FOLDER = WHACK_FOLDER / "debug"

WHACK_BOARD_GREY_IMAGE = WHACK_FOLDER / "grayscale_whack_board.png"
WHACK_SHOP_IMAGE = WHACK_FOLDER / "grayscale_shop.png"

POTATO_POSITIONS = []
CLOSET_INDEX = []
POTATO_CROP_BOX_POSITIONS = []

NORMAL_POTATO_COLORS = list(range(180, 195))
GREAT_POTATO_COLORS = list(range(152, 160))
ALLOWED_COLORS = NORMAL_POTATO_COLORS + GREAT_POTATO_COLORS

FIRST_CLOSET_CENTER = (65, 139)
CLOSET_COL_OFFSET = 131
CLOSET_ROW_OFFSET = 215

CLOSET_ROWS = 3
CLOSET_COLUMNS = 5

CROP_BOX_RAD = 2

WHACK_OFFSET_X = 353
WHACK_OFFSET_Y = 215

WHACK_WIDTH = 663
WHACK_HEIGHT = 634

WHACK_REWARD_POPUP_CHECK_BOX_1 = (387, 200, 405, 212)
WHACK_REWARD_POPUP_CHECK_BOX_2 = (512, 200, 531, 212)
START_BUTTON_COORDINATES = (661, 987)

WHACK_CLOSET_POTATO_BOX=(
    WHACK_OFFSET_X,
    WHACK_OFFSET_Y,
    WHACK_OFFSET_X + WHACK_WIDTH,
    WHACK_OFFSET_Y + WHACK_HEIGHT,
)

def fill_lists():
    """
    Fill lists with closet data
    """
    for col in range(CLOSET_COLUMNS):
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


fill_lists()
