import pygame, sys, chess
from NetworkManager import NetworkManager
from GameState import GameState
from Renderer import Renderer
from AssetsManager import AssetsManager

# Classe principal que inicializa e controla o ciclo de vida do jogo
class MainGame:
    def __init__(self):
        # Inicializa os componentes principais do jogo
        self.renderer = Renderer() # Responsável por desenhar o tabuleiro e peças
        self.assets = AssetsManager() # Carrega as imagens das peças
        self.game_state = GameState() # Armazena o estado atual do jogo
        self.network = NetworkManager() # Gerencia comunicação em rede
        self.running = True
        self.clock = pygame.time.Clock()
        self.network.game_over_callback = self._handle_remote_game_over # Callback para fim de jogo remoto

    def run(self):
        # Inicia o jogo
        self._setup_network() # Pergunta se o jogador será servidor ou cliente
        self._main_loop()

    def _setup_network(self):
        # Define se o jogador vai hospedar ou se conectar a um jogo
        is_server = input("Host game? (y/n): ").strip().lower() == 'y'
        self.network.move_received_callback = self.game_state.receive_move # Define função para receber jogadas
        
        if is_server:
            self.network.start_server()
            self.game_state.my_turn = True
            self.game_state.is_black_player = False
        else:
            self.network.connect_to_server()
            self.game_state.my_turn = False
            self.game_state.is_black_player = True

    def _main_loop(self):
        while self.running:
            self.clock.tick(60) # Limita FPS
            self._handle_events()
            self._process_network_messages()
            self._render() # Atualiza renderização do tabuleiro

            if self.game_state.game_over:
                self._handle_game_over() # Se o jogo acabou, exibe tela final

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        # Processa eventos do pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.network.send_move('quit\n')
                self.running = False

            if (event.type == pygame.MOUSEBUTTONDOWN and 
                self.game_state.my_turn and 
                not self.game_state.game_over):
                self._handle_move(event.pos)

    def _handle_move(self, mouse_pos):
        # Processa tentativa de movimento com base no clique do jogador
        square = self.renderer.get_square_from_mouse(mouse_pos, self.game_state.is_black_player)
        piece = self.game_state.board.piece_at(square)

        if self.game_state.selected_square is None:
            if piece is not None and piece.color == self.game_state.board.turn:
                self.game_state.selected_square = square
        else:
            move = chess.Move(self.game_state.selected_square, square)
            if self.game_state.make_move(move): # Tenta fazer o movimento
                self.network.send_move(str(move)) # Envia movimento ao adversário
                if self.game_state.game_over:
                    if "won" in self.game_state.result:
                        self.network.send_game_over("win")
                    elif "lost" in self.game_state.result:
                        self.network.send_game_over("lose")
                    else:
                        self.network.send_game_over("draw")
            self.game_state.selected_square = None

    def _render(self):
        self.renderer.draw_board()
        self.renderer.highlight_moves(self.game_state.board, self.game_state.selected_square, self.game_state.is_black_player)
        self.renderer.draw_pieces(self.game_state.board, self.assets.pieces, self.game_state.is_black_player)
        pygame.display.flip()

    def _process_network_messages(self):
        for msg_type, content in self.network.get_messages():
            if msg_type == 'move':
                self.game_state.receive_move(content)
            elif msg_type == 'game_over':
                self._handle_remote_game_over(content)
            elif msg_type == 'quit':
                self.running = False
                self.game_state.result = "Opponent quit the game."
                self.game_state.game_over = True

    def _handle_game_over(self):
        again_rect = self.renderer.draw_game_over_screen(self.game_state.result)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.send_move('quit')
                    self.running = False
                    return
                
                if (event.type == pygame.MOUSEBUTTONDOWN and 
                    again_rect.collidepoint(pygame.mouse.get_pos())):
                    self.game_state.reset()
                    return
                
    def _handle_remote_game_over(self, result):
        self.game_state.game_over = True
        if result == "win":
            self.game_state.result = "Checkmate! You lost!"
        elif result == "lose":
            self.game_state.result = "Checkmate! You won!"
        else:
            self.game_state.result = "Stalemate!"
        self._handle_game_over()

if __name__ == "__main__":
    game = MainGame()
    game.run()