import socket, threading, chess

# Gerencia a comunicação entre dois jogadores via TCP/IP
class NetworkManager:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.sock = None
        self.receive_thread = None
        self.move_received_callback = None

    def start_server(self):
        # Inicia o socket como servidor aguardando conexão
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print("Waiting for connection...")
        conn, _ = self.sock.accept()
        self.sock = conn
        print("Opponent connected!")
        self._start_receive_thread()

    def connect_to_server(self):
        # Conecta-se ao servidor remoto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("Connected to server!")
        self._start_receive_thread()

    def _start_receive_thread(self):
        self.receive_thread = threading.Thread(target=self._receive_moves, daemon=True)
        self.receive_thread.start()

    def _receive_moves(self):
        # Thread que escuta os dados recebidos do outro jogador
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if data == 'quit':
                    print("Opponent quit.")
                    break
                elif data.startswith('game_over:'):
                    result = data.split(':')[1]
                    if self.game_over_callback:
                        self.game_over_callback(result)
                else:
                    move = chess.Move.from_uci(data)
                    if self.move_received_callback:
                        self.move_received_callback(move)
            except ConnectionError:
                print("Connection lost")
                break

    def send_move(self, move):
        # Envia um movimento ao adversário
        if self.sock:
            self.sock.send(str(move).encode())

    def send_game_over(self, result):
        if self.sock:
            self.sock.send(f'game_over:{result}'.encode())

    def close(self):
        if self.sock:
            self.sock.close()