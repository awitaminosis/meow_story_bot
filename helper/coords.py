from pydantic import BaseModel


class Coords(BaseModel):
    DESERT_Y_MAX: int = 6
    DESERT_Y_MIN: int = 4
    DESERT_X_MAX: int = 2
    DESERT_X_MIN: int = 1
    SEA_Y: int = 7
    SEA_X_MAX: int = 3
    SEA_X_MIN: int = 2
    OWL_VICINITY_Y_MAX: int = 9
    OWL_VICINITY_Y_MIN: int = 8
    OWL_VICINITY_X: int = 8
    MOUNTAIN_SPURS_Y: int = 10
    MOUNTAIN_SPURS_X: int = 4
    BALL_VICINITY_Y_MAX: int = 9
    BALL_VICINITY_Y_MIN: int = 8
    BALL_VICINITY_X_MAX: int = 6
    BALL_VICINITY_X_MIN: int = 4
    NORTHERN_ROAD_Y: int = 7
    NORTHERN_ROAD_X: int = 4
    MOUSE_HOUSE_Y_MAX: int = 6
    MOUSE_HOUSE_Y_MIN: int = 4
    MOUSE_HOUSE_X_MAX: int = 6
    MOUSE_HOUSE_X_MIN: int = 5
    HEDGEHOG_HOUSE_Y_MAX: int = 6
    HEDGEHOG_HOUSE_Y_MIN: int = 4
    HEDGEHOG_HOUSE_X: int = 8
    INSIDE_CAVE_Y: int = 2
    INSIDE_CAVE_X: int = 8
    CAVE_MAW_Y: int = 3
    CAVE_MAW_X: int = 6
    LOOK_NIGHT_FOREST_ENTRY_Y: int = 3
    LOOK_NIGHT_FOREST_ENTRY_X: int = 4
    LOOK_SWAMP_Y: int = 3
    LOOK_SWAMP_X_MAX: int = 6
    LOOK_SWAMP_X_MIN: int = 5
    OWL_Y: int = 9
    OWL_X: int = 10
    BALL_Y: int = 9
    BALL_X: int = 6
    CAVE_MUSHROOMS_Y: int = 1
    CAVE_MUSHROOMS_X: int = 8
    NIGHT_FOREST_START_Y: int = 2
    NIGHT_FOREST_START_X: int = 3
    NIGHT_FOREST_EXIT_Y: int = 3
    NIGHT_FOREST_EXIT_X: int = 3
    DARK_LINE_SQARE_X: int = 7
    DARK_LINE_SQARE_Y: int = 6
    DARK_LINE_BASE_Y: int = 3


coords = Coords()
