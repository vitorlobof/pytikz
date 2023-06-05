from pathlib import Path
import os

BASE_DIR = Path().parent.parent.resolve()
BOARD_DIR = os.path.join(BASE_DIR, 'tikz', 'template')

if __name__=='__main__':
    print(
        BASE_DIR,
        BOARD_DIR,
        OUT_DIR,
        sep='\n'
    )
