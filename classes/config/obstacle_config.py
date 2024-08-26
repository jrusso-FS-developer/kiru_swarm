from typing import List

from classes.config.enums.sides import Sides

class ObstacleBlock:
    def __init__(self, 
                 name, 
                 blocker,
                 right_offset, 
                 left_offset, 
                 top_offset, 
                 image_path, 
                 image_animation_path, 
                 image_secondary_animation_path, 
                 is_climable, 
                 is_landable, 
                 is_deadly_on_contact,
                 is_deadly_on_primary_animation,
                 is_deadly_on_secondary_animation,
                 animation_frames,
                 secondary_animation_frames,
                 animation_pause_timer,
                 secondary_animation_pause_timer,
                 hold_animation,
                 DEADLY_SIDES:List[Sides],
                 COLLIDABLE_SIDES:List[Sides]):
        self.name = name 
        self.blocker = blocker   
        self.image_path = image_path
        self.image_animation_path = image_animation_path
        self.image_secondary_animation_path = image_secondary_animation_path
        self.type = type
        self.is_climable = is_climable
        self.is_landable = is_landable
        self.is_deadly_on_contact = is_deadly_on_contact
        self.is_deadly_on_primary_animation = is_deadly_on_primary_animation
        self.is_deadly_on_secondary_animation = is_deadly_on_secondary_animation
        self.top_offset = top_offset
        self.right_offset = right_offset
        self.left_offset = left_offset
        self.animation_frames = animation_frames
        self.secondary_animation_frames = secondary_animation_frames
        self._animation_pause_timer = animation_pause_timer
        self.secondary_animation_pause_timer = secondary_animation_pause_timer
        self._hold_animation = hold_animation
        self.DEADLY_SIDES = DEADLY_SIDES
        self.COLLIDABLE_SIDES = COLLIDABLE_SIDES

    name = ''
    rect = None  
    blocker = False 
    is_climable = False
    is_landable = False
    top_offset = 0
    right_offset = 0
    left_offset = 0
    bottom = 0
    top = 0
    _x = 0
    _y = 0
    image_path = ''
    image_animation_path = ''
    animation_frames = 0
    secondary_animation_frames = 0
    _animation_pause_timer = 0
    secondary_animation_pause_timer = 0
    _hold_animation = 0
    is_deadly_on_contact = False
    is_deadly_on_secondary_animation = False
    is_deadly_on_primary_animation = False
    DEADLY_SIDES:Sides = Sides.NONE
    COLLIDABLE_SIDES:Sides = Sides.NONE
    
class ObstacleConfig:
    TRASHCAN:ObstacleBlock = ObstacleBlock(
                                           'trashcan', # name
                                           True, # blocker
                                           20, # right offset
                                           20, # left offset
                                           95, # top offset
                                           'sprites/assets/obstacles/trashcan/trashcan.png', # image path
                                           'sprites/assets/obstacles/trashcan/trashcan_open_{0}.png', # image animation path
                                           'sprites/assets/obstacles/trashcan/trashcan_open_blink_{0}.png', # image secondary animation path
                                           False, # is climable
                                           True, # is landable
                                           False, # is deadly on contact
                                           True, # is deadly on primary animation
                                           False, # is deadly on secondary animation
                                           11, # animation frames
                                           15, # secondary animation frames
                                           240, # animation pause timer
                                           40, # secondary animation pause timer
                                           120, # hold animation
                                           [Sides.TOP], # deadly sides
                                           [Sides.TOP, Sides.LEFT, Sides.RIGHT] # collidable sides
                                           )
    DONOTENTER_SIGN:ObstacleBlock = ObstacleBlock(
                                           'do_not_enter_sign', # name
                                           False, # blocker
                                           0, # right offset
                                           0, # left offset
                                           0, # top offset
                                           'sprites/assets/obstacles/roadsigns/do_not_enter.png', # image path
                                           '', # image animation path
                                           '', # image secondary animation path
                                           False, # is climable
                                           False, # is landable
                                           False, # is deadly on contact
                                           False, # is deadly on primary animation
                                           False, # is deadly on secondary animation
                                           0, # animation frames
                                           0, # secondary animation frames
                                           0, # animation pause timer
                                           0, # secondary animation pause timer
                                           0, # hold animation
                                           [], # deadly sides
                                           [] # collidable sides
                                           )
    ARROWRIGHT_SIGN:ObstacleBlock = ObstacleBlock(
                                           'arrow_right_sign', # name
                                           False, # blocker
                                           0, # right offset
                                           0, # left offset
                                           0, # top offset
                                           'sprites/assets/obstacles/roadsigns/arrow_right_sign.png', # image path
                                           '', # image animation path
                                           '', # image secondary animation path
                                           False, # is climable
                                           False, # is landable
                                           False, # is deadly on contact
                                           False, # is deadly on primary animation
                                           False, # is deadly on secondary animation
                                           0, # animation frames
                                           0, # secondary animation frames
                                           0, # animation pause timer
                                           0, # secondary animation pause timer
                                           0, # hold animation
                                           [], # deadly sides
                                           [] # collidable sides
                                           )
    PLATFORM_MEDIUM:ObstacleBlock = ObstacleBlock(
                                           'platform_medium', # name
                                           True, # blocker
                                           25, # right offset
                                           25, # left offset
                                           5, # top offset
                                           'sprites/assets/obstacles/platforms/platform_medium.png', # image path
                                           '', # image animation path
                                           '', # image secondary animation path
                                           False, # is climable
                                           True, # is landable
                                           False, # is deadly on contact
                                           False, # is deadly on primary animation
                                           False, # is deadly on secondary animation
                                           0, # animation frames
                                           0, # secondary animation frames
                                           0, # animation pause timer
                                           0, # secondary animation pause timer
                                           0, # hold animation
                                           [], # deadly sides
                                           [Sides.TOP, Sides.LEFT, Sides.RIGHT, Sides.BOTTOM] # collidable sides
                                           )
    PLATFORM_SMALL:ObstacleBlock = ObstacleBlock(
                                           'platform_small', # name
                                           True, # blocker
                                           25, # right offset
                                           25, # left offset
                                           5, # top offset
                                           'sprites/assets/obstacles/platforms/platform_small.png', # image path
                                           '', # image animation path
                                           '', # image secondary animation path
                                           False, # is climable
                                           True, # is landable
                                           False, # is deadly on contact
                                           False, # is deadly on primary animation
                                           False, # is deadly on secondary animation
                                           0, # animation frames
                                           0, # secondary animation frames
                                           0, # animation pause timer
                                           0, # secondary animation pause timer
                                           0, # hold animation
                                           [], # deadly sides
                                           [Sides.TOP, Sides.LEFT, Sides.RIGHT, Sides.BOTTOM] # collidable sides
                                           )