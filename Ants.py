import pygame
import pygame_gui
from Model_GameEngine import *
from Model_Terrain import *
from Model_Obstacle import *
from Model_Ant import *
import math

class Ants:

    def __init__(self, _width, _height):
        self.windowWidth = _width
        self.windowHeight = _height
        self.window_surface = None
        self.manager = None
        self.clock = None
        self.background = None

    def start(self):
        pygame.init()

        pygame.display.set_caption('Ant vs Ant Simulator')
        self.window_surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.manager = pygame_gui.UIManager((self.windowWidth, self.windowHeight), 'data/themes/button_theming_test_theme.json')
        self.clock = pygame.time.Clock()
        self.gameEngine = GameEngine(Terrain(self.windowWidth, self.windowHeight), self.manager, self.window_surface)
        self.gameEngine.start()

        self.background = pygame.Surface((self.windowWidth, self.windowHeight))
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))

    def run(self):
        is_running = True

        while is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                self.manager.process_events(event)
                
            self.gameEngine.update(time_delta)
            self.gameEngine.render()

            #self.manager.update(time_delta) # effacer ça plus tard...
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()


    def handleEvent(self, e):
        pass