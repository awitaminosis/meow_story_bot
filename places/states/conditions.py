from aiogram.fsm.context import FSMContext


class Transitions:
    @staticmethod
    async def can_go_to_forest(state: FSMContext, location_from):
        state_data = await state.get_data()
        is_showel_mentioned = state_data.get("showel_mentioned", False)
        return is_showel_mentioned and location_from not in {"forest", "t_visit_mouse"}

    @staticmethod
    async def can_fish(state: FSMContext, location_from):  # noqa: ARG004
        state_data = await state.get_data()
        rods_taken = state_data.get("fishing_rods", False)
        worms = state_data.get("worms", 0)
        return rods_taken and worms > 0

    @staticmethod
    async def can_feed_hedgehog(state: FSMContext, location_from):  # noqa: ARG004
        state_data = await state.get_data()
        is_showel_mentioned = state_data.get("showel_mentioned", False)
        return is_showel_mentioned

    @staticmethod
    async def can_visit_mouse(state: FSMContext, location_from):  # noqa: ARG004
        state_data = await state.get_data()
        is_mouse_mentioned = state_data.get("mouse_mentioned", False)
        return is_mouse_mentioned

    @staticmethod
    async def mouse_is_missing(state: FSMContext, location_from):  # noqa: ARG004
        state_data = await state.get_data()
        mouse_quest_level = state_data.get("mouse_quest_level", 0)
        return mouse_quest_level == 3  # noqa: PLR2004

    @staticmethod
    async def mouse_not_missing(state: FSMContext, location_from):
        return not await Transitions.mouse_is_missing(location_from, state)

    @staticmethod
    async def can_take_rods(state: FSMContext, location_from):  # noqa: ARG004
        state_data = await state.get_data()
        rods_taken = state_data.get("fishing_rods", False)
        return not rods_taken
