import sys
import os

# Add the game directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.scripts.Main import main

if __name__ == "__main__":
    main.run()