import socket
import threading


class Server:
    #host = '127.0.0.1'   #---> LocalHost
    #port =  8080

    def __init__(self):
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.bind(('127.0.0.1', 8080))
        self.ss.listen()
        self.dicc = dict()
        print("\n\033[1;35m"+"Welcome to Server"+"\033[0m")

    def broadcast(self, message, c):
        for valor in self.dicc.values():
            if (valor != c):
                valor.send(message)

    def handle(self, username):
        c = self.dicc.get(username)
        while True:
            try:
                #c = self.dicc.get(username)
                message = c.recv(1024)
                if(message.decode('ascii') == 'CLOSE'):
                    print(username+"\033[2;33m"+" S'ha desconnectat"+"\033[0m")
                    #self.broadcast('{} ha marxat!'.format(username).encode('ascii'), c)
                    c.send('CLOSE'.encode('ascii'))
                    c.close()
                else:
                    self.broadcast(message, c)
            except:
                c.close()
                self.broadcast('\n{} ha marxat!\n'.format(
                    username).encode('ascii'), c)
                self.dicc.pop(username)
                break

    def rebre_missatge(self):
        while True:
            c, a = self.ss.accept()
            print("\033[1;35m"+"Connexio nova amb {}".format(str(a))+"\033[0m")
            c.send('USERNAME'.encode('ascii'))
            username = c.recv(1024).decode('ascii')
            self.dicc[username] = c
            print("\033[1;33m"+"Usuari:  {}".format(username))
            self.broadcast("{} s'ha unit al chat!\n".format(
                username).encode('ascii'), c)
            #c.send('Connected to server!\n'.encode('ascii'))
            thread = threading.Thread(target=self.handle, args=(username, ))
            thread.start()

serv=Server()
serv.rebre_missatge()