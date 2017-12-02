#!/usr/bin/python3.6
#-*-coding=Utf8-*-

import threading, socket, sys
from tkinter import *

class Fenetre(Frame):
    def __init__(self, emission):
        Frame.__init__(self, height=400, width=400)
        self.emission = emission

        self.bind('<Destroy>', self.fermerThreads)
        self.labelPseudo = Label(self, text="rentrer votre pseudo : ")
        self.labelPseudo.pack(side=TOP)
        self.saisiePseudo = Entry(self, width=25)
        self.saisiePseudo.bind('<Return>', self.validerPSeudo)
        self.saisiePseudo.pack(side=BOTTOM)
        self.conversation = Text(self)
        self.conversation.pack()
        self.pack()
    def validerPSeudo(self, event):
        self.pseudo = self.saisiePseudo.get()
        self.labelPseudo.destroy()
        Label(self, text="vous : " + self.pseudo).pack(side=TOP)
        self.saisiePseudo.destroy()
        self.saisieMess = Entry(self, width=50)
        self.saisieMess.bind('<Return>', self.envoyerMess)
        self.saisieMess.pack(side=BOTTOM)
    def fermerThreads(self, event):
        self.emission.emmetre("jemedeco!")
        print("fermeture threads")
        tf.stop()
        tr.stop()
    def envoyerMess(self, event):
        message = str(self.pseudo) + ", " + str(self.saisieMess.get())
        self.emission.emmetre(message)
        self.conversation.insert(INSERT, "\nvous>>" + str(self.saisieMess.get()))
        self.saisieMess.delete(0, END)
        
class ThreadFenetre(threading.Thread):
    def __init__(self, emission):
        threading.Thread.__init__(self)
        self.emission = emission
        
    def run(self):
        self.fenetre = Fenetre(self.emission)
        tr = ThreadReception(connexion, self.fenetre)
        tr.start()
        self.fenetre.mainloop()
        
class ThreadReception(threading.Thread):
    def __init__(self, connexion, fenetre):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.fenetre = fenetre
    def run(self):
        while True:
            reception = self.connexion.recv(1024).decode("Utf8")
            if reception == "serveur, vousetesdeconnecté!":
                break
            message_recu = reception.split(", ")
            #if message_recu[1] == "vousetesdeconnecté!" and message_recu[0] == "serveur":
            #    break
            print("attente d'un message")
            
            self.fenetre.conversation.insert(INSERT, "\n" + message_recu[0] + ">>" + message_recu[1])
# arreter des threads
        print("client arrete. Connexion interrompue")
        self.connexion.close()
class Emission:
    def __init__(self, connexion):
        self.connexion = connexion
    def emmetre(self, message):
        print(" emission : " + message)
        self.connexion.send(message.encode("utf8"))

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 50001

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host,port))
        emission = Emission(connexion)
        tf = ThreadFenetre(emission)
        tf.start()
        
    except socket.error:
        print("la connexion a echoue")		
        sys.exit()
    print("connexion établie avec le serveur")