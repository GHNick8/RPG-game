# RPG Starter Template (Python + Pygame)

This is a modular RPG framework built with Python and Pygame. It includes:

- Tile-based movement and overworld
- Random encounters and a battle system
- Inventory and shop system
- Scene manager and menu UI
- Save/load functionality

## How to Run

1. Install pygame:  
   `pip install pygame`

   1.2. Optional:
        Use virtual env 
        - `python -m venv venv`
        - `venv\scripts\activate`
        - `pip install pygame`

2. Run the game:  
   `python main.py`

## Structure

- `main.py` – Entry point
- `scenes/` – Title, Overworld, Battle scenes
- `ui/` – Modular menus (shop, player, save)
- `assets/` – Sprites and tiles
- `settings.py` – Config for screen, fonts, colors
- `scene_manager.py` – Handles scene switching

## Customize It

- Replace placeholder assets with your own
- Expand the battle system with magic, enemies, etc.
- Create new scenes (dungeons, world map, etc.)
