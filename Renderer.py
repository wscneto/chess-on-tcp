import pygame, chess
from typing import Tuple, Optional

# Responsável pela renderização do tabuleiro, peças e destaques
class Renderer:
    LIGHT_BROWN = (240, 217, 181)
    DARK_BROWN = (181, 136, 99)
    HIGHLIGHT_SELECTED = (255, 255, 0, 100)
    HIGHLIGHT_LEGAL = (0, 0, 255, 80)

    def __init__(self, width=640, height=640):
        self.width = width
        self.height = height
        self.square_size = width // 8
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Online Chess")

    def draw_board(self):
        # Desenha o tabuleiro 8x8 com cores alternadas
        for row in range(8):
            for col in range(8):
                color = self.LIGHT_BROWN if (row + col) % 2 == 0 else self.DARK_BROWN
                pygame.draw.rect(self.window, color, 
                               (col * self.square_size, row * self.square_size, 
                                self.square_size, self.square_size))

    def draw_pieces(self, board: chess.Board, piece_images: dict, is_black_perspective: bool):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if is_black_perspective:
                    # Muda a perspectiva para visualização do jogador de pretas
                    row = square // 8 
                    col = 7 - (square % 8)
                else:
                    row = 7 - (square // 8)
                    col = square % 8
                    
                color = 'w' if piece.color == chess.WHITE else 'b'
                key = color + piece.symbol().upper()
                piece_image = piece_images[key]
                self.window.blit(piece_image, (col * self.square_size, row * self.square_size))

    def highlight_moves(self, board: chess.Board, selected_square: Optional[int], is_black_perspective: bool):
        if selected_square is None:
            return
        
        if is_black_perspective:
            file = 7 - chess.square_file(selected_square)
            rank = chess.square_rank(selected_square)
            vis_selected_square = chess.square(file, rank)
        else:
            vis_selected_square = selected_square
        
        self._draw_overlay_square(vis_selected_square, self.HIGHLIGHT_SELECTED, is_black_perspective)
        
        for move in board.legal_moves:
            if move.from_square == selected_square:
                to_square = move.to_square
                if is_black_perspective:
                    file = 7 - chess.square_file(to_square)
                    rank = chess.square_rank(to_square)
                    vis_to_square = chess.square(file, rank)
                else:
                    vis_to_square = to_square
                self._draw_overlay_square(vis_to_square, self.HIGHLIGHT_LEGAL, is_black_perspective)

    def _draw_overlay_square(self, square: int, color_rgba: Tuple[int, int, int, int], is_black_perspective: bool):
        if is_black_perspective:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            col = file
            row = rank
        else:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
        
        overlay = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        overlay.fill(color_rgba)
        self.window.blit(overlay, (col * self.square_size, row * self.square_size))

    def draw_game_over_screen(self, result_text: str):
        # Desenha a tela de fim de jogo com o resultado
        self.draw_board()
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        self.window.blit(overlay, (0, 0))
        
        if len(result_text) > 20:
            parts = result_text.split('!')
            if len(parts) > 1:
                self._draw_text_center(parts[0] + '!', 48, -60)
                self._draw_text_center(parts[1], 48, 0)
            else:
                self._draw_text_center(result_text, 48, -30)
        else:
            self._draw_text_center(result_text, 48, -30)
        
        again_rect = self._draw_text_center("Play Again", 36, 60)
        pygame.display.flip()
        return again_rect

    def _draw_text_center(self, text: str, size: int, y_offset=0, color=(0, 0, 0)):
        font = pygame.font.SysFont("arial", size, True)
        render = font.render(text, True, color)
        rect = render.get_rect(center=(self.width // 2, self.height // 2 + y_offset))
        self.window.blit(render, rect)
        return rect

    def get_square_from_mouse(self, pos: Tuple[int, int], is_black_perspective: bool) -> int:
        # Converte posição do clique do mouse para a casa correspondente no tabuleiro
        x, y = pos
        col = x // self.square_size
        row = y // self.square_size
        
        if is_black_perspective:
            visual_col = 7 - col
            visual_row = row
        else:
            visual_col = col
            visual_row = 7 - row
            
        return chess.square(visual_col, visual_row)