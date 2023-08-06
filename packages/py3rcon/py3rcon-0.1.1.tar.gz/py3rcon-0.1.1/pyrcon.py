import socket

class RCON:

    def __init__(self, ip, password, port=27960):
        self.ip = ip
        self.port = port
        self.password = password
        self.prefix = bytes([0xff, 0xff, 0xff, 0xff]) + b'rcon '
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, command, response=False):

        cmd = f"{self.password} {command}".encode()
        query = self.prefix + cmd
        
        self.socket.connect((self.ip, self.port))
        self.socket.send(query)

        if response:
            data = self.socket.recv(4096)
            return data

if __name__ == "__main__":
    rcon = RCON('127.0.0.1', "secret")
    
    # No-response command.
    rcon.send_command("say Hello, world!")

    # If you need a response.
    response = rcon.send_command("status", response=True)
    print(response)
