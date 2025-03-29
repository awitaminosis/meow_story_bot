from places.states.base import *


class Inventory(LocationMessage):
    location = 'load'

    def __init__(self, controller):
        super().__init__(self.location, controller)

    async def handler(self, message: Message, state: FSMContext):
        try:
            chat_id = message.chat.id
            state_data = await state.get_data()
            print('Инвентарь: ', state_data)
            worms = state_data.get('worms', 0)
            pool_fish_pcs = state_data.get('pool_fish_pcs', 0)
            river_fish_pcs = state_data.get('river_fish_pcs', 0)
            sea_fish_pcs = state_data.get('sea_fish_pcs', 0)
            rods_taken = state_data.get('fishing_rods', False)
            showel_taken = state_data.get('showel_taken', False)
            glowing_rod = state_data.get('glowing_rod', False)
            glowing_mushroom = state_data.get('glowing_mushroom', False)

            if worms:
                text = f'червей: {worms}'
                await say(bot, chat_id,[text])
            if rods_taken:
                text = f'удочки: есть'
                await say(bot, chat_id,[text])
            if showel_taken:
                text = f'лопата: есть'
                await say(bot, chat_id,[text])
            if pool_fish_pcs:
                text = f'рыбы из лужи (штук): {pool_fish_pcs}'
                await say(bot, chat_id,[text])
            if river_fish_pcs:
                text = f'рыбы из речки (штук): {river_fish_pcs}'
                await say(bot, chat_id,[text])
            if sea_fish_pcs:
                text = f'рыбы из моря (штук): {sea_fish_pcs}'
                await say(bot, chat_id,[text])
            if glowing_rod:
                text = f'Светящаяся удочка: есть'
                await say(bot, chat_id,[text])
            if glowing_mushroom:
                text = f'Светящийся гриб: есть'
                await say(bot, chat_id,[text])
            if not worms and not rods_taken and not showel_taken and not pool_fish_pcs and not river_fish_pcs and not sea_fish_pcs:
                await say(bot,chat_id,['Пока что пусто'])
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def filter(self,F):
        return F.text == 'Инвентарь'
