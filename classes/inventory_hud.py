from typing import List
import pygame
import globals
from classes.weapon import Weapon


class InventoryHUD:
    def __init__(self, inventory):
        self._inventory = inventory
        self.reset_position()
        
    CELL_MAX = 1
    RIGHT_OFFSET = 50
    LARGE_RIGHT_OFFSET = 96
    menu_open = False
    _position = { 'x': 0, 'y': 0 }
    _inventory: Weapon = []
    _columns = 3
    _column_count = 0
    _row_count = 1
    _game_paused = False
    _key_press_timer = 0
    _selected_index = -1

    def toggle_menu(self):
        if not self.menu_open:
            self.menu_open = True 
            globals.game_paused = True
            for index, item in enumerate(self._inventory):
                if isinstance(item, Weapon):
                    if item.selected:
                        self._selected_index = index
                        break
        else: 
            self.menu_open = False
            if (self._selected_index != -1):
                for item in self._inventory:
                    if isinstance(item, Weapon):
                        item.selected = False
                        continue
                self._inventory[self._selected_index].selected = True
                self._selected_index = -1
            globals.game_paused = False

    def reset_position(self):
        self._position = { 'x': 290, 'y': 10 }

    def add_item(self, item: Weapon):
        self._inventory.append(item)
        self.draw()

    def remove_item(self, item: Weapon):    
        self._inventory.remove(item)
        self.draw()

    def get_inventory(self) ->  List[Weapon]:
        return self._inventory
    
    def draw_menu(self):

        # add background image
        inventory_bg_surf = pygame.image.load('sprites/backgrounds/inventory_bg.png')
        inventory_bg_surf_rect = inventory_bg_surf.get_rect()
        inventory_bg_surf_rect.x = globals.SCREEN.get_width() / 2 - inventory_bg_surf_rect.width / 2
        inventory_bg_surf_rect.y = globals.SCREEN.get_height() / 2 - inventory_bg_surf_rect.height / 2
        globals.SCREEN.blit(inventory_bg_surf, inventory_bg_surf_rect)

        # now add heading
        heading_font = pygame.font.Font('fonts/Unkempt-Bold.ttf', 36)
        heading_surf = heading_font.render(f"Inventory", True, (255, 255, 255))
        heading_surf_rect = heading_surf.get_rect()
        heading_surf_rect.x = inventory_bg_surf_rect.x + 35
        heading_surf_rect.y = inventory_bg_surf_rect.y + 30
        globals.SCREEN.blit(heading_surf, heading_surf_rect)

        # now add instructions 
        instruction_font = pygame.font.Font('fonts/Unkempt-Bold.ttf', 24)
        instruction_surf = instruction_font.render(f"Use your arrow keys <- -> to select an item.", True, (255, 255, 255))
        instruction_surf_rect = instruction_surf.get_rect()
        instruction_surf_rect.x = heading_surf_rect.x + 5
        instruction_surf_rect.y = heading_surf_rect.y + 45
        globals.SCREEN.blit(instruction_surf, instruction_surf_rect)

        # now add instructions 
        instruction_surf = instruction_font.render(f"'Enter' to equip.", True, (255, 255, 255))
        instruction_surf_rect = instruction_surf.get_rect()
        instruction_surf_rect.x = heading_surf_rect.x + 5
        instruction_surf_rect.y = heading_surf_rect.y + 75
        globals.SCREEN.blit(instruction_surf, instruction_surf_rect)

        # now add cells
        self.reset_position()
        self._column_count = 0
        self._row_count = 0
        starting_x = instruction_surf_rect.x + 100
        starting_y = instruction_surf_rect.y + 50

        # display weapons first
        for item in self._inventory:
            if isinstance(item, Weapon):
                cell_surf = pygame.image.load('sprites/assets/ui/inventory_cell_large.png')
                cell_surf_rect = cell_surf.get_rect()
                cell_surf_rect.x = starting_x
                cell_surf_rect.y = starting_y
                image_surf = pygame.image.load(f'{item.IMAGE_PATH}/inventory_large.png') if not item.selected else pygame.image.load(f'{item.IMAGE_PATH}/inventory_large_selected.png')
                image_surf_rect = image_surf.get_rect()
                image_surf_rect.x = cell_surf_rect.x + cell_surf_rect.width / 2 - image_surf_rect.width / 2
                image_surf_rect.y = cell_surf_rect.y + cell_surf_rect.height / 2 - image_surf_rect.height / 2
                globals.SCREEN.blit(cell_surf, cell_surf_rect)
                globals.SCREEN.blit(image_surf, image_surf_rect)
                starting_x += self.LARGE_RIGHT_OFFSET
                self._column_count += 1

        # add remaining empty inventory cells     
        while self._column_count < self.CELL_MAX:
            cell_surf = pygame.image.load('sprites/assets/ui/inventory_cell_large.png')
            cell_surf_rect = cell_surf.get_rect()
            cell_surf_rect.x = starting_x
            cell_surf_rect.y = starting_y
            globals.SCREEN.blit(cell_surf, cell_surf_rect)
            starting_x += self.LARGE_RIGHT_OFFSET
            self._column_count += 1

    
    def draw(self):
        self.reset_position()
        self._column_count = 0
        self._row_count = 0    

        # display weapons first
        for item in self._inventory:
            if isinstance(item, Weapon) and item.selected:
                if self._column_count > self.CELL_MAX:
                    self._row_count += 1
                    self._column_count = 0
                    self._position['y'] += self.RIGHT_OFFSET
                    self._position['x'] = globals.SCREEN.get_width() / 2 - 300

                cell_surf = pygame.image.load('sprites/assets/ui/inventory_cell.png')
                cell_surf_rect = cell_surf.get_rect()
                cell_surf_rect.x = self._position['x']
                cell_surf_rect.y = self._position['y']
                image_surf = pygame.image.load(f'{item.IMAGE_PATH}/inventory.png')
                image_surf_rect = image_surf.get_rect()
                image_surf_rect.x = self._position['x'] + 3
                image_surf_rect.y = self._position['y'] + 5
                globals.SCREEN.blit(cell_surf, cell_surf_rect)
                globals.SCREEN.blit(image_surf, image_surf_rect)
                self._position['x'] += self.RIGHT_OFFSET
                self._column_count += 1

        # add remaining empty inventory cells     
        while self._column_count < self.CELL_MAX:
            cell_surf = pygame.image.load('sprites/assets/ui/inventory_cell.png')
            cell_surf_rect = cell_surf.get_rect()
            cell_surf_rect.x = self._position['x']
            cell_surf_rect.y = self._position['y']
            globals.SCREEN.blit(cell_surf, cell_surf_rect)
            self._position['x'] += self.RIGHT_OFFSET
            self._column_count += 1
        
        if (self.menu_open):
            if (self._key_press_timer == 0):
                if globals.pressed_keys[pygame.K_LEFT]:
                    self._key_press_timer = 8
                    for index, item in enumerate(self._inventory):
                        if isinstance(item, Weapon):
                            if item.selected:
                                if index > 0:
                                    item.selected = False
                                    self._inventory[index - 1].selected = True
                                break
                if globals.pressed_keys[pygame.K_RIGHT]:
                    self._key_press_timer = 8
                    for index, item in enumerate(self._inventory):
                        if isinstance(item, Weapon):
                            if item.selected:
                                if index < len(self._inventory) - 1:
                                    item.selected = False
                                    self._inventory[index + 1].selected = True
                                break

                if globals.pressed_keys[pygame.K_RETURN]:
                    self._selected_index = -1
                    self.toggle_menu()
            else:
                self._key_press_timer -= 1
            self.draw_menu()

        