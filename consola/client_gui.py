from email import message
import random
import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import Sizegrip
from tokenize import String



sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # --->El server sempre serà el localHost
sc.connect(('127.0.0.1', 8080))
bye = "adeu"

    
consola= Tk()
consola.withdraw() #esconder la consola
username = simpledialog.askstring("Usuari", "Escriu el teu nom d'usuari:") + str(
    random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9))
consola.deiconify() #aparecer la consola
consola.title(" PyChat_UPC: ")
consola.config(bg='#EEE8AA') #color de fondo
consola.resizable(True, True)
consola.columnconfigure(0, weight=1)
consola.rowconfigure(0, weight=1)

# create the sizegrip


welcom_msg = " El teu usuari sera: "+username
contenedor1 = Label(consola, text=welcom_msg, font=(
    'Times', 20))
#contenedor1.configure(background='magenta') 
#contenedor1.configure(background='blue')



txtMessages = Text(consola, width=50)
txtMessages.grid(row=0, column=0, padx=10, pady=10)
txtMessages.configure(fg='blue')

txtMessages.insert(END, "\n"+welcom_msg)
# create a scroll bar
scroll = Scrollbar(consola, orient=VERTICAL)
scroll.grid(row=0, column=1, sticky=NS)

# place the scroll bar
# into the gui window
txtMessages.config(yscrollcommand=scroll.set)
scroll.config(command=txtMessages.yview)

txtMessages.config(state=DISABLED)

txtYourMessage = Entry(consola, width=50) 
txtYourMessage.grid(row=1, column=0, padx=30, pady=30)



        
def rebre_missatge():
    while True:
        try:

            missatge = sc.recv(1024).decode('ascii')
            #print(missatge)
            if missatge == 'CLOSE':
                print(" closing")
                sc.close()
                break
            if missatge == 'USERNAME':
                sc.send(username.encode('ascii'))
                
            else:
                txtMessages.configure(state=NORMAL)
                print(missatge) 
                txtMessages.insert(END, "\n "+missatge)
                txtMessages.configure(state=DISABLED)
                txtMessages.see(END)         
        except Exception as e:
            print(" Hi ha hagut algun error")
            sc.close()
            break
        
        


def enviar_missatge():
    #while True:
        txtMessages.configure(state=NORMAL)
        #missatge = '{}: {}'.format(self.username, input(''))
        missatge = txtYourMessage.get()
        txtYourMessage.delete(0, END) #para q desaparezca el mensaje al enviar
        
        if(missatge ==""):
            print("Connected to server")
        elif(missatge == "adeu" or missatge == "adios" or missatge == "exit"):
            print("\n")
            txtMessages.insert(END, "\n" + " You: sending close, ")
            sc.send('CLOSE'.encode('ascii'))
            #self.sc.close()
            quit()
        else:
            missatge_f = '{}: {}'.format(username, missatge)
            txtMessages.insert(END, "\n" + " You: " + missatge)
            sc.send(missatge_f.encode('ascii'))
        txtMessages.configure(state=DISABLED)
            
def enviar_missatgegui(event):
    enviar_missatge()
        

txtYourMessage.bind('<Return>', enviar_missatgegui)       

boto = Button(consola, text="Envia", width=20, command=enviar_missatge, fg='green', bg='yellow')
boto.grid(row=2, column=0, padx=10, pady=10)


receive_thread = threading.Thread(target=rebre_missatge)
receive_thread.daemon = True
receive_thread.start()

write_thread = threading.Thread(target=enviar_missatge)
write_thread.daemon = True
write_thread.start()


consola.mainloop()





