from email import message
import random
import socket
import threading
from tokenize import String


class Client:
    username = str
    sc = socket
    bye = str

    def __init__(self, username):
        self.username = username
        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # --->El server sempre serà el localHost
        self.sc.connect(('127.0.0.1', 8080))
        self.bye = "adeu"
        

    def rebre_missatge(self):
        while True:
            try:
                missatge = self.sc.recv(1024).decode('ascii')
                #print(missatge)
                if missatge == 'CLOSE':
                    print("\033[1;31m"+"Conexió tancada"+"\033[0m")
                    self.sc.close()
                    break
                if missatge == 'USERNAME':
                    self.sc.send(self.username.encode('ascii'))
                else:
                    print(missatge)
            except Exception as e:
                print(e)
                print("\033[2;31m"+"Hi ha hagut algun error"+"\033[0m")
                self.sc.close()
                break

    def enviar_missatge(self):
        while True:
            #missatge = '{}: {}'.format(self.username, input(''))
            missatge = input()
            if(missatge == self.bye):
                print("\n\033[6;31m"+"Tancant conexió..."+"\033[0m")
                self.sc.send('CLOSE'.encode('ascii'))
                #self.sc.close()
                quit()
            else:
                missatge_f = "\033[1;36m"+self.username+": "+"\033[3;33m"+missatge+"\033[0m"
                self.sc.send(missatge_f.encode('ascii'))


username = input("\n\033[1;35m"+"Escriu el teu nom d'usuari: "+"\033[0m")
username = username + str(random.randrange(9)) + \
    str(random.randrange(9)) + str(random.randrange(9))
print("\033[1;37m"+"Usuari: "+"\033[1;34m"+username+"\033[0m\n")
# codigo ansi, [formato ;color, m finalizacion       cerrar codigo ansi 
mysc = Client(username)

receive_thread = threading.Thread(target=mysc.rebre_missatge)
receive_thread.start()
write_thread = threading.Thread(target=mysc.enviar_missatge)
write_thread.start()

    

