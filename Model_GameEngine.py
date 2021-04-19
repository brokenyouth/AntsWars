import pygame
import pygame_gui
from Model_Ant import *
from Model_Obstacle import *
from Model_Anthil import *
from Model_Spider import *
from Renderer import *
from Util import *
class GameEngine():

    def __init__(self, _world, _mngr, _surface):
        self.world = _world
        self.manager = _mngr
        self.surface = _surface
        self.worldSizeX, self.worldSizeY = self.world.getDimensions()
        self.renderer = None

        self.surfaceWidth = self.surface.get_width()
        self.surfaceHeight = self.surface.get_height()

    
    def initGame(self, nbAnthils, nbAntPerAnthil ):
        for n in range(nbAnthils):
            x, y = DEFAULT_ANTHIL_POSITIONS[ n % len(DEFAULT_ANTHIL_POSITIONS) ]
            color = DEFAULT_ANTHIL_COLOR[ n % len(DEFAULT_ANTHIL_POSITIONS) ]
            anthil = Anthil( x , y  , nbAntPerAnthil, color )
            for i in range(nbAntPerAnthil):
                ant = Ant( x, y, getRandRange( 2 * PI ), color, i )
                ant.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE
                ant.color = color # mettre un setColor ici plus tard
                anthil.addAnt( ant )
            self.world.addAnthil( x, y, anthil )
        
        spider = Spider( random.randrange(0, self.worldSizeX) * TILZSIZE, random.randrange(0, self.worldSizeY) * TILZSIZE, getRandRange( 2 * PI ), color, 0 )
        spider.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE

        self.world.addSpider(spider.x, spider.y, spider)
        
        obstacle = Obstacle( self.surfaceWidth//2, self.surfaceHeight//2, (255, 255, 255, 255) )
        self.world.addObstacle(obstacle.x, obstacle.y, obstacle)

    def start(self):
        # Define some variables
        self.toggle = True
        self.simulation_is_running = False
        self.reset_simulation = False
        self.game_not_initialized = True
        # Set background
        bg = self.manager.get_theme().get_colour('dark_bg')
        # Set UI
        
        self.panel = pygame_gui.elements.UIPanel(pygame.Rect(175, 0, self.surfaceWidth - (200 + 175), 75),
                             starting_layer_height=4,
                             manager=self.manager)
        self.gamemode = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1, 1, 200, 30),
                                               manager=self.manager, options_list=['Simple', '2 Species', '4 Species'],
                                               container=self.panel,
                                               starting_option='Simple')
        self.start_simulation_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (25, 35) ,
                                                               (75,
                                                                30)),
                                     text="Start!",
                                     manager=self.manager,
                                     container=self.panel,
                                     object_id='#1,2' )
        self.reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (105, 35) ,
                                                               (75,
                                                                30)),
                                     text="Reset!",
                                     manager=self.manager,
                                     container=self.panel,
                                     object_id='#1,2' )
        
        self.anthill_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (215, 0) ,
                                                               (125,
                                                                30)),
                                     text="Drop Anthill",
                                     manager=self.manager,
                                     container=self.panel,
                                     object_id='#1,2' )

        self.spider_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (215, 35) ,
                                                               (125,
                                                                30)),
                                     text="Drop Spider",
                                     manager=self.manager,
                                     container=self.panel,
                                     object_id='#1,2' )

        self.ressource_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (350, 0) ,
                                                               (125,
                                                                30)),
                                     text="Drop Ressource",
                                     manager=self.manager,
                                     container=self.panel,
                                     object_id='#1,2' )

        self.editmode_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (485, 0) ,
                                                               (125,
                                                                30)),
                                     text="Edit Mode",
                                     manager=self.manager,
                                     container=self.panel,
                                     object_id='#1,2' )

        self.speed_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect( (605, 0) ,
                                                (125, 30) ),
                                    text="Speed",
                                    manager=self.manager,
                                    container=self.panel,
                                    object_id='#1,2'  )

        self.speed_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(700, 1, 100, 30),
                                               manager=self.manager, options_list=['10%', '50%', '100%', '200%', '400%'],
                                               container=self.panel,
                                               starting_option='100%')
                                                         

        self.toggle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (75, 0) ,
                                                               (75,
                                                                50)),
                                     text="Toggle",
                                     manager=self.manager,
                                     object_id='#1,2' )
        # Set renderer
        self.renderer = Renderer( self.surface, self.world, bg )

    def handleEvent(self, _event):
        """"
        Updates all GameEngine related events like keyboard press, mouse press, exit detection and so on.
        :Return: a boolean to keep track whether or not we should close the window.
        """
        is_running = True
        if _event.type == pygame.QUIT:
            is_running = False
        if _event.type == pygame.MOUSEBUTTONUP:
            print ( pygame.mouse.get_pos() )
        return is_running

    def updateSpiders(self, dt):
        """
        This function runs over every spider in the world/terrain and updates their position.
        Similar to updateAnts() function.
        """
        for spider in self.world.getSpiders():
            spider_direction = spider.getDirection()
            dirX, dirY = spider_direction.getVec()
            x = ((MOVESPEED) * dt) * dirX
            y = ((MOVESPEED) * dt) * dirY

            if spider.x < 0:
                x = self.surfaceWidth
            elif spider.y < 0:
                y = self.surfaceHeight
            elif spider.x > self.surfaceWidth:
                spider.x = 0
            elif spider.y > self.surfaceHeight:
                spider.y = 0
            
            spider.lastDirectionUpdate += dt
            if spider.lastDirectionUpdate > DIRECTIONUPDATERATE:
                randDir = getRandDirectionRange()
                spider.direction.addTarget(randDir)
                spider.lastDirectionUpdate = 0

            spider.addPosition(x,y)
            spider.direction.update(dt)

    def updateAnts(self, anthil, dt):
        """
        This function runs over every ant in the world/terrain which belongs to a certain anthill and updates their position.
        """
        for ant in anthil.getAnts():
            ant_direction = ant.getDirection()
            dirX, dirY = ant_direction.getVec()
            x = (MOVESPEED * dt) * dirX
            y = (MOVESPEED * dt) * dirY

            if ant.x < 0:
                ant.x = self.surfaceWidth
            elif ant.y < 0:
                ant.y = self.surfaceHeight
            elif ant.x > self.surfaceWidth:
                ant.x = 0
            elif ant.y > self.surfaceHeight:
                ant.y = 0
            
            ant.lastDirectionUpdate += dt
            if ant.lastDirectionUpdate > DIRECTIONUPDATERATE:
                randDir = getRandDirectionRange()
                ant.direction.addTarget(randDir)
                ant.lastDirectionUpdate = 0

            ant.addPosition(x,y)
            ant.direction.update(dt)
    
    def updateUI(self, dt):
        # Check toggle panel
        if self.toggle_button.check_pressed():
            self.toggle = not self.toggle

        if not self.toggle:
            self.panel.hide()
            self.toggleEnableDisableCustomizationButtons() # check for customizations buttons because .show() enables them by default
        else:
            self.panel.show()
            self.toggleEnableDisableCustomizationButtons()
        
        # Check if we should run/stop the simulation.
        if self.start_simulation_button.check_pressed():
            self.simulation_is_running = not self.simulation_is_running
            if self.start_simulation_button.text == "Start!":
                # block any attempt to start a new game ontop of the current one.
                if self.game_not_initialized:
                    self.prepareGame()
                    self.game_not_initialized = not self.game_not_initialized
                self.start_simulation_button.set_text("Stop!")
            else:
                self.start_simulation_button.set_text("Start!")
        
        # Check if we should reset the simulation
        if self.reset_button.check_pressed():
            self.reset_simulation = not self.reset_simulation
            self.simulation_is_running = False
            self.game_not_initialized = not self.game_not_initialized

        # update buttons interaction
        self.toggleEnableDisableCustomizationButtons()
        

    def update(self, dt):
        self.manager.update(dt)
        self.updateUI(dt)

        # update world entities if the simulation is running
        if self.simulation_is_running:
            self.updateSpiders(dt)
            for anthil in self.world.getAnthils():
                self.updateAnts(anthil, dt)
        
        # reset the world if asked to
        if self.reset_simulation:
            self.resetWorld()
            self.start_simulation_button.set_text("Start!")
            self.reset_simulation = not self.reset_simulation #fix bug with button ??

        """
        print('simulation status -> ', self.simulation_is_running)
        print('start button simulation status -> ', self.start_simulation_button)
        print('reset simulation status -> ', self.reset_simulation)
        print('reset button simulation status -> ', self.reset_button)
        """

        
    def render(self):
        self.renderer.render()

    def resetWorld(self):
        self.world.reset()
    
    def prepareGame(self):
        if self.game_not_initialized:
            selected_gamemode = self.gamemode.selected_option

            if selected_gamemode == 'Simple':
                self.initGame( 1, 100 )
            elif selected_gamemode == '2 Species':
                self.initGame( 2, 100 )
            elif selected_gamemode == '4 Species':
                self.initGame( 4, 100 )
    
    def toggleEnableDisableCustomizationButtons(self):
        if not self.game_not_initialized:
            self.gamemode.disable()
        else:
            self.gamemode.enable()
