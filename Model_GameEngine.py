import pygame
import pygame_gui
from Model_Ant import *
from Model_Obstacle import *
from Model_Anthil import *
from Model_Spider import *
from Model_Ressource import *
from Model_Pheromone import *
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
    
    def addRessourceAt(self, x, y):
        # bound check
        ressource = Ressource( x , y )
        self.world.addEntity( ressource.x , ressource.y , ressource )

    def addObstacleAt(self, x, y):
        # bound check
        obstacle = Obstacle( x, y, (255, 255, 255, 255) )
        self.world.addEntity(obstacle.x, obstacle.y, obstacle)
    
    def addSpiderAt(self, x, y):
        # bound check
        spider = Spider( x, y, getRandRange( 2 * PI ), 0 )
        spider.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE

        self.world.addEntity(spider.x, spider.y, spider)

    def addAnthilAt(self, x, y, size, _id):
        # bound check
        color = DEFAULT_ANTHIL_COLOR[ _id ]
        anthil = Anthil( x , y  , size, color, _id )
        for i in range(size):
            ant = Ant( x, y, getRandRange( 2 * PI ), color, _id, AntState.EXPLORE )
            ant.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE
            ant.lastPheromoneUpdate = getRandUnder(100) * 0.01 * PHEROMONEDEPOSITRATE
            ant.color = color
            anthil.addAnt( ant )
        self.world.addEntity( x, y, anthil )
    
    def initGame(self, nbAnthils, nbAntPerAnthil ):
        for n in range(nbAnthils):
            x, y = DEFAULT_ANTHIL_POSITIONS[ n ]
            self.addAnthilAt( x, y, nbAntPerAnthil, n )
            #print( self.world.getAt( x, y ) )
        
        spider = Spider( random.randrange(0, self.worldSizeX) * TILZSIZE, random.randrange(0, self.worldSizeY) * TILZSIZE, getRandRange( 2 * PI ), 0 )
        spider.lastDirectionUpdate = getRandUnder(100) * 0.01 * DIRECTIONUPDATERATE

        self.world.addEntity(spider.x, spider.y, spider)
        
        obstacle = Obstacle( self.surfaceWidth//2, self.surfaceHeight//2, (255, 255, 255, 255) )
        self.world.addEntity(obstacle.x, obstacle.y, obstacle)

    def start(self):
        global CURRENTMODE, EDITMODE
        # Define some variables
        self.toggle = True
        self.simulation_is_running = False
        self.reset_simulation = False
        self.game_not_initialized = True
        CURRENTMODE = 'Simple'
        EDITMODE = EditMode.DISABLE
        # Set background
        bg = self.manager.get_theme().get_colour('dark_bg')
        # Set UI
        
        self.panel = pygame_gui.elements.UIPanel(pygame.Rect(175, 0, self.surfaceWidth - (200 + 175), 125),
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
        
        self.obstacle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (350, 35) ,
                                                               (125,
                                                                30)),
                                     text="Drop Obstacle",
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

        self.editmode_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect( (485, 30) ,
                                                (125, 30) ),
                                    text="Edit OFF",
                                    manager=self.manager,
                                    container=self.panel,
                                    object_id='#1,2'  )

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
                                                         
        self.pheromone_evap_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect( (805, 0) ,
                                                (125, 30) ),
                                    text="Pheromone evap",
                                    manager=self.manager,
                                    container=self.panel,
                                    object_id='#1,2'  )
        
        self.pheromone_evap_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(935, 1, 100, 30),
                                               manager=self.manager, options_list=['10%', '25%', '50%', '95%'],
                                               container=self.panel,
                                               starting_option='25%')

        self.toggle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect( (75, 0) ,
                                                               (75,
                                                                50)),
                                     text="Toggle",
                                     manager=self.manager,
                                     object_id='#1,2' )
        # Set renderer
        self.renderer = Renderer( self.surface, self.world, bg )

        # Init default gamemode
        self.prepareGame()
        self.game_not_initialized = False

    def handleEvent(self, _event):
        """"
        Updates all GameEngine related events like keyboard press, mouse press, exit detection and so on.
        :Return: a boolean to keep track whether or not we should close the window.
        """
        global EDITMODE
        global DRAGFLAG
        is_running = True
        if _event.type == pygame.QUIT:
            is_running = False
        if _event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            # if the mouse click is inside the panel region, and the panel is visible,
            # or if we are in any editmode and clicked inside the toggle button,
            # do nothing.
            # this is hardcoded for 1600*900 resolution
            if self.toggle and ( ( x >= 175 and y >= 0 ) and ( x <= self.surfaceWidth - (200 + 175) and y <= 125 )
                            or ( (x >= 75 and y >= 0 ) and ( x <= 150 and y <= 50 ) ) ):
                return True
            else:
                if EDITMODE == EditMode.ANTHILL_MODE:
                    self.addAnthilAt( x , y , 100, random.randrange(4) )
                    # check if game was initialized here later
                elif EDITMODE == EditMode.SPIDER_MODE:
                    self.addSpiderAt( x, y )
                elif EDITMODE == EditMode.RESSOURCE_MODE:
                    self.addRessourceAt( x , y )
                    print('Ressource at {} / {}'.format(x,y))
                elif EDITMODE == EditMode.OBSTACLE_MODE:
                    DRAGFLAG = False
                    EDITMODE = EditMode.ENABLE
        if _event.type == pygame.MOUSEBUTTONDOWN:
            if EDITMODE == EditMode.OBSTACLE_MODE:
                DRAGFLAG = True
        if DRAGFLAG and (EDITMODE == EditMode.OBSTACLE_MODE):
            x, y = pygame.mouse.get_pos()
            self.addObstacleAt( x , y )

        return is_running

    def updateEntities(self, dt):
        for y in range( int( WIN_HEIGHT // TILZSIZE ) ):
            for x in range( int (WIN_WIDTH / TILZSIZE ) ):
                _entity = self.world.getAt( x, y )
                if isinstance( _entity, Anthil ):
                    self.updateAnthills( _entity, dt )
                elif isinstance( _entity, Spider ):
                    self.updateSpider( _entity, dt )
        self.updatePheromones()

    def updateSpider(self, spider, dt):
        """
        This function runs over every spider in the world/terrain and updates their position.
        Similar to updateAnts() function.
        """
        global MOVESPEED
        
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
    
    def antAI(self, ant, dt):
        """
        Agent based model AI for each ant
        Will decide of it's next actions e.g pick up a ressource, return home, explore, or fight with spider.
        When an Ant finds a ressource, it will take it back home and deposit pheromones on the way.
        When an Ant smells a pheromone, it will follow it.
        When an Ant interacts with a spider, it will fight against it.
        When an Ant is in None of these states, it will explore it's environment.
        """
        ant.lastDirectionUpdate += dt
        ant.lastPheromoneUpdate += dt

        # Check if the ant has interacted with any ressource within a radius
        # ------------------------------------------------------------------
        self.checkRessource( ant )
        # -------------------------------------------------------------------
        # Check if the ant is near/at home.
        # ------------------------------------------------------------------
        self.checkAnthill( ant ) 
        # -------------------------------------------------------------------
        # Check if the ant smells a pheromone
        # ------------------------------------------------------------------
        self.checkPheromones( ant )
        # -------------------------------------------------------------------
        # Explore environment
        # ------------------------------------------------------------------
        self.checkState(ant)
        # ------------------------------------------------------------------


    def checkAnthill(self, ant):
        xhome, yhome = ant.homePosition
        anthill = self.world.getAt( math.floor(xhome // TILZSIZE) , math.floor(yhome // TILZSIZE) )
        if vectorLength( (ant.x - xhome), (ant.y - yhome) ) < TILZSIZE: # is the ant at home
            if ant.getId() == anthill.getId(): # if the ant belongs to this anthill (note: this also works for mutltiple anthill with same color)
                ant.setEnergy(ant.maxEnergy) # refill energy
                if ant.getIsCarryingRessource(): # if the want was carrying a ressource, add team score
                    anthill.addScore()
                ant.setCarryingRessource(False) # set ant as not carrying anymore
                ant.setState( AntState.EXPLORE )
                    

    def checkPheromones(self, ant):
        in_range, pheromone = self.world.hasPheromoneInRange( ant.x, ant.y ) # is there a pheromone in range?
        if in_range:
            if ant.color == pheromone.color :# is this a pheromone for my team?
                # calculate new ant direction
                angle = pheromone.angleToRessource
                ant.direction.instantRedirect( angle )

                

    def checkRessource(self, ant):
        in_range, ressource = self.world.hasRessourceInRange( ant.x, ant.y ) # is there a ressource in range?
        if in_range and (type(ressource) == Ressource):
            if not ant.getIsCarryingRessource(): # if the ant isn't carrying something already
                angle = getAngleBetween( ant.x, ant.y, ressource.x, ressource.y ) # get the ant to go towards the ressource direction
                ant.direction.instantRedirect( angle )
                if not sameCell ( ant.x, ant.y, ressource.x, ressource.y ): 
                    ressource.take() # drop ressource global quantity
                    ant.lastKnownRessource = ressource
                    ant.setCarryingRessource(True) # set ant as carrying ressource
                    ant.setEnergy(ant.maxEnergy // 2) # give her some energy
                    ant.setState( AntState.TOHOME ) # make her go home
                    ant.dropEnergy(5)

    def checkState(self, ant):
        
        if ant.getState( ) == AntState.EXPLORE:
            if ant.lastDirectionUpdate > DIRECTIONUPDATERATE:
                randDir = getRandDirectionRange()
                ant.direction.addTarget(randDir)
                ant.lastDirectionUpdate = 0

        if ant.getState( ) == AntState.TOHOME:
            # find home direction
            xhome, yhome = ant.homePosition
            angle = getAngleBetween( ant.x, ant.y, xhome, yhome )
            ant.direction.instantRedirect( angle )
            if (ant.lastPheromoneUpdate > PHEROMONEDEPOSITRATE) and ant.getEnergy() >= 25:
                is_there, phero = self.world.hasPheromoneInRange(ant.x, ant.y, distance=ant.detectionRadius)
                if not is_there: # is there a pheromone in range?
                    self.depositPheromone( Pheromone( ant.x , ant.y , PheromoneState.Ressource, ant.color, ant.lastKnownRessource.x, ant.lastKnownRessource.y ) )
                    ant.dropEnergy(25)
                ant.lastPheromoneUpdate = 0

        if self.checkWall(ant.x, ant.y):
            ant.setState( AntState.EXPLORE )
            ant.direction.instantRedirect(PI)
        
        """if ant.getIsCarryingRessource() and (ant.getState( ) == AntState.EXPLORE):
            ant.setState( AntState.TOHOME )"""

    def checkWall(self, newX, newY):
        return self.world.hasWallAt( newX, newY, self.surfaceWidth, self.surfaceHeight)

    def depositPheromone(self, _phero):
        self.world.addPheromone( _phero )
    
    def updatePheromones(self):
        global PHEROMONEDISPRATE
        for p in self.world.getPheromones():
            p.intensity -= 0.1
            if (p.intensity < 1) or flip_biased_coin(PHEROMONEDISPRATE / 100):
                self.world.removePheromone(p)

    def updateAnthills(self, anthil, dt):
        """
        This function runs over every ant in the world/terrain which belongs to a certain anthill and updates their position.
        """
        global MOVESPEED
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
            
            self.antAI(ant, dt)

            
            # bad collision detection
            # -----------------------
            if self.checkWall( ant.x + x , ant.y ):
                x = 0
                ant.lastDirectionUpdate = DIRECTIONUPDATERATE + 1
            if self.checkWall( ant.x, ant.y + y ):
                y = 0
                ant.lastDirectionUpdate = DIRECTIONUPDATERATE + 1
            # -----------------------
            
            ant.addPosition(x , y)
            ant.direction.update(dt)
    
    def updateUI(self, dt):
        """
        """
        global EDITMODE
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
                else:
                    self.start_simulation_button.set_text("Stop!")
            else:
                self.start_simulation_button.set_text("Start!")
        
        # Check if we should reset the simulation
        if self.reset_button.check_pressed():
            self.reset_simulation = not self.reset_simulation
            self.simulation_is_running = False
            self.game_not_initialized = True # check this if something goes wrong

        # Check speed
        self.updateSpeed()

        # Check pheromone rate
        self.updatePheromoneRate()

        # update buttons interaction
        self.toggleEnableDisableCustomizationButtons()

        # check if we should switch to editmode
        if self.editmode_button.check_pressed():
            if not self.simulation_is_running: # if we are not in simulation mode, allow edit mode
                if EDITMODE == EditMode.ENABLE:
                    EDITMODE = EditMode.DISABLE
                    self.editmode_label.set_text("Edit OFF")
                    self.toggleEnableDisableCustomizationButtons()
                else:
                    EDITMODE = EditMode.ENABLE
                    self.editmode_label.set_text("Edit ON")
                    self.toggleEnableDisableCustomizationButtons()
        # check other edit modes
        if self.anthill_button.check_pressed():
            EDITMODE = EditMode.ANTHILL_MODE
        if self.spider_button.check_pressed():
            EDITMODE = EditMode.SPIDER_MODE
        if self.ressource_button.check_pressed():
            EDITMODE = EditMode.RESSOURCE_MODE
        if self.obstacle_button.check_pressed():
            EDITMODE = EditMode.OBSTACLE_MODE

    def update(self, dt):
        self.manager.update(dt)
        self.updateUI(dt)

        # update world entities if the simulation is running
        if self.simulation_is_running:
            self.updateEntities(dt)
        
        # reset the world if asked to
        if self.reset_simulation:
            self.resetWorld()
            self.start_simulation_button.set_text("Start!")
            self.reset_simulation = not self.reset_simulation #fix bug with button ??
        
    def render(self):
        self.renderer.render()

    def resetWorld(self):
        global EDITMODE
        self.world.reset()
        self.simulation_is_running = False
        EDITMODE = EditMode.DISABLE
        self.editmode_label.set_text("Edit OFF")
    
    def updateSpeed(self):
        global MOVESPEED
        if self.speed_dropdown.selected_option == '10%':
            MOVESPEED = DEFAULTMOVESPEED * 0.1
        elif self.speed_dropdown.selected_option == '50%':
            MOVESPEED = DEFAULTMOVESPEED * 0.5
        elif self.speed_dropdown.selected_option == '100%':
            MOVESPEED = DEFAULTMOVESPEED
        elif self.speed_dropdown.selected_option == '200%':
            MOVESPEED = DEFAULTMOVESPEED * 2.0
        elif self.speed_dropdown.selected_option == '400%':
            MOVESPEED = DEFAULTMOVESPEED * 4.0

    def updatePheromoneRate(self):
        global PHEROMONEDISPRATE
        if self.pheromone_evap_dropdown.selected_option == "10%":
            PHEROMONEDISPRATE = 0.10
        elif self.pheromone_evap_dropdown.selected_option == "25%":
            PHEROMONEDISPRATE = 0.25
        elif self.pheromone_evap_dropdown.selected_option == "50%":
            PHEROMONEDISPRATE = 0.50
        elif self.pheromone_evap_dropdown.selected_option == "95%":
            PHEROMONEDISPRATE = 0.95

    def prepareGame(self):
        if self.game_not_initialized:
            self.resetWorld()
            selected_gamemode = self.gamemode.selected_option
            if selected_gamemode == 'Simple':
                self.initGame( 1, 50 )
            elif selected_gamemode == '2 Species':
                self.initGame( 2, 50 )
            elif selected_gamemode == '4 Species':
                self.initGame( 4, 150 )
            #self.game_not_initialized = not self.game_not_initialized
    
    def toggleEnableDisableCustomizationButtons(self):
        if not self.game_not_initialized:
            self.gamemode.disable()
        else:
            self.gamemode.enable()
        
        if EDITMODE == EditMode.DISABLE:
                self.anthill_button.disable()
                self.spider_button.disable()
                self.ressource_button.disable()
                self.obstacle_button.disable()
        elif EDITMODE == EditMode.ENABLE:
                self.anthill_button.enable()
                self.spider_button.enable()
                self.ressource_button.enable()
                self.obstacle_button.enable()
            
