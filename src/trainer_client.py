"""Cliente UDP mínimo para preparar episodios en rcssserver."""

import math
import socket


class TrainerClient:
    """Conecta al puerto del trainer y envía comandos oficiales de escenario."""

    def __init__(self, host="127.0.0.1", port=6001, timeout=2.0):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.server_addr = (host, port)
        self.connected = False

    def connect(self, version=15):
        self.sock.sendto(
            f"(init (version {version}))\x00".encode("ascii"), self.server_addr
        )
        reply, self.server_addr = self.sock.recvfrom(8192)
        response = reply.decode("latin1").strip("\x00 \r\n")
        if not response.startswith("(init ok)"):
            raise RuntimeError(f"Respuesta inesperada del trainer: {response}")
        self.connected = True
        return response

    def send_command(self, command):
        if not self.connected:
            raise RuntimeError("Conecta el trainer antes de enviar comandos")
        self.sock.sendto(f"{command}\x00".encode("ascii"), self.server_addr)

    def move_ball(self, x, y):
        if not all(math.isfinite(value) for value in (x, y)) or not (
            -52 <= x <= 52 and -32 <= y <= 32
        ):
            raise ValueError("El balón debe ubicarse dentro de x=[-52,52], y=[-32,32]")
        self.send_command(f"(move (ball) {x:.2f} {y:.2f})")

    def change_mode(self, mode):
        if mode not in {"before_kick_off", "play_on"}:
            raise ValueError("Modo permitido: before_kick_off o play_on")
        self.send_command(f"(change_mode {mode})")

    def close(self):
        self.sock.close()
        self.connected = False
