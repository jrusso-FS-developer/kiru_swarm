from enum import Enum

from classes.config.map_config import MapConfig

class Theme(Enum):
    DAY = 1
    NIGHT = 2

class LevelBlock:
    def __init__(self, name, theme, map_config, backdroppath, foregroundpaths, midgroundpaths, music_path):
        self.name = name
        self.backdroppath = backdroppath
        self.foregroundpaths = foregroundpaths
        self.midgroundpaths = midgroundpaths
        self.theme = theme
        self.music_path = music_path
        self.map_config = map_config

    name: str = ''
    backdroppath: str = ''  
    foregroundpaths: list[str] = []
    midgroundpaths: list[str] = []
    theme: Theme = None
    GROUND_TILE: str = ''
    music_path: str = ''
    map_config = None

class LevelConfig(Enum):
    LEVEL_1 = LevelBlock('Day Grinder', 
                    Theme.DAY, 
                    MapConfig.Level1Map,
                    "sprites/backgrounds/city/city_day_backdrop.png",
                    ["sprites/backgrounds/city/city_day_bg_foreground_1.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_2.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_3.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_4.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_5.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_6.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_7.png",
                     "sprites/backgrounds/city/city_day_bg_foreground_8.png"],
                     ["sprites/backgrounds/city/city_day_bg_midground_1.png",
                      "sprites/backgrounds/city/city_day_bg_midground_2.png",
                      "sprites/backgrounds/city/city_day_bg_midground_3.png",
                      "sprites/backgrounds/city/city_day_bg_midground_4.png",
                      "sprites/backgrounds/city/city_day_bg_midground_5.png",
                      "sprites/backgrounds/city/city_day_bg_midground_6.png",
                      "sprites/backgrounds/city/city_day_bg_midground_7.png",
                      "sprites/backgrounds/city/city_day_bg_midground_8.png"],
                      'sounds/music/getting-it-done.mp3')
    LEVEL_2 = LevelBlock('Night Grinder', 
                    Theme.NIGHT,                     
                    MapConfig.Level1Map,
                    "sprites/backgrounds/city/city_night_backdrop.png",
                    ["sprites/backgrounds/city/city_night_bg_foreground_1.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_2.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_3.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_4.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_5.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_6.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_7.png",
                     "sprites/backgrounds/city/city_night_bg_foreground_8.png"],
                     ["sprites/backgrounds/city/city_night_bg_midground_1.png",
                      "sprites/backgrounds/city/city_night_bg_midground_2.png",
                      "sprites/backgrounds/city/city_night_bg_midground_3.png",
                      "sprites/backgrounds/city/city_night_bg_midground_4.png",
                      "sprites/backgrounds/city/city_night_bg_midground_5.png",
                      "sprites/backgrounds/city/city_night_bg_midground_6.png",
                      "sprites/backgrounds/city/city_night_bg_midground_7.png",
                      "sprites/backgrounds/city/city_night_bg_midground_8.png"],
                      'sounds/music/getting-it-done.mp3')