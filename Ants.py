import pygame
import pygame_gui
from Model_GameEngine import *
from Model_Terrain import *
from Model_Obstacle import *
from Model_Ant import *
import math

class Ants:

    def __init__(self, _width, _height):
        """
        Main APP.
        Intialized the window, surface and UI managers and the game engine!
        """
        self.windowWidth = _width
        self.windowHeight = _height
        self.window_surface = None
        self.manager = None
        self.clock = None
        self.background = None
        self.ui_container = None

    def start(self):
        pygame.init()

        pygame.display.set_caption('Ants Simulation')
        self.window_surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.manager = pygame_gui.UIManager((self.windowWidth, self.windowHeight), 'data/themes/button_theming_test_theme.json')
        self.background = self.manager.get_theme().get_colour('dark_bg')
        self.clock = pygame.time.Clock()
        self.gameEngine = GameEngine(Terrain(self.windowWidth, self.windowHeight), self.manager, self.window_surface)
        self.gameEngine.start()

    def run(self):
        """
        Main APP loop
        """
        is_running = True
        while is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                is_running = self.handleEvent(event)
                self.manager.process_events(event)
                
            self.gameEngine.update(time_delta)
            self.gameEngine.render()
            self.manager.draw_ui(self.window_surface)


            pygame.display.update()


    def handleEvent(self, e):
        """
        Let the engine handle the events.
        """
        return self.gameEngine.handleEvent(e)