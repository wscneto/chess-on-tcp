import os, cairosvg, io, pygame

# Classe que carrega e armazena as imagens SVG das peças em formato PNG
class AssetsManager:
    def __init__(self):
        self.pieces = {}
        self.load_assets()

    def load_assets(self):
        # Carrega cada tipo de peças brancas e pretas
        piece_names = ['P', 'R', 'N', 'B', 'Q', 'K']
        for piece in piece_names:
            self.pieces['w' + piece] = self._load_svg('w' + piece)
            self.pieces['b' + piece] = self._load_svg('b' + piece)

    def _load_svg(self, name: str):
        # Converte o SVG da peça para imagem compatível com pygame
        svg_path = os.path.join('assets', name + '.svg')
        png_data = cairosvg.svg2png(url=svg_path, output_width=80, output_height=80)
        return pygame.image.load(io.BytesIO(png_data)).convert_alpha()