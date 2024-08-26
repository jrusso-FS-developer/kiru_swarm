# globals import
from typing import Tuple
import globals

# dependency imports
import pygame
from Box2D import (b2PolygonShape, b2FixtureDef, b2BodyDef)

# class objects
from classes.config.map_config import MapObstacleBlock
from classes.config.enums.sides import Sides
from classes.debugger import Debugger

class Obstacle(MapObstacleBlock):
    def __init__(self, config: MapObstacleBlock):
        super().__init__( 
                        config,
                        config._x, 
                        config._bottom)
        self.set()

    # vars
    actively_deadly = False
    collision_side:Sides = None
    landed_on = False
    poly_fixture: b2FixtureDef = None

    _surf:pygame.surface.Surface = None   
    _rect:pygame.rect.Rect = None  
    _animation_frame = -1
    _secondary_animation_frame = -1
    _animation_timer = 0
    _secondary_animation_timer = 0
    _animation_hold_timer = 0
    _animation_reverse = False
    _physics_body = None
    _physics_body_def: b2BodyDef = None
    _poly_shape: b2PolygonShape = None

    def set(self):
        self._surf = pygame.image.load(self.image_path)
        self._rect = self._surf.get_rect()
        self._animation_pause_timer = 240
        self._animation_frame = -1
        self._animation_timer = self._animation_pause_timer
        self._secondary_animation_timer = self.secondary_animation_pause_timer
        self._animation_hold_timer = self._hold_animation

        # create physics poly/fixture
        if self.blocker:
            self._poly_shape = b2PolygonShape(box=(self.get_width() / 2, self.get_height() / 2))
            self.poly_fixture = b2FixtureDef(shape=self._poly_shape, density=1, friction=0.3)
            self._physics_body_def = b2BodyDef(position=(self.get_x_center(), self.get_y_center()))
            self._physics_body = globals.physics_world.CreateBody(self._physics_body_def)
            self._physics_body.CreateFixture(self.poly_fixture)
            self._physics_body.userData = 'blocker'

        # set position correctly for physics body
        self.set_position(self._x, self._bottom - self.get_height() - self.top_offset)

    def get_top(self):
        return self._rect.y + self.top_offset
    
    def get_bottom(self):
        return self._rect.bottom

    def get_x_center(self):
        return self._rect.x + self._rect.width / 2
    
    def get_y_center(self):
        return self._rect.y + self._rect.height / 2
    
    def get_width(self):
        return self._rect.width - self.left_offset - self.right_offset
    
    def get_height(self):
        return self._rect.height - self.top_offset
    
    def get_left(self):
        return self._rect.x + self.left_offset
    
    def get_right(self):    
        return self._rect.x + self.get_width() - self.right_offset
    
    def get_position(self) -> Tuple[int, int]: 
        return (self.get_x_center(), self.get_y_center())
    
    def set_position(self, x = None, y = None):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y
        if self._physics_body != None:
            self._physics_body.position = (self.get_x_center() / globals.PPM, self.get_y_center() / globals.PPM)

    def draw(self, speed):
        new_x = self._x - speed if not globals.game_paused and globals.game_moving else self._rect.x
        self.set_position(new_x)  
        self.animate()
        globals.SCREEN.blit(self._surf, self._rect)        

    def animate(self):  
        if (globals.game_paused or globals.player.is_dying):
            return 
        
        # wait until timer is up
        if (self._animation_timer > 0):
            self._animation_timer -= 1
            return 
        
        # animate
        if (self.animation_frames > 0):
            if (self._animation_frame < self.animation_frames and not self._animation_reverse):
                self._animation_frame += 1
                self._surf = pygame.image.load(self.image_animation_path.format(self._animation_frame))

                if (self.is_deadly_on_primary_animation):
                    if (self._animation_frame > self.animation_frames - self.animation_frames / 3):
                        self.actively_deadly = True
            else:
                if (self._animation_hold_timer > 0):
                    self._animation_hold_timer -= 1

                    if (self._secondary_animation_timer > 0):
                        self._secondary_animation_timer -= 1
                        return
                    
                    # animate secondary
                    if (self._secondary_animation_frame < self.secondary_animation_frames):
                        self._secondary_animation_frame += 1
                        self._surf = pygame.image.load(self.image_secondary_animation_path.format(self._secondary_animation_frame))
                    else:
                        self._secondary_animation_frame = -1
                        self._secondary_animation_timer = self.secondary_animation_pause_timer                
                elif(self._animation_frame > 0):
                    self._animation_reverse = True
                    self._animation_frame -= 1
                    self._surf = pygame.image.load(self.image_animation_path.format(self._animation_frame))
                else:
                    self._surf = pygame.image.load(self.image_path)
                    self._animation_timer = self._animation_pause_timer
                    self._animation_reverse = False
                    self._animation_hold_timer = self._hold_animation
                    self._secondary_animation_timer = self.secondary_animation_pause_timer
                    self.actively_deadly = False if not self.is_deadly_on_contact else self.is_deadly_on_contact