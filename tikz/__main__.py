import os
import sys
import importlib
import subprocess
from .settings import BASE_DIR

def convert_to_svg(basename):
    to_svg = subprocess.Popen([
        'inkscape',
        '--export-type=svg',
        '--pdf-poppler',
        '-l',
        f'{basename}.pdf'
    ])

    to_svg.communicate()

    if to_svg.returncode == 0:
        print('Conversion to svg successful.')
    else:
        print('Conversion to svg failed.')

def rename_texfile(basename):
    board = os.path.join(BASE_DIR, 'board.pdf')
    dst = os.path.join(BASE_DIR, f'{basename}.pdf')
    
    if os.path.exists(dst):
        os.remove(dst)
    
    os.rename(board, dst)

def import_class(filepath, class_name):
    module_name = filepath.replace('.py', '').replace('/', '.')
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_

def run_command_line():
    args = sys.argv

    if len(args) == 3:
        filepath, class_name = sys.argv[1:]
    elif len(args) == 4:
        filepath, class_name, last_arg = sys.argv[1:]
    else:
        raise NotImplemented
    
    class_ = import_class(filepath, class_name)
    instance = class_()
    instance.render()
    rename_texfile(instance.__class__.__name__)

    if len(args) == 4 and last_arg == '-svg':
        convert_to_svg(class_name)

if __name__=='__main__':
    run_command_line()
