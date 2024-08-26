# system imports
import random
from typing import List, Tuple

# dependency imports
import pygame
from Box2D import (b2PolygonShape, b2FixtureDef, b2BodyDef, b2Vec2)

# global vars
from classes.config.enums.danger_zone import DangerZone
from classes.config.enums.directions import Direction
from classes.halo import Halo
from classes.raycastcallback import RayCastCallback
import globals

# class objects
from classes.config.enums.sides import Sides
from classes.obstacle import Obstacle
from classes.config.map_config import MapEnemyBlock
from classes.debugger import Debugger

class Enemy(MapEnemyBlock):
    def __init__(self, 
                 config: MapEnemyBlock):
        super().__init__(config, config._initial_x, config._initial_y)
        self.set()  

    # constants
    LEFT_BOUNDARY:int = 0
    RIGHT_BOUNDARY:int = 0

    # vars
    is_dead = False
    mask: pygame.mask.Mask = None
    poly_fixture: b2FixtureDef = None

    _attack_animation_frame:int = 0
    _attack_completion_timer = 0
    _is_attacking:bool = False
    _is_hurt:bool = False
    _begin_attack_animation_frame:int = 0
    _debugger_message = ''
    _distance_x = 0
    _distance_y = 0
    _enemy_attack_position = (0, 0)
    _fallback_direction: Direction = Direction.NONE
    _fallback_position = (0, 0)
    _flip = False
    _flying = False
    _halo: Halo = None
    _hurt_animation_frame:int = 0
    _hurt_pause_frame = 0
    _hurt_pause_frames = 20
    _health = 100
    _initial_x = 0
    _initial_y = 0
    _is_walking = False
    _main_animation_frame:int = 0
    _physics_body = None
    _physics_body_def: b2BodyDef = None
    _player_attack_position = (0, 0)
    _poly_shape: b2PolygonShape = None
    _rect:pygame.rect.Rect = None
    _stun_time: int = 0
    _surf:pygame.surface.Surface = None 
    _thinking_frames:int  = 0

    def __str__(self):
        return self._name
        
    def set(self):
        self.is_dead = False
        self._is_attacking = False
        self._is_hurt = False
        self._attack_animation_frame = 0
        self._begin_attack_animation_frame = 0
        self._fallback_direction = Direction.NONE
        self._fallback_position = (0, 0)
        self._halo = Halo()
        self._health = 100
        self._hurt_animation_frame = 0
        self._hurt_pause_frame = 0
        self._stun_time = 0
        self._thinking_frame = 0
        self._thinking_frames = random.randint(self.THINKING_FRAME_RANGE[0], self.THINKING_FRAME_RANGE[1])
        self._main_animation_frame = 0

        # set boundaries
        self.LEFT_BOUNDARY = self.BOUNDARIES[0]
        self.RIGHT_BOUNDARY = self.BOUNDARIES[1]

        # set initial offsets
        self._top_offset = self.OFFSETS[0]
        self._right_offset = self.OFFSETS[1]
        self._bottom_offset = self.OFFSETS[2]
        self._left_offset = self.OFFSETS[3]

        # create image/mask
        self._surf = pygame.image.load(f'{self.ASSET_PATH}/{self.STILL_IMAGE}')
        self._rect = self._surf.get_rect()
        self.mask = pygame.mask.from_surface(self._surf)

        # create physics poly/fixture
        self._poly_shape = b2PolygonShape(box=(self.get_width() / 2, self.get_height() / 2))
        self.poly_fixture = b2FixtureDef(shape=self._poly_shape, density=1, friction=0.3)
        self._physics_body_def = b2BodyDef(position=(self.get_x_center(), self.get_y_center()))
        self._physics_body = globals.physics_world.CreateBody(self._physics_body_def)
        self._physics_body.CreateFixture(self.poly_fixture)
        self._physics_body.userData = 'enemy'
        self.set_position(self._initial_x, self._initial_y)

    def get_top(self):
        return self._rect.y + self._top_offset
    
    def get_bottom(self):
        return self._rect.bottom - self._bottom_offset
    
    def get_x(self):
        return self._rect.x
    
    def get_y(self):
        return self._rect.y

    def get_x_center(self):
        return self._rect.x + self._rect.width / 2
    
    def get_y_center(self):
        return self._rect.y + self._rect.height / 2
    
    def get_width(self):
        return self._rect.width - self._left_offset - self._right_offset
    
    def get_height(self):
        return self._rect.height - self._top_offset - self._bottom_offset
    
    def get_left(self):
        return self._rect.x + self._left_offset
    
    def get_right(self):    
        return self._rect.x + self.get_width() - self._right_offset
    
    def get_center_position(self) -> Tuple[int, int]: 
        return (self.get_x_center(), self.get_y_center())
    
    def get_position(self) -> Tuple[int, int]: 
        return (self.get_x(), self.get_y())
    
    def hit(self):
        _reducer = (globals.player.active_weapon.DAMAGE * self.DURABILITY)
        self._health -= (globals.player.active_weapon.DAMAGE - _reducer) if not globals.DEBUG_MODE else 0
        self._is_hurt = True
        self._hurt_animation_frame = 0
        globals.player.active_weapon.play_hit()
        self._stun_time = globals.player.active_weapon.STUN_TIME
    
    def set_position(self, x = None, y = None):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y
        self._physics_body.position = (self.get_x_center() / globals.PPM, self.get_y_center() / globals.PPM)

    def reset_attack(self):
        self._is_attacking = False
        self._begin_attack_animation_frame = 0
        self._thinking_frame = 0
        self._top_offset = self.OFFSETS[0]
        self._right_offset = self.OFFSETS[1]
        self._bottom_offset = self.OFFSETS[2]
        self._left_offset = self.OFFSETS[3]
        self._hurt_animation_frame = 0
        self._hurt_pause_frame = 0
        self._is_hurt = False

    # keep enemy in same place as ground moves
    def move_with_ground(self):      
        # set enemy on the ground
        self.set_position(None, self.FLOOR - self.get_height())    

        if (self._fallback_position == (0, 0)):
            # move enemy laterally  
            if (globals.game_moving and not globals.player.is_dying):
                self.set_position(self._rect.x - globals.ground_scroll_speed)

        # set the still image
        self._surf = pygame.image.load(f'{self.ASSET_PATH}/standing_still_backwards.png') if (self._flip) else pygame.image.load(f'{self.ASSET_PATH}/standing_still.png')
 
    # fly animation
    def fly(self):
        self._flying = True

        # if enemy is near the ground, then fly up and away from ninja-boy
        if (self._stun_time == 0):
            if (self.get_top() > self.CEILING + 10):
                self.set_position(None, self._rect.y - (self.get_top() - self.CEILING) / 10)
            else:
                self.set_position(None, self.CEILING)

            # move enemy laterally
            if (self.IS_BOUNDED):  
                if (self.IS_AGGRESSIVE):           
                    # determine what side of the screen ninja-boy is on
                    if (globals.player.get_x_center() > globals.SCREEN_WIDTH / 2):                    
                        # ninja-boy is on the right side of the screen, move to the left. 
                        if (self.get_left() > self.LEFT_BOUNDARY):  
                            if (self.IS_SMOOTH_MOVER): 
                                self.set_position(self._rect.x - ((self.get_left() - self.LEFT_BOUNDARY) / 20))  
                            else:
                                self.set_position(self._rect.x - globals.ground_scroll_speed - self.VELOCITY)    
                        else:
                            self.set_position(180)
                    elif (globals.player.get_x_center() <= globals.SCREEN_WIDTH / 2):     
                        # ninja-boy is on the left side of the screen, move to the right.
                        if (self.get_right() < globals.SCREEN_WIDTH - self.RIGHT_BOUNDARY):
                            if (self.IS_SMOOTH_MOVER):
                                self.set_position(self._rect.x + (globals.SCREEN_WIDTH - self.RIGHT_BOUNDARY - self.get_right()) / 20)
                            else:
                                self.set_position(self._rect.x + globals.ground_scroll_speed + self.VELOCITY)
                        else:
                            self.set_position(globals.SCREEN_WIDTH - 180 - self.get_width())

        # increment the main animation frame
        if (self._main_animation_frame < self.MAIN_ANIMATION_FRAMES):
            # set the proper image
            if (self._flip):
                self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/flying/flying_backwards_{self._main_animation_frame}.png')   
            else:
                self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/flying/flying_{self._main_animation_frame}.png')   
            self._main_animation_frame += 1  
        else:
            self._main_animation_frame = 0

    # check for obstacles between player and enemy, then attack if none.
    def create_attack(self):        
        self._player_attack_position = globals.player.get_position()
        self._enemy_attack_position = self.get_center_position()

        # draw a physical line between player and enemy, for debugging raycasting below.
        '''start_point = (globals.player._physics_body.position.x * globals.PPM, globals.player._physics_body.position.y * globals.PPM)
        end_point = (self._physics_body.position.x * globals.PPM, self._physics_body.position.y * globals.PPM)
        pygame.draw.line(globals.screen, (255, 0, 0), start_point, end_point)'''
        
        # check for obstacles between player and enemy
        rayCastCallback = RayCastCallback()
        globals.physics_world.RayCast(rayCastCallback, self._physics_body.position, globals.player._physics_body.position)

        # if no obstacles, then attack
        if not rayCastCallback.hit:      
            self._is_attacking = True
            self._top_offset = self.ATTACKING_OFFSETS[0]
            self._right_offset = self.ATTACKING_OFFSETS[1]
            self._bottom_offset = self.ATTACKING_OFFSETS[2]
            self._left_offset = self.ATTACKING_OFFSETS[3]
        else:
            self.reset_attack()

    # attack logic/animation
    def attack(self):        
        self._main_animation_frame = 0
        _divisor = 20

        if (self._attack_completion_timer > 100):
            self.reset_attack()
            self._attack_completion_timer = 0
            return

        self._attack_completion_timer += 1

        # begin attack animation
        if (self.IS_AGGRESSIVE):
            if (self._begin_attack_animation_frame < self.BEGIN_ATTACK_ANIMATION_FRAMES): 
                # set the proper image
                if (self._flip):
                    self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/attacking/begin_attack_backwards_{self._begin_attack_animation_frame}.png') 
                else:
                    self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/attacking/begin_attack_{self._begin_attack_animation_frame}.png')   
                self._begin_attack_animation_frame += 1
            else:
                if (self._attack_animation_frame < self.ATTACK_ANIMATION_FRAMES):
                    # set the proper image
                    if (self._flip):
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/attacking/attack_loop_backwards_{self._attack_animation_frame}.png')    
                    else:
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/attacking/attack_loop_{self._attack_animation_frame}.png')
                    self._attack_animation_frame += 1
                else:
                    self._attack_animation_frame = 0  
        else:
            # increment the main animation frame
            if (self._attack_animation_frame < self.ATTACK_ANIMATION_FRAMES):
                if (self.IS_FLYABLE):
                    if (self._flip):
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/flying/flying_backwards_{self._attack_animation_frame}.png')   
                    else:
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/flying/flying_{self._attack_animation_frame}.png')  
                elif (self.IS_WALKABLE):
                    # set the proper image
                    if (self._flip):
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/walking/walking_backwards_{self._attack_animation_frame}.png')   
                    else:
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/walking/walking_{self._attack_animation_frame}.png')    
                self._attack_animation_frame += 1  
            else:
                self._attack_animation_frame = 0

        # move towards player
        _distance_x = 0
        _distance_y = 0

        vertical_pass = False if self.IS_FLYABLE else True
        horizontal_pass = False

        # update player original position, factoring in ground scroll speed
        self._player_attack_position = (self._player_attack_position[0] - globals.ground_scroll_speed, self._player_attack_position[1])

        # check if you passed the original player coordinates
        if (self._enemy_attack_position[0] > self._player_attack_position[0]):
            _distance_x = self.get_x_center() - self._player_attack_position[0]
            _velocity = (_distance_x / _divisor) if (_distance_x / _divisor) < self.MAX_VELOCITY else self.MAX_VELOCITY
            self.set_position(self._rect.x - _velocity)
            if (self.get_left() < (self._player_attack_position[0] + (globals.player.get_width() / 2) - globals.player.RIGHT_OFFSET)):
                horizontal_pass = True              
        else:
            _distance_x = self._player_attack_position[0] - self.get_x_center()
            _velocity = (_distance_x / _divisor) if (_distance_x / _divisor) < self.MAX_VELOCITY else self.MAX_VELOCITY
            self.set_position(self._rect.x + _velocity)
            if (self.get_right() > (self._player_attack_position[0] - (globals.player.get_width() / 2) + globals.player.LEFT_OFFSET)):
                horizontal_pass = True
                
        if (self.IS_FLYABLE):
            if (self._enemy_attack_position[1] > self._player_attack_position[1]):
                _distance_y = self.get_y_center() - self._player_attack_position[1]
                _velocity = (_distance_y / _divisor) if (_distance_y / _divisor) < self.MAX_VELOCITY else self.MAX_VELOCITY
                self.set_position(None, self._rect.y - _distance_y / _divisor)
                if (self.get_top() < self._player_attack_position[1] + globals.player.get_height() / 2):
                    vertical_pass = True
            else:
                _distance_y = self._player_attack_position[1] - self.get_y_center()
                _velocity = (_distance_y / _divisor) if (_distance_y / _divisor) < self.MAX_VELOCITY else self.MAX_VELOCITY
                self.set_position(None, self._rect.y + _distance_y / _divisor)
                if (self.get_bottom() > self._player_attack_position[1] - globals.player.get_height() / 2 + globals.player.TOP_OFFSET):
                    vertical_pass = True
                
        # reset attack
        if ((vertical_pass and horizontal_pass) or globals.player.is_hurt):
            self.reset_attack()
    
    def checkForObstacleCollision(self, obstacles: List[Obstacle]):
        for obstacle in obstacles:            
            # collision with top/bottom - ensuring enemy is within the left/right boundaries of the obstacle
            if (((self.get_right() > obstacle.get_left()) and 
                (self.get_right() < obstacle.get_right())) or 
                ((self.get_left() < obstacle.get_right()) and 
                (self.get_left() > obstacle.get_left()))):
                # collision with top
                if (Sides.TOP in obstacle.COLLIDABLE_SIDES and 
                    (self.get_bottom() > obstacle.get_top()) and 
                    (self.get_bottom() < obstacle.get_top() + 10)): 
                    self.set_position(self.get_center_position()[0], obstacle.get_top() - self.get_height() - 5)
                    self._fallback_position = (0, 0)  
                    self.reset_attack()
                # collision with bottom
                elif ((Sides.BOTTOM in obstacle.COLLIDABLE_SIDES and self.get_top() < obstacle.get_bottom()) and 
                    (self.get_top() > obstacle.get_bottom() - 10)): 
                    self.set_position(self.get_center_position()[0], obstacle.get_bottom() + 5)
                    self._fallback_position = (0, 0)   
                    self.reset_attack()
                # collision with left/right - ensuring enemy is within the top/bottom boundaries of the obstacle
                elif (((self.get_bottom() > obstacle.get_top()) and 
                    (self.get_bottom() < obstacle.get_bottom())) or 
                    ((self.get_top() < obstacle.get_bottom()) and 
                    (self.get_top() > obstacle.get_top()))):
                    # left collision  
                    if (Sides.LEFT in obstacle.COLLIDABLE_SIDES and 
                        self.get_right() > obstacle.get_left() and 
                        self.get_right() < obstacle.get_x_center()): 
                        self.set_position(self.get_x() - 10)
                        self._fallback_position = (0, 0)   
                        self.reset_attack()
                    # right collision
                    elif (Sides.RIGHT in obstacle.COLLIDABLE_SIDES and 
                        self.get_left() < obstacle.get_right() and 
                        self.get_left() > obstacle.get_x_center()):    
                        self.set_position(self.get_x() + 10)
                        self._fallback_position = (0, 0)
                        self.reset_attack()

    def checkDangerZoneCollision(self):      
        if (self._stun_time == 0):  
            if self.mask.overlap(globals.player.mask, (globals.player._rect.x - self.get_left(), globals.player._rect.y - self.get_top())):     
                if (DangerZone.BOTTOM_LEFT in self.DANGER_ZONES or 
                    DangerZone.BOTTOM_RIGHT in self.DANGER_ZONES):  
                    # now check if enemies dangerous side is contacting player
                    if ((globals.player.get_top() > self.get_y_center() and globals.player.get_top() < self.get_bottom()) or 
                        (self.get_y_center() > globals.player.get_top() and self.get_bottom() < globals.player.get_bottom()) or 
                        (globals.player.get_bottom() > self.get_y_center() and globals.player.get_bottom() < self.get_bottom())):
                        if (self.get_x_center() > globals.player.get_x_center()):     
                            if (DangerZone.BOTTOM_LEFT in self.DANGER_ZONES):
                                globals.player.hit(self.DAMAGE, Sides.RIGHT)  
                                if (not self.IS_FLYABLE):
                                    self.set_fallback(Sides.LEFT)
                                    self.reset_attack()
                        else:
                            if (DangerZone.BOTTOM_RIGHT in self.DANGER_ZONES): 
                                globals.player.hit(self.DAMAGE, Sides.LEFT)
                                if (not self.IS_FLYABLE):
                                    self.set_fallback(Sides.RIGHT)
                                    self.reset_attack()

    def checkForHit(self):
        if self.mask.overlap(globals.player.mask, (globals.player._rect.x - self.get_left(), globals.player._rect.y - self.get_top())):       
            if (globals.player.is_attacking):
                if (self.get_x_center() > globals.player.get_x_center()):  
                    if globals.player.facing_direction == Direction.RIGHT:
                        self.set_fallback(Sides.LEFT)
                        self.reset_attack()
                        self.hit()
                else:
                    if globals.player.facing_direction == Direction.LEFT:
                        self.set_fallback(Sides.RIGHT)
                        self.reset_attack()
                        self.hit()

    def set_fallback(self, _hit_side: Sides):
        _distance = 450 if self.IS_FLYABLE else 100
        if _hit_side == Sides.RIGHT:
            self._fallback_direction = Direction.LEFT                
            self._fallback_position = ((self.get_x() - _distance), self._fallback_position[1])  
        elif _hit_side == Sides.LEFT: 
            self._fallback_direction = Direction.RIGHT
            self._fallback_position = ((self.get_x() + _distance), self._fallback_position[1])

    def thinking(self): 
        if (self._thinking_frame < self._thinking_frames):
            self._thinking_frame += 1
            return True 
        self.create_attack()  
        return False     

    def draw(self, obstacles: List[Obstacle]):
        Debugger.print(self._debugger_message)
        self._debugger_message = ''  
            
        # now what is the distance between enemy and player?
        self._distance_x = self.get_x_center() - globals.player.get_x_center()
        self._distance_y = self.get_y_center() - globals.player.get_y_center()

        self._flip = (self._distance_x > 0)
        globals.SCREEN.blit(self._surf, self._rect)

        # if paused, don't move
        if globals.game_paused:
            return        
        
        if not self._is_attacking and not self._is_hurt:
            if self.IS_FLYABLE: 
                self.fly()
            if self.IS_WALKABLE:
                self.move_with_ground()
        
        # if game is moving, unless hurt, start thinking.   
        # as a side note, this is an area, where we might be able to 
        # define machine learning algorithms to make the enemy smarter?
        if globals.game_moving and not globals.player.is_dying:            
            self._fallback_position = (self._fallback_position[0] - globals.ground_scroll_speed, self._fallback_position[1]) if self._fallback_position != (0, 0) else (0, 0)

            # this must happen before hurt animation and fallback, to adjust for obstacle collision.
            self.checkForObstacleCollision(obstacles) 

            # hurt animation
            if (self._is_hurt):                
                if (self._hurt_animation_frame < self.HURT_ANIMATION_FRAMES):
                    if (self._flip):
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/hurt/hurt_backwards_{self._hurt_animation_frame}.png')   
                    else:
                        self._surf = pygame.image.load(f'{self.ASSET_PATH}/animations/hurt/hurt_{self._hurt_animation_frame}.png')   
                    self._hurt_animation_frame += 1
                else:
                    if (self._hurt_pause_frame < self._hurt_pause_frames):
                        self._hurt_pause_frame += 1 
                        if self.IS_WALKABLE: self.move_with_ground()
                    else:
                        self._hurt_animation_frame = 0
                        self._is_hurt = False
                        self._hurt_pause_frame = 0

            # if fallback position is set, then move to it, otherwise, continue
            if (self._fallback_position != (0, 0)):       
                if (self._fallback_direction == Direction.LEFT):
                    _distance = (self.get_x() - self._fallback_position[0]) / 10 
                    if (_distance > 2):
                        self.set_position(self._rect.x - _distance)
                    else:
                        self._fallback_position = (0, 0)
                        self._fallback_direction = Direction.NONE
                elif (self._fallback_direction == Direction.RIGHT):
                    _distance = (self._fallback_position[0] - self.get_x()) / 10  
                    if (_distance > 2):
                        self.set_position(self._rect.x + _distance)
                    else:
                        self._fallback_position = (0, 0)
                        self._fallback_direction = Direction.NONE  
                return       
            
            # check if enemy is dead
            self.is_dead = True if (self._health <= 0) else False  
            if self.is_dead:
                globals.player.score_component.add_points(self.POINTS_VALUE)
                return
            
            # reset the mask            
            self.mask = pygame.mask.from_surface(self._surf)
            globals.SCREEN.blit(self._surf, self._rect)
  
            self.checkForHit()

            if (self._stun_time > 0):
                self._stun_time -= 1
                self._halo.set_position(self.get_x() - 5, self.get_y() - 10)
                self._halo.draw()
                return
            
            if (not self._is_hurt):  
                self.checkDangerZoneCollision()         

                # if enemy is a thinker, then think
                if self.IS_THINKER:
                    if self.thinking():
                        return                

                    # attack player
                    if self._is_attacking:
                        self.attack()
                        return


