import importlib


class StateController:
    state_classes_dir = 'places.states'
    file2class = {
        #название файла : класс
        #start (из places.states.start) : Start
        'start': 'Start',
        'tiger_home': 'TigerHomeLocation',
        'do_fishing_by_range': 'DoFishingByRange',
        'do_fishing_in_sea': 'DoFishingInSea',
        'enter_forest': 'EnterForest',
        'feed_hedgehog': 'FeedHedgehog',
        'go_fishing': 'GoFishing',
        'go_fishing_in_pool': 'GoFishingInPool',
        'go_fishing_in_river': 'GoFishingInRiver',
        'go_fishing_in_sea': 'GoFishingInSea',
        'hedgehog_home': 'HedgehogHome',
        'inventory': 'Inventory',
        'load': 'Load',
        'mouse_give_quest': 'MouseGiveQuest',
        'news': 'News',
        'rods_taken': 'RodsTaken',
        'save': 'Save',
        'start_new_story': 'StartNewStory',
        'visit_mouse': 'VisitMouse',
        'worms_dig': 'WormsDig',
    }

    def __init__(self):
        pass

    def includeClasses(self):
        for k, v in self.file2class.items():
            module = importlib.import_module(self.state_classes_dir + '.' + k)
            a_class = getattr(module, v)
            a_class().register()


StateController().includeClasses()
