import os
import importlib
from pathlib import Path


BASE_DIR = Path().parent.parent.resolve()
BOARD_DIR = os.path.join(BASE_DIR, 'tikz', 'template')
OUTPUT_DIR = BASE_DIR

settings_filepath = os.path.join(BASE_DIR, 'settings.py')

if os.path.exists(settings_filepath):
    module = importlib.import_module('settings')
    OUTPUT_DIR = getattr(module, 'OUTPUT_DIR')
