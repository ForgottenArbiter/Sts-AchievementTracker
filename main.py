import json
import os

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ReferenceListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock

ACHIEVEMENT_DICT = {
    "GUARDIAN": "The Guardian",
    "GHOST_GUARDIAN": "The Ghost",
    "SLIME_BOSS": "The Boss",
    "CHAMP": "The Champion",
    "AUTOMATON": "The Automaton",
    "COLLECTOR": "The Collector",
    "CROW": "The Crow",
    "SHAPES": "The Shapes",
    "TIME_EATER": "The Time Eater",
    "RUBY": "Ruby",
    "EMERALD": "Emerald",
    "SAPPHIRE": "Sapphire",
    "AMETHYST": "Amethyst",
    "SHRUG_IT_OFF": "Shrug It Off",
    "PURITY": "Purity",
    "COME_AT_ME": "Come At Me",
    "THE_PACT": "The Pact",
    "ADRENALINE": "Adrenaline",
    "POWERFUL": "Powerful",
    "JAXXED": "Jaxxed",
    "IMPERVIOUS": "Impervious",
    "BARRICADED": "Barricaded",
    "CATALYST": "Catalyst",
    "PLAGUE": "Plague",
    "NINJA": "Ninja",
    "INFINITY": "Infinity",
    "YOU_ARE_NOTHING": "You Are Nothing",
    "PERFECT": "Perfect",
    "ONE_RELIC": "Who Needs Relics?",
    "SPEED_CLIMBER": "Speed Climber",
    "ASCEND_0": "Ascend 0",
    "MINIMALIST": "Minimalist",
    "DONUT": "Ooh Donut!",
    "COMMON_SENSE": "Common Sense",
    "FOCUSED": "Focused",
    "NEON": "Neon",
    "TRANSIENT": "The Transient",
    "RUBY_PLUS": "Ruby+",
    "EMERALD_PLUS": "Emerald+",
    "SAPPHIRE_PLUS": "Sapphire+",
    "AMETHYST_PLUS": "Amethyst+",
    "THE_ENDING": "The End?",
    "LUCKY_DAY": "My Lucky Day"
}


# Change to whatever the directory of your preferences folder is
SAVE_DIR = "D:\\SteamLibrary\\steamapps\\common\\SlayTheSpire\\preferences\\"


def read_achievements():
    # This may need to change depending on which save slot you're using
    achieve_file = os.path.join(SAVE_DIR, "STSAchievements")
    with open(achieve_file, 'r') as f:
        d = json.load(f)
        proper_keys = set()
        for item in d:
            if item in ACHIEVEMENT_DICT:
                proper_keys.add(item)
        return proper_keys


class Base(GridLayout):
    aList = ObjectProperty(None)
    header = ObjectProperty(None)
    title_text = StringProperty("{}/{} Achievements".format(0, len(ACHIEVEMENT_DICT)))
    num_achievements = 0

    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)
        self.rows_minimum = {0: 50, 1: 100}
        self.cols = 1

    def update_label(self, new_num):
        self.title_text = "{}/{} Achievements".format(new_num, len(ACHIEVEMENT_DICT))

    def check_achievements(self, dt):
        try:
            a_dict = read_achievements()
        except Exception:
            return
        new_num_achievements = len(a_dict)
        if new_num_achievements != self.num_achievements:
            self.num_achievements = new_num_achievements
            self.update_label(new_num_achievements)
            for item in ACHIEVEMENT_DICT:
                if item in a_dict:
                    self.aList.widget_dict[item].g = 0.5
                    self.aList.widget_dict[item].r = 0
                else:
                    self.aList.widget_dict[item].g = 0
                    self.aList.widget_dict[item].r = 0.6


class AchievementEntry(Label):
    name = StringProperty("test")
    r = NumericProperty(0.8)
    g = NumericProperty(0)
    b = NumericProperty(0)
    a = NumericProperty(0)
    rgb = ReferenceListProperty(r, g, b, a)

    def __init__(self, **kwargs):
        super(AchievementEntry, self).__init__(**kwargs)
        self.font_size = 20


class AchievementList(GridLayout):

    def __init__(self, **kwargs):
        super(AchievementList, self).__init__(**kwargs)
        self.widget_dict = {}
        self.cols = 3
        for item in ACHIEVEMENT_DICT:
            new_widget = AchievementEntry(text=ACHIEVEMENT_DICT[item], r=0.8)
            self.add_widget(new_widget)
            self.widget_dict[item] = new_widget


class AchievementApp(App):

    def build(self):
        base = Base()
        Clock.schedule_interval(base.check_achievements, 1/5.0)
        return base


if __name__ == '__main__':
    AchievementApp().run()
