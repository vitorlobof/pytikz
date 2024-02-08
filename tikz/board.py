import os
import subprocess
from .settings import BASE_DIR, BOARD_DIR, OUTPUT_DIR

class Board:
    directory = OUTPUT_DIR
    objs = []

    header = '\n'.join((
        r'\documentclass{standalone}',
        r'\usepackage{tikz}'
    ))

    begin = '\n'.join((
        r'\begin{document}',
        r'\begin{tikzpicture}'
    ))

    end = '\n'.join((
        r'\end{tikzpicture}',
        r'\end{document}'
    ))

    def add(self, *objs) -> None:
        self.objs.extend(objs)
    
    def construct(self):
        pass

    def rename_file(self):
        basename = self.__class__.__name__
        src = os.path.join(BASE_DIR, 'board.pdf')
        dst = os.path.join(OUTPUT_DIR, self.directory, f'{basename}.pdf')

        if os.path.exists(dst):
            os.remove(dst)
        
        os.rename(src, dst)

    def render(self) -> None:
        filepath = os.path.join(BOARD_DIR, 'board.tex')

        self.construct()

        code = '\n\n'.join((
            self.header,
            self.begin,
            '\n'.join(obj.render() for obj in self.objs),
            self.end
        ))

        with open(filepath, 'w+', encoding='utf-8') as f:
            f.write(code)

        print('Compiling LaTeX file.')

        process = subprocess.Popen(
            ['pdflatex', filepath], stdout=subprocess.DEVNULL)
        process.communicate()

        self.rename_file()
        
        if process.returncode == 0:
            print('LaTeX compilation successful.')
        else:
            print('LaTeX compilation failed.')
