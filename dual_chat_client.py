#!/usr/bin/python3.6
#-*-coding=Utf8-*-

import threading, socket, sys, time
from tkinter import *

class ThreadActualiserListeJoueursConnectes(threading.Thread):
    def __init__(self, emission, fenetre):
        threading.Thread.__init__(self)
        self.emission = emission
        self.fenetre = fenetre
    def run(self):
        while True:
            print(self.fenetre.pseudo)
            self.emission.emmetre(self.fenetre.pseudo + ", getJoueursConnectes")
            time.sleep(3)

class Fenetre(Frame):
    def __init__(self, emission):
        Frame.__init__(self, height=400, width=400)
        self.emission = emission

        self.bind('<Destroy>', self.fermerThreads)
        self.labelPseudo = Label(self, text="rentrer votre pseudo : ")
        self.labelPseudo.pack(side=TOP)
        self.saisiePseudo = Entry(self, width=25)
        self.saisiePseudo.bind('<Return>', self.validerPseudo)
        self.saisiePseudo.pack(side=BOTTOM)
        self.conversation = Text(self)
        self.conversation.pack(side=RIGHT)
        self.connectes = Text(self)
        self.connectes.pack(side=LEFT)
        self.pack()
        self.pseudo = ""
        
    def validerPseudo(self, event):
        self.pseudo = self.saisiePseudo.get()
        self.labelPseudo.destroy()
        Label(self, text="vous : " + self.pseudo).pack(side=TOP)
        self.saisiePseudo.destroy()
        self.saisieMess = Entry(self, width=50)
        self.saisieMess.bind('<Return>', self.envoyerMess)
        self.saisieMess.pack(side=BOTTOM)
       # taljc = ThreadActualiserListeJoueursConnectes(self.emission, self)
       # taljc.start()
    def fermerThreads(self, event):
        self.emission.emmetre(self.pseudo + ", jemedeco!")
        print("fermeture threads")
        tf.stop()
        tr.stop()
        taljc.stop()
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
            print(reception)
            reception = reception.split(', ')
            if reception[0] == "serveur":
                if reception[1] == "vousetesdeconnecté!":
                    break
                elif reception[1] == "test get joueurs co!":
                    print("test get joueurs co!")
                    
            print("attente d'un message")
            
            self.fenetre.conversation.insert(INSERT, "\n" + reception[0] + ">>" + reception[1])
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