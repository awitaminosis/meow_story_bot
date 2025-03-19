from aiogram.fsm.context import FSMContext


class Transitions:
    @staticmethod
    async def can_go_to_forest(location_from, state: FSMContext):
        state_data = await state.get_data()
        is_showel_mentioned = state_data.get('showel_mentioned', False)
        if is_showel_mentioned:
            if location_from != 'forest' and location_from != 't_visit_mouse':
                return True
        return False

    @staticmethod
    async def can_fish(location_from, state: FSMContext):
        state_data = await state.get_data()
        rods_taken = state_data.get('fishing_rods', False)
        worms = state_data.get('worms', 0)
        return rods_taken and worms > 0

    @staticmethod
    async def can_feed_hedgehog(location_from, state: FSMContext):
        state_data = await state.get_data()
        is_showel_mentioned = state_data.get('showel_mentioned', False)
        return is_showel_mentioned

    @staticmethod
    async def can_visit_mouse(location_from, state: FSMContext):
        state_data = await state.get_data()
        is_mouse_mentioned = state_data.get('mouse_mentioned', False)
        return is_mouse_mentioned

    @staticmethod
    async def mouse_is_missing(location_from, state: FSMContext):
        state_data = await state.get_data()
        mouse_quest_level = state_data.get('mouse_quest_level', 0)
        return mouse_quest_level == 3

    @staticmethod
    async def mouse_not_missing(location_from, state: FSMContext):
        return not await Transitions.mouse_is_missing(location_from, state)

    @staticmethod
    async def can_take_rods(location_from, state: FSMContext):
        state_data = await state.get_data()
        rods_taken = state_data.get('fishing_rods', False)
        return not rods_taken
