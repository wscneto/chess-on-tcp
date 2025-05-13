import socket, threading, chess, queue

# Gerencia a comunicação entre dois jogadores via TCP/IP
class NetworkManager:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.sock = None
        self.receive_thread = None
        self.message_queue = queue.Queue()

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
        buffer = ""
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                    
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.startswith("move:"):
                        move_str = line[5:]
                        try:
                            move = chess.Move.from_uci(move_str)
                            self.message_queue.put(('move', move))
                        except chess.InvalidMoveError:
                            print(f"Invalid move received: {move_str}")
                    elif line.startswith("game_over:"):
                        result = line[10:]
                        self.message_queue.put(('game_over', result))
                    elif line == "quit":
                        print("Opponent quit.")
                        return
                    else:
                        print(f"Unknown message: {line}")
                        
            except ConnectionError:
                print("Connection lost")
                break
    
    def get_messages(self):
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages

    def send_move(self, move):
        # Envia um movimento ao adversário
        if self.sock:
            self.sock.sendall(f"move:{move}\n".encode())

    def send_game_over(self, result):
        if self.sock:
            self.sock.sendall(f"game_over:{result}\n".encode())

    def close(self):
        if self.sock:
            self.sock.close()