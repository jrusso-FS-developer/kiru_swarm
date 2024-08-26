#system imports
from decimal import Decimal
from typing import List

# dependency imports
import pygame
from Box2D import (b2PolygonShape, b2FixtureDef, b2BodyDef)

# global vars
from classes.config.coin_config import CoinBlock
from classes.config.map_config import MapWeaponBlock
from classes.config.power_up_config import EFFECT_TYPES
from classes.heart import Heart
from classes.power_up import PowerUp
import globals

#enums
from classes.config.enums.sides import Sides
from classes.config.enums.directions import Direction

#class objects
from classes.debugger import Debugger
from classes.obstacle import Obstacle
from classes.coin_hud import CoinHUD
from classes.config.weapon_config import WeaponConfig
from classes.health_bar_hud import HealthBarHUD
from classes.inventory_hud import InventoryHUD
from classes.life_hud import LifeHUD
from classes.score import Score
from classes.weapon import Weapon

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() 
        self.set()

    # CONSTANTS
    ACCELERATION: Decimal = 0.40
    GRAVITY: int = 1
    GROUND: int = globals.GROUND - 5 
    IMAGE_PATH = 'sprites/characters/player/ninja-boy'
    IMMUNITY_SUFFIX: str = '_immunity'
    MAX_JUMP_VELOCITY: int = 15
    MAX_VELOCITY: int = 10
    MIN_JUMP_VELOCITY: Decimal = .05
    MIN_VELOCITY: int = 0
    SOUND_PATH: str = 'sounds/character/player/ninja-boy'
    WALK_VELOCITY: int = 3

    #offset vars
    BOTTOM_OFFSET: int = 5
    LEFT_OFFSET: int = 65
    RIGHT_OFFSET: int = 65
    TOP_OFFSET: int = 25

    # game vars
    active_weapon: Weapon = None
    facing_direction: Direction = Direction.NONE
    is_attacking: bool = False
    is_dead: bool = False
    is_dying: bool = False # lets the level know to play dying music, and pause for animation
    is_hurt: bool = False
    life_count: int = globals.GAME_LIFE_COUNT
    mask: pygame.mask.Mask = None
    poly_fixture: b2FixtureDef = None
    score_component: Score

    _active_suffix: str = ''
    _attack_direction: Direction = Direction.NONE
    _attack_frame_count: int = 11
    _attack_index: int = 0
    _coin_component: CoinHUD = None
    _collision_object: Obstacle = None
    _collision_side: Sides = Sides.NONE
    _current_position_x: float = 0
    _death_animation_frame: int = 0
    _death_animation_frame_count: int = 11
    _death_pause_frame_count: int = 180
    _death_pause_frame: int = 0
    _debugger_message: str = ''
    _forced_slow_to_stop = False
    _game_over_music:pygame.mixer.Sound = None
    _health_bar: HealthBarHUD = None
    _health: float = 100
    _hurt_animation_frame: int = 0
    _hurt_animation_frame_count: int = 11
    # BEGIN immunity frames, set by collecting PowerUp.EFFECT_TYPE == EFFECT_TYPES.IMMUNITY
    _immunity_frame: int = 0
    _immunity_frame_count: int = 0
    # END PowerUp.EFFECT_TYPE == EFFECT_TYPES.IMMUNITY
    _immunity_timer: int = 0 # this is for momentary immunity, granted when player is hit.
    _inventory_component: InventoryHUD = None 
    _is_crouching: bool = False
    _is_jumping: bool = False
    _is_running: bool = False
    _jumping_frame_count: int = 5
    _jumping_index: int = 0
    _jump_pause_frames: int = 0
    _jump_sound: pygame.mixer.Sound = None
    _jump_start_frame_count: int = 5
    _jump_start_index: int = 0
    _jump_velocity: Decimal = MAX_JUMP_VELOCITY / 2
    _key_press_timer: int = 0
    _life: LifeHUD = None
    _lose_life_music: pygame.mixer.Sound = None
    _moving_direction: Direction = Direction.NONE
    _fallback_position: tuple[Decimal, Decimal] = (0, 0)
    _obstacles: List[Obstacle] = []
    _ooof_sound: pygame.mixer.Sound = None
    _player_ground: Decimal = Decimal(GROUND + BOTTOM_OFFSET)
    _playing_jump: bool = False
    _playing_woosh: bool = False
    _physics_body: object = None
    _physics_body_def: b2BodyDef = None
    _poly_shape: b2PolygonShape = None
    _pre_attack_position: tuple[Decimal, Decimal] = (0, 0)
    _running_frame_count: int = 10
    _running_index: int = 0
    _running_sound: pygame.mixer.Sound = None
    _velocity: Decimal = Decimal(MIN_VELOCITY)
    _walking_frame_count: int = 23
    _walking_index: int = 0
    _weapons: List[Weapon] = []
    _weapon_index: int = -1

    def set(self):
        # initial states
        self.is_attacking = False
        self.is_dead = False
        self.is_hurt = False
        self.is_dying = False
        
        self._active_suffix = ''
        self._attack_direction = Direction.NONE
        self._attack_frame_count = 11
        self._attack_index = 0
        self._coin_component = CoinHUD()
        self._death_animation_frame = 0
        self._death_pause_frame = 0
        self._health = 100
        self._health_bar = HealthBarHUD(self._health)
        self._hurt_animation_frame_count = 11
        self._immunity_frame = 0
        self._immunity_frame_count = 0
        self._immunity_timer = 0
        self._is_running = False
        self._is_running_playing = False
        self._is_crouching = False
        self._is_jumping = False
        self._jump_start_frame_count = 5
        self._jump_start_index = 0
        self._jumping_frame_count = 5
        self._jumping_index = 0
        self._life = LifeHUD()
        self._life.set_folder(self.IMAGE_PATH)
        self._moving_direction = Direction.NONE
        self._player_ground = Decimal(self.GROUND + self.BOTTOM_OFFSET)
        self._pre_attack_position = (0, 0) 
        self._running_frame_count = 11
        self._running_index = 0  
        self.score_component = Score(0)
        self._velocity = self.MIN_VELOCITY    
        self._walking_index = 0
        self._walking_frame_count = 22

        # weapons
        self._weapons: List[Weapon] = []
        self._weapons.append(Weapon(MapWeaponBlock(WeaponConfig.SAMURAI, (0, 0)), True, True))
        self._weapon_index = 0
        self.active_weapon = self._weapons[0]
        self._inventory_component = InventoryHUD(self._weapons)

        # initial image/rect
        self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still.png')
        self.mask = pygame.mask.from_surface(self.surf)
        self._rect = self.surf.get_rect()
        self._rect.center = globals.screen_center   

        # create physics poly/fixture
        self._poly_shape = b2PolygonShape(box=(self.get_width() / 2, self.get_height() / 2))
        self.poly_fixture = b2FixtureDef(shape=self._poly_shape, density=1, friction=0.3)
        self._physics_body_def = b2BodyDef(position=(self.get_x_center(), self.get_y_center()))
        self._physics_body = globals.physics_world.CreateBody(self._physics_body_def)
        self._physics_body.CreateFixture(self.poly_fixture)
        self._physics_body.userData = 'player'

        # now you can set the player on the ground
        self.set_position(None, self._player_ground - self.get_height() - self.TOP_OFFSET)  

        # sounds 
        self._jump_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/jump.mp3')
        self._ooof_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/ooof.mp3')
        self._running_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/running.wav')    
        self._jump_sound.set_volume(.80)
        self._ooof_sound.set_volume(.50)

        # music
        self._lose_life_music = pygame.mixer.Sound(f'{globals.MUSIC_PATH}/bum-bum-bum-bum-bum.mp3')
        self._game_over_music = pygame.mixer.Sound(f'{globals.MUSIC_PATH}/game-over.mp3')
        self._lose_life_music.set_volume(.30)
        self._lose_life_music.set_volume(.30)

    # GETTERS: the enemy will find you... bwahahaha
    def get_top(self):
        return self._rect.y + self.TOP_OFFSET
    
    def get_bottom(self):
        return self._rect.bottom - self.BOTTOM_OFFSET
    
    def get_x(self):
        return self._rect.x
    
    def get_y(self):
        return self._rect.y
    
    def get_x_center(self):
        return self._rect.x + self._rect.width / 2
    
    def get_y_center(self):
        return self._rect.y + self._rect.height / 2
    
    def get_width(self):
        return self._rect.width - self.RIGHT_OFFSET - self.LEFT_OFFSET
    
    def get_height(self):
        return self._rect.height - self.TOP_OFFSET - self.BOTTOM_OFFSET
    
    def get_left(self):
        return self._rect.left + self.LEFT_OFFSET
    
    def get_right(self):    
        return self._rect.right - self.RIGHT_OFFSET
    
    def get_position(self):
        return (self.get_x(), self.get_y())
    
    def get_fixture(self):
        return self.poly_fixture
    
    def collect_coin(self, coin: CoinBlock):
        self._coin_component.add_coins(coin.VALUE)
    
    def collect_heart(self, heart: Heart):
        self._health += heart.VALUE if self._health + heart.VALUE < 100 else 100 - self._health

    def collect_weapon(self, weapon: Weapon):
        weapon.selected = True
        for item in self._inventory_component.get_inventory():
            if isinstance(item, Weapon):
                item.selected = False
        self._inventory_component.add_item(weapon)

    def collect_power_up(self, power_up: PowerUp):
        if power_up.EFFECT_TYPE == EFFECT_TYPES.IMMUNITY:
            self._immunity_frame_count = power_up.EFFECT_FRAMES
        else:
            pass
    
    def set_position(self, x = None, y = None):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y
        self._physics_body.position = (self.get_x_center() / globals.PPM, self.get_y_center() / globals.PPM)
    
    def hit(self, damage, side: Sides = Sides.NONE):
        # if immunity timer is active, don't take damage
        if (self._immunity_timer > 0):
            return
        
        # if player has self._immunity_frame_count > 0, due to collecting a power_up
        # this gets reset to 0 once self._immunity_frame == self._immunity_frame_count
        if (self._immunity_frame_count):
            return
        
        # set hurt animation initial state
        self._hurt_animation_frame = 0
        self.facing_direction = Direction.RIGHT if side == Sides.RIGHT or side == Sides.NONE else Direction.LEFT
        self.is_hurt = True
        self.set_fallback()
        self._ooof_sound.play()

        # decrease health
        self._health -= damage if not globals.DEBUG_MODE else 0
        
        # set health and immunity timer
        self._health_bar.set_health(self._health)
        self._immunity_timer = 30

        # check for death
        if self._health <= 0:
            self.lose_life()

    def set_fallback(self):
        if self.facing_direction == Direction.RIGHT:
            self._fallback_position = ((self.get_x() - 100), self._fallback_position[1])  
        else: 
            self._fallback_position = ((self.get_x() + 100), self._fallback_position[1])

    def _stop_sounds(self):
        self._running_sound.stop()
        self._is_running_playing = False
        self._running_sound.set_volume(0)
    
    def lose_life(self):
        if not globals.DEBUG_MODE:
            # decrease life count
            self._life.decrease_count()

            # stop any currently playing sounds
            self._stop_sounds()
            self._death_animation_frame = 0
            self.is_dying = True
            
            # play the lose life music
            self._lose_life_music.play()

            if self.life_count <= 0:
                self.is_dead = True
            

    def die(self):
        if (self._is_jumping):
            self.check_collision()
            self.jump()

        if (self._death_animation_frame < self._death_animation_frame_count):
            if (self.facing_direction == Direction.LEFT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/death/death_backwards_{self._death_animation_frame}.png')
            else:
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/death/death_{self._death_animation_frame}.png')
            self._death_animation_frame += 1
        else:
            if (self._death_pause_frame < self._death_pause_frame_count):
                self._death_pause_frame += 1
            else:                
                if (not self._is_jumping):
                    self._death_pause_frame = 0
                    self._death_animation_frame = 0                      
                    self.is_dying = False

                    # restart the level
                    if (self.is_dead):
                        # pause the game, and set game over.  
                        # the main.py game loop will handle the game over screen
                        globals.game_paused = True
                        globals.game_over = True  
                    else:
                        # reset player position, health and velocity
                        self.is_hurt = False
                        self._health = 100
                        self._rect.center = globals.screen_center
                        self._player_ground = Decimal(self.GROUND + self.BOTTOM_OFFSET)
                        self.set_position(None, self._player_ground - self.get_height() - self.TOP_OFFSET) 
                        self._velocity = self.MIN_VELOCITY

                        # pause the game until the level reloads and sets pause to globals.game_paused = False
                        globals.game_paused = True  
                        globals.restart_level = True

    def check_collision(self):
        self._collision_object = None
        _collision_top_offset = self.TOP_OFFSET if not self._is_crouching else self.TOP_OFFSET + 25

        # bounce off the top of the screen
        if (self._rect.y + _collision_top_offset <= 15):
            self._jump_velocity -= self.MAX_JUMP_VELOCITY / 2

        for obstacle in self._obstacles:
            obstacle.collision_side = None
            # collision detected
            if (self._rect.right - self.RIGHT_OFFSET > obstacle._rect.left + obstacle.left_offset 
                and self._rect.left + self.LEFT_OFFSET < obstacle._rect.right - obstacle.right_offset):
                # land if you can
                if ((Sides.TOP in obstacle.COLLIDABLE_SIDES) and 
                    (self._rect.y + self._rect.height > obstacle._rect.top + obstacle.top_offset - 5
                    and self._rect.y + self._rect.height < obstacle._rect.top + obstacle.top_offset + 25)):
                    obstacle.collision_side = Sides.TOP
                    if (self._is_jumping and not obstacle.landed_on):
                        if (obstacle.is_landable):
                            self._jump_pause_frames = 15
                            self._is_jumping = False
                            self._jump_velocity = self.MAX_JUMP_VELOCITY / 2
                            self._jump_start_index = 0
                            self._jumping_index = 0
                            self._playing_jump = False
                            obstacle.landed_on = True
                            _new_y = obstacle.get_top() - self.get_height() - _collision_top_offset - self.BOTTOM_OFFSET
                            _new_y += 10 if self.is_dying else 0
                            self.set_position(None, _new_y)
                        else:
                            # TODO: Logic for if you land on an unlandable object? bounce or just fall in?
                            pass
                elif ((Sides.RIGHT in obstacle.COLLIDABLE_SIDES or Sides.LEFT in obstacle.COLLIDABLE_SIDES)
                    and self._rect.y + self._rect.height >= obstacle._rect.top + obstacle.top_offset + 25):   
                    obstacle.landed_on = False  

                    #if not under the obstacle, then detect side collision
                    if (self._rect.y + _collision_top_offset <= obstacle._rect.bottom):              
                        # block left
                        if (Sides.LEFT in obstacle.COLLIDABLE_SIDES and (self._rect.right - self.RIGHT_OFFSET >= obstacle._rect.left + obstacle.left_offset 
                            and self._rect.right - self.RIGHT_OFFSET < obstacle._rect.right - obstacle.right_offset)):
                            obstacle.collision_side = Sides.LEFT
                            self.set_position(obstacle._rect.left + obstacle.left_offset - self.get_width() - self.RIGHT_OFFSET)
                            self._fallback_position = (0, 0)
                        # block right
                        elif (Sides.RIGHT in obstacle.COLLIDABLE_SIDES and ((self._rect.left + self.LEFT_OFFSET <= obstacle._rect.right - obstacle.right_offset)
                              and (self._rect.left + self.LEFT_OFFSET > obstacle._rect.left + obstacle.left_offset))):
                            obstacle.collision_side = Sides.RIGHT
                            self.set_position(obstacle._rect.right - obstacle.right_offset - self.LEFT_OFFSET)
                            self._fallback_position = (0, 0)
                    else: 
                        # bounce off the bottom
                        if ((Sides.BOTTOM in obstacle.COLLIDABLE_SIDES) 
                        and (self._rect.y + _collision_top_offset <= obstacle._rect.bottom + 20)):
                            obstacle.landed_on = False  
                            self._jump_velocity -= self.MAX_JUMP_VELOCITY / 2
            else: # no collision
                obstacle.landed_on = False            
            
            if (obstacle.collision_side != None):
                self._collision_object = obstacle

                # check for deadly contact
                if (self._collision_object.actively_deadly):
                    if (self._collision_object.collision_side in self._collision_object.DEADLY_SIDES):
                        self.lose_life()
                        break
        
        if (not self._is_jumping and self._collision_object == None and not self.is_attacking):
            if (self._rect.y + self._rect.height < self._player_ground):
                self._is_jumping = True   

    def draw(self, obstacles: List[Obstacle], ground_scroll):
        self._health_bar.set_health(self._health)
        self._life.draw()
        self.score_component.draw()
        self._coin_component.draw()
        self._inventory_component.draw()
        self._is_running = False
        self._obstacles = obstacles
        direction_shift = False
        Debugger.print(self._debugger_message)
        
        if (self.is_dying):
            self.die()
            return 
        
        if (self.is_dead):
            # TODO: game over logic
            return

        if (self._immunity_timer > 0):
            self._immunity_timer -= 1

        if (self._immunity_frame < self._immunity_frame_count):
            self._active_suffix = self.IMMUNITY_SUFFIX
            self._immunity_frame += 1
        else:
            self._active_suffix = ''
            self._immunity_frame = 0
            self._immunity_frame_count = 0

        if globals.pressed_keys[pygame.K_i]:
            if (self._key_press_timer == 0):
                self._key_press_timer = 6
                self._inventory_component.toggle_menu()
            else:
                self._key_press_timer -= 1

        for index, item in enumerate(self._inventory_component.get_inventory()):
            if isinstance(item, Weapon):
                if item.selected:
                    self._weapon_index = index
                    self.active_weapon = item
                    break

        if (not globals.game_paused):
            if (globals.game_moving):  
                # check for collisions with obstacles 
                # enemy collisions are handled by the Enemy objects
                self.check_collision()

                if (self.is_hurt):
                    if (self._hurt_animation_frame < self._hurt_animation_frame_count):
                        if (self.facing_direction == Direction.LEFT):
                            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/hurt/hurt_backwards_{self._hurt_animation_frame}.png')
                        else:
                            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/hurt/hurt_{self._hurt_animation_frame}.png')
                        self._hurt_animation_frame += 1

                        if (self._fallback_position != (0, 0) and not self._is_jumping):
                            if (self._fallback_position[0] < self.get_x()):
                                self.set_position(self.get_x() - 10)
                            elif (self._fallback_position[0] > self.get_x()): 
                                self.set_position(self.get_x() + 10)
                    else:
                        self.is_hurt = False
                        self._hurt_animation_frame = 0
                        self._fallback_position = (0, 0)

                    if (self._is_jumping):
                        self.jump() 
                    return   
                
                # reduce jump pause frames by one frame until 0
                if (self._jump_pause_frames > 0):
                    self._jump_pause_frames -= 1
                
                # begin walking right, if they've reached the left EDGE_THRESHOLD
                if self.get_left() > globals.EDGE_THRESHOLD: 
                    self.set_position(self._rect.x - ground_scroll)
                    self._is_walking = False
                else:
                    if (not self._is_jumping and not self._is_running and not self.is_attacking):
                        self._is_walking = True
                        self._moving_direction = Direction.RIGHT if not any(globals.pressed_keys) and self._velocity == 0 else self._moving_direction
                        self.facing_direction = self._moving_direction

                # check for user's input if not attacking/jumping
                if (self.is_attacking):
                    if (self._is_jumping): self.jump()
                    self.attack()
                else:
                    # speed up the game scrolling, if player is beyond the right EDGE_THRESHOLD
                    _right_threshold = (globals.SCREEN_WIDTH - (globals.SCREEN_WIDTH // 2.75))
                    if self.get_right() > _right_threshold:
                        acceleration = (self.get_right() - _right_threshold) / 20
                        globals.bg_scroll_speed = globals.MIN_BG_SCROLL_SPEED + acceleration / 5
                        globals.ground_scroll_speed = globals.MIN_GROUND_SCROLL_SPEED + acceleration 
                    else:
                        globals.bg_scroll_speed = globals.MIN_BG_SCROLL_SPEED
                        globals.ground_scroll_speed = globals.MIN_GROUND_SCROLL_SPEED   

                    if (self._is_jumping):
                        self.jump()  
                    else:
                        if (not any(globals.pressed_keys) or 
                            (globals.pressed_keys[pygame.K_UP]) or 
                            (globals.pressed_keys[pygame.K_DOWN])):
                            # slow down gradually
                            self.slow_to_stop()
                        else:
                            if (self._is_crouching):
                                self._velocity = self.WALK_VELOCITY
                            else:
                                if self._velocity < self.MAX_VELOCITY:
                                    self._velocity += self.ACCELERATION 

                        if globals.pressed_keys[pygame.K_DOWN]:
                            self._is_crouching = True
                        if globals.pressed_keys[pygame.K_UP]:
                            self.facing_direction = Direction.UP
                            self._is_crouching = False
                            if globals.pressed_keys[pygame.K_LEFT]:
                                self._moving_direction = Direction.LEFT
                                self.facing_direction = Direction.UP_LEFT
                            elif globals.pressed_keys[pygame.K_RIGHT]:
                                self._moving_direction = Direction.RIGHT
                                self.facing_direction = Direction.UP_RIGHT
                        elif globals.pressed_keys[pygame.K_LEFT]:
                            self.set_position(self._rect.x - self._velocity)
                            self._is_running = True if not self._is_crouching else False
                            if (self._moving_direction != Direction.LEFT):
                                direction_shift = True
                                self._moving_direction = Direction.LEFT
                                self.facing_direction = Direction.LEFT
                                self._velocity = self.MIN_VELOCITY
                        elif globals.pressed_keys[pygame.K_RIGHT]:
                            self.set_position(self._rect.x + self._velocity)
                            self._is_running = True if not self._is_crouching else False
                            if (self._moving_direction != Direction.RIGHT):
                                direction_shift = True
                                self._moving_direction = Direction.RIGHT
                                self.facing_direction = Direction.RIGHT
                                self._velocity = self.MIN_VELOCITY
                                
                        if globals.pressed_keys[pygame.K_SPACE]:
                            self._running_sound.stop()                            
                            self._is_crouching = False
                            if (not self._is_jumping):
                                if (self._jump_pause_frames == 0):
                                    self.set_position(None, self._rect.y - self._jump_velocity)
                                    self._jump_velocity = self.MAX_JUMP_VELOCITY   
                                    self._is_jumping = True 
                                    if self._collision_object != None: self._collision_object.landed_on = False

                        # walk or run?
                        if (self._moving_direction == Direction.LEFT or self._moving_direction == Direction.RIGHT):
                            if (self._velocity > 3.5):
                                self._walking_index = 0
                                self.running()
                            else:
                                self._running_index = 0    
                                self.walking()                                
                        else:
                            self._running_index = 0            
                            self.walking() 

                    # attack             
                    if globals.pressed_keys[pygame.K_f]:
                        self.is_attacking = True

                        # set the attack direction
                        if (self._attack_direction == Direction.NONE):
                            if globals.pressed_keys[pygame.K_LEFT]:
                                if (globals.pressed_keys[pygame.K_UP]):
                                    self._attack_direction = Direction.UP_LEFT
                                elif (globals.pressed_keys[pygame.K_DOWN]):
                                    self._attack_direction = Direction.DOWN_LEFT
                                else:
                                    self._attack_direction = Direction.LEFT
                            elif globals.pressed_keys[pygame.K_RIGHT]:
                                if (globals.pressed_keys[pygame.K_UP]):
                                    self._attack_direction = Direction.UP_RIGHT
                                elif (globals.pressed_keys[pygame.K_DOWN]):
                                    self._attack_direction = Direction.DOWN_RIGHT
                                else:
                                    self._attack_direction = Direction.RIGHT
                            elif globals.pressed_keys[pygame.K_UP]:
                                self._attack_direction = Direction.UP
                            else:
                                self._attack_direction = self._moving_direction

                    running_volume = self._running_sound.get_volume()

                    if not self._is_running:                        
                        if (running_volume > .05 and not direction_shift):
                            self._running_sound.set_volume(running_volume - running_volume / 12)
                        else:
                            self._running_sound.stop()
                            self._is_running_playing = False
                            self._running_sound.set_volume(0)
                    else:
                        if (not self._is_running_playing or direction_shift):                            
                            self._running_sound.stop()
                            self._running_sound.play(-1)
                            self._running_sound.set_volume(0)
                            self._is_running_playing = True
                        else:
                            running_volume  = .50 if running_volume ==  0 else running_volume
                            running_volume = running_volume + 1 - running_volume / 2 if running_volume < .95 else 1
                            self._running_sound.set_volume(running_volume)

                # keep player in bounds
                self.stay_in_bounds()
            else:
                self._walking_index = 0
                self._running_index = 0
                if(self._moving_direction == Direction.LEFT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still_backwards{self._active_suffix}.png')
                else:
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still{self._active_suffix}.png')

        # create the mask
        self.mask = pygame.mask.from_surface(self.surf)

    def stay_in_bounds(self):
        if self.get_left() < 0:            
            self.set_position(0 - self.LEFT_OFFSET)
            if self._collision_object != None and self._collision_object.collision_side == Sides.LEFT:
                self.lose_life()
        if self._rect.right - self.RIGHT_OFFSET> globals.SCREEN_WIDTH:
            self.set_position(globals.SCREEN_WIDTH + self.RIGHT_OFFSET - self.get_width())
        if self._rect.top + self.TOP_OFFSET <= 0:
            self._rect.top = 0
        if self._rect.bottom >= self._player_ground - 5:
            _new_y: Decimal = self._player_ground - self.get_height() - self.TOP_OFFSET
            
            # adjust for weapon crouch attack bottom offset
            if (self.is_attacking):
                _new_y += self.active_weapon.CROUCH_ATTACK_BOTTOM_OFFSET if self._is_crouching else self.active_weapon.ATTACK_BOTTOM_OFFSET
                
            self.set_position(None, _new_y)
    
    def attack(self):
        # play attack sound
        if (not self._playing_woosh):            
            self.active_weapon.play_woosh()
            self._playing_woosh = True

        _attack_prefix = 'crouch_' if self._is_crouching else ''    

        if (not self._is_jumping):
            if (self._pre_attack_position == (0, 0)):
                self._pre_attack_position = self.get_position()
            _new_y = self._pre_attack_position[1]
            _new_y += self.active_weapon.CROUCH_ATTACK_BOTTOM_OFFSET if self._is_crouching else self.active_weapon.ATTACK_BOTTOM_OFFSET
            self.set_position(None, _new_y)


        # attack animation
        if (self._attack_direction == Direction.LEFT):
            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/horizontal/{_attack_prefix}attack_backwards_{self._attack_index}{self._active_suffix}.png')
        elif (self._attack_direction == Direction.RIGHT or self._attack_direction == Direction.NONE):
            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/horizontal/{_attack_prefix}attack_{self._attack_index}{self._active_suffix}.png')
        elif (self._attack_direction == Direction.UP):
            _folder = 'horizontal'
            if(self._moving_direction == Direction.LEFT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/{_folder}/attack_backwards_{self._attack_index}{self._active_suffix}.png')
            elif(self._moving_direction == Direction.RIGHT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/{_folder}/attack_{self._attack_index}{self._active_suffix}.png')
            else:
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/{_folder}/attack_{self._attack_index}{self._active_suffix}.png')
        elif (self._attack_direction == Direction.UP_LEFT):
            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/{_folder}/attack_backwards_{self._attack_index}{self._active_suffix}.png')
        elif (self._attack_direction == Direction.UP_RIGHT):
            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/attacking/{self.active_weapon.NAME}/{_folder}/attack_{self._attack_index}{self._active_suffix}.png')
        self._attack_index = self._attack_index + 1 if self._attack_index < self._attack_frame_count else 0 

        # attack is over, reset
        if (self._attack_index == 0):
            self.is_attacking = False 
            self._playing_woosh = False    
            self._attack_direction = Direction.NONE 
            if (not self._is_jumping):
                self.set_position(None, self._pre_attack_position[1])
            self._pre_attack_position = (0, 0) 

    def jump(self):
        if (self._jump_pause_frames > 0):
            return
        
        if (not self._forced_slow_to_stop and (globals.pressed_keys[pygame.K_LEFT] or globals.pressed_keys[pygame.K_RIGHT])):            
            self._velocity = (self._velocity + (self.ACCELERATION / 2)) if self._velocity < self.MAX_VELOCITY / 1.5 else self.MAX_VELOCITY / 1.5

            if (globals.pressed_keys[pygame.K_LEFT]):
                self._moving_direction = Direction.LEFT
                self.facing_direction = self._moving_direction
                self.set_position(self._rect.x - self._velocity)
            if (globals.pressed_keys[pygame.K_RIGHT]):
                self._moving_direction = Direction.RIGHT
                self.facing_direction = self._moving_direction
                self.set_position(self._rect.x + self._velocity)
        else:
            self._forced_slow_to_stop = True if self._velocity >= self.MAX_VELOCITY / 2 else False
            # slow down gradually
            self.slow_to_stop()

        if (not self._playing_jump):
            self._jump_sound.play()
            self._playing_jump = True

        # jump logic
        self.set_position(None, self._rect.y - self._jump_velocity)
        self._jump_velocity -= self.GRAVITY / 3 if globals.pressed_keys[pygame.K_SPACE] else self.GRAVITY 
        self._player_ground = Decimal(self.GROUND + self.BOTTOM_OFFSET) if self._collision_object != None and self._collision_side != Sides.TOP else Decimal(self._player_ground)

        if self._rect.bottom >= self._player_ground:
            self._jump_pause_frames = 8
            _new_y = self._player_ground - self.get_height() - self.TOP_OFFSET
            _new_y += 10 if self.is_dying else 0
            if (self.is_attacking):
                _new_y += self.active_weapon.CROUCH_ATTACK_BOTTOM_OFFSET if self._is_crouching else self.active_weapon.ATTACK_BOTTOM_OFFSET 
            self.set_position(None, _new_y)
            self._is_jumping = False
            self._jump_velocity = self.MAX_JUMP_VELOCITY / 2
            self._jump_start_index = 0
            self._jumping_index = 0
            self._playing_jump = False
            self._velocity = self.MIN_VELOCITY

        if (not self.is_hurt):
            # jump animation
            if (self._jump_start_index < self._jump_start_frame_count):
                if (self._moving_direction == Direction.LEFT or self._moving_direction == Direction.UP_LEFT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/jumping/jumping_start_backwards_{self._jump_start_index}{self._active_suffix}.png')
                elif (self._moving_direction == Direction.RIGHT or self._moving_direction == Direction.UP_RIGHT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/jumping/jumping_start_{self._jump_start_index}{self._active_suffix}.png')

                self._jump_start_index += 1
            else:
                if (self._moving_direction == Direction.LEFT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/jumping/jumping_loop_backwards_{self._jumping_index}{self._active_suffix}.png')
                elif (self._moving_direction == Direction.RIGHT or self._moving_direction == Direction.UP_RIGHT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/jumping/jumping_loop_{self._jumping_index}{self._active_suffix}.png')
                self._jumping_index = self._jumping_index + 1 if self._jumping_index < self._jumping_frame_count else 0

    def slow_to_stop(self):
        if self._velocity > self.MIN_VELOCITY:
            if (self._forced_slow_to_stop or (not globals.pressed_keys[pygame.K_LEFT] and not globals.pressed_keys[pygame.K_RIGHT])):
                self._velocity -= self.ACCELERATION / 4 if self._is_jumping else self.ACCELERATION

            if self._moving_direction == Direction.LEFT:
                self.set_position(self._rect.x - self._velocity)
            elif self._moving_direction == Direction.RIGHT:
                self.set_position(self._rect.x + self._velocity)
        else:
            self._velocity = self.MIN_VELOCITY if self._collision_side != Sides.TOP else 0

    def walking(self):
        if (self._is_walking or self._velocity > 0):
            _walking_type: str = 'walking' if not self._is_crouching else 'crouch_walk'
            if (self._moving_direction == Direction.LEFT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/walking/{_walking_type}_backwards_{self._walking_index}{self._active_suffix}.png')
            elif (self.facing_direction == Direction.RIGHT) or (self.facing_direction == Direction.NONE):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/walking/{_walking_type}_{self._walking_index}{self._active_suffix}.png')
            elif (self.facing_direction == Direction.UP_RIGHT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/walking/{_walking_type}_looking_up_{self._walking_index}{self._active_suffix}.png')
            elif (self.facing_direction == Direction.UP_LEFT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/walking/{_walking_type}_looking_up_backwards_{self._walking_index}{self._active_suffix}.png')
            elif (self.facing_direction == Direction.UP):
                if (self._moving_direction == Direction.LEFT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/walking/walking_looking_up_backwards_{self._walking_index}{self._active_suffix}.png')
                elif (self._moving_direction == Direction.RIGHT or self._moving_direction == Direction.NONE):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/walking/walking_looking_up_{self._walking_index}{self._active_suffix}.png')
            self._walking_index = self._walking_index + 1 if self._walking_index < self._walking_frame_count else 0
        else:
            _standing_type: str = 'standing' if not self._is_crouching else 'crouching'
            if (self.facing_direction == Direction.LEFT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/{_standing_type}_still_backwards{self._active_suffix}.png')
            elif (self.facing_direction == Direction.RIGHT) or (self.facing_direction == Direction.NONE):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/{_standing_type}_still{self._active_suffix}.png')
            elif (self.facing_direction == Direction.UP_RIGHT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still_looking_up{self._active_suffix}.png')
            elif (self.facing_direction == Direction.UP_LEFT):
                self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still_looking_up_backwards{self._active_suffix}.png')
            elif (self.facing_direction == Direction.UP):
                if (self._moving_direction == Direction.LEFT):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still_looking_up_backwards{self._active_suffix}.png')
                elif (self._moving_direction == Direction.RIGHT or self._moving_direction == Direction.NONE):
                    self.surf = pygame.image.load(f'{self.IMAGE_PATH}/standing_still_looking_up{self._active_suffix}.png')
            self._walking_index = 0

            self.facing_direction = self._moving_direction

    def running(self):
        if (self._moving_direction == Direction.LEFT):
            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/running/running_backwards_{self._running_index}{self._active_suffix}.png')
        else:
            self.surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/running/running_{self._running_index}{self._active_suffix}.png')            
        self._running_index = self._running_index + 1 if self._running_index < self._running_frame_count else 0