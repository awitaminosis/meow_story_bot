class Coords:
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

    @classmethod
    def is_night_forest_entry(cls, i, j):
        return i < cls.LOOK_NIGHT_FOREST_ENTRY_X and j < cls.LOOK_NIGHT_FOREST_ENTRY_Y

    @classmethod
    def is_swamp(cls, i, j):
        return (
            cls.LOOK_SWAMP_X_MIN <= i <= cls.LOOK_SWAMP_X_MAX and j < cls.LOOK_SWAMP_Y
        )

    @classmethod
    def is_cave_maw(cls, i, j):
        return i > cls.CAVE_MAW_X and j == cls.CAVE_MAW_Y

    @classmethod
    def is_inside_cave(cls, i, j):
        return i >= cls.INSIDE_CAVE_X and j <= cls.INSIDE_CAVE_Y

    @classmethod
    def is_hedgehog_house(cls, i, j):
        return (
            i >= cls.HEDGEHOG_HOUSE_X
            and cls.HEDGEHOG_HOUSE_Y_MIN <= j <= cls.HEDGEHOG_HOUSE_Y_MAX
        )

    @classmethod
    def is_mouse_house(cls, i, j):
        return (
            cls.MOUSE_HOUSE_X_MIN <= i <= cls.MOUSE_HOUSE_X_MAX
            and cls.MOUSE_HOUSE_Y_MIN <= j <= cls.MOUSE_HOUSE_Y_MAX
        )

    @classmethod
    def is_desert(cls, i, j):
        return (
            cls.DESERT_X_MIN <= i <= cls.DESERT_X_MAX
            and cls.DESERT_Y_MIN <= j <= cls.DESERT_Y_MAX
        )

    @classmethod
    def is_sea(cls, i, j):
        return cls.SEA_X_MIN <= i <= cls.SEA_X_MAX and j >= cls.SEA_Y

    @classmethod
    def is_northern_road(cls, i, j):
        return i >= cls.NORTHERN_ROAD_X and j == cls.NORTHERN_ROAD_Y

    @classmethod
    def is_ball_vicinity(cls, i, j):
        return (
            cls.BALL_VICINITY_X_MIN <= i <= cls.BALL_VICINITY_X_MAX
            and cls.BALL_VICINITY_Y_MIN <= j <= cls.BALL_VICINITY_Y_MAX
        )

    @classmethod
    def is_mountain_spur(cls, i, j):
        return i >= cls.MOUNTAIN_SPURS_X and j == cls.MOUNTAIN_SPURS_Y

    @classmethod
    def is_owl_vicinity(cls, i, j):
        return (
            i >= cls.OWL_VICINITY_X
            and cls.OWL_VICINITY_Y_MIN <= j <= cls.OWL_VICINITY_Y_MAX
        )

    @classmethod
    def is_owl(cls, x, y):
        return x == coords.OWL_X and y == coords.OWL_Y

    @classmethod
    def is_ball(cls, x, y):
        return x == coords.BALL_X and y == coords.BALL_Y

    @classmethod
    def is_cave_mushrooms(cls, x, y):
        return x == coords.CAVE_MUSHROOMS_X and y == coords.CAVE_MUSHROOMS_Y

    @classmethod
    def is_night_forest_start(cls, x, y):
        return x == coords.NIGHT_FOREST_START_X and y == coords.NIGHT_FOREST_START_Y

    @classmethod
    def is_dark_line(cls, new_x, new_y):
        return new_y <= coords.DARK_LINE_BASE_Y or (
            new_y <= coords.DARK_LINE_SQARE_Y and new_x >= coords.DARK_LINE_SQARE_X
        )


coords = Coords()
