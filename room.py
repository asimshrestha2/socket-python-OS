#class holds 
class Room:
    def __init__(self, sockets):
        self.sockets = sockets

    def exitRoom(self):
        for socket in sockets:
            socket.close();
        
