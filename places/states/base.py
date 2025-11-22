from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helper.app import dp


class Location:
    def __init__(self, location, controller):
        self.location = location
        self.controller = controller

    def register(self):
        raise NotImplementedError("unknown type:" + self.handler_type)

    async def get_keyboard(self, state: FSMContext):
        builder = InlineKeyboardBuilder()
        for place, place_text, keyboard_type, condition, extra in self.can_reach:
            if extra.get("coords", None) is not None:
                x, y = extra["coords"]
                place += f"__{x},{y}"  # noqa: PLW2901
            elif extra.get("action", None) is not None:
                action = extra["action"]
                place += f"--{action}"  # noqa: PLW2901
            if condition:
                if await condition(self.location, state) and keyboard_type == "inline":
                    builder.row(
                        InlineKeyboardButton(text=place_text, callback_data=place)
                    )
            elif keyboard_type == "inline":
                builder.row(InlineKeyboardButton(text=place_text, callback_data=place))
        keyboard = builder.as_markup()
        return keyboard


class LocationCallbackQuery(Location):
    def register(self):
        dp.callback_query.register(self.handler, self.filter)

    async def filter(self, callback_query):
        return callback_query.data == self.location


class LocationCommand(Location):
    def register(self):
        dp.message.register(self.handler, self.filter)


class LocationMessage(Location):
    def register(self):
        dp.message.register(self.handler, self.filter)


class LocationWebApp(Location):
    def register(self):
        dp.message.register(self.handler, self.filter)
