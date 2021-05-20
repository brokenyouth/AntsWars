# AntsWars

Requirements:
    Pygame & Pygame_gui
    On any terminal (make sure python & pip are added to PATH):
    
    pip3 install pygame
    pip3 install pygame_gui


Structure:

    MVC Architecture

    Model: 
        • Ant.py
        • Anthill.py
        • Obstacle.py
        • Ressource.py
        • Pheromone.py
        • Spider.py
        • Terrain.py ( world )

    View:
        • Renderer.py (renders the world's entites based on their state)

    Controller:
        • GameEngine.py ( all logic is here )

    Main class:
        • Ants.py

    Utility functions file:
        • Util.py

    Entry point:
        • Main.py

Unfinished:

    Ant vs Ant combat
    Better ant wall check
    Spider AI
    Add different type of ants (workers, warriors, etc.)
    Better ressource check
    Optimize code (it's slow, really)

Bugs:

    A random bug occurs with ressource check which crashes the app (?)
    TypeError: cannot unpack non-iterable bool object

