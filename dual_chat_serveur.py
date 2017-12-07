#!/usr/bin/python3.6
#-*-coding=Utf8-*-

import threading, socket, sys
"""dual chat est un chat qui permet aux clients qui se connectent en 1er et 2 eme, 3eme et 4eme, 
5 eme et 6eme (ect..) de parler en tete à tete, dans l'idée ensuite de faire un jeu de bataille"""

"""je commence par creer un chat simple en version graphique"""

class ThreadClient(threading.Thread):
    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion
    def run(self):
        nom = self.getName()
        while True:
            messClient = self.connexion.recv(1024).decode("Utf8")
            messClient = messClient.split(', ')
            if messClient[1] == "jemedeco!":
                mess = "serveur, vousetesdeconnecté!"
                self.connexion.send(mess.encode("Utf8"))
                break
            elif messClient[1] == "getJoueursConnectes":
                mess = "serveur, test get joueurs co!"
                self.connexion.send(mess.encode("Utf8"))
            print(messClient)
            for client in conn_client:
                if client != nom:
                    print("reexpedition message :  " + messClient[0] + ", " + messClient[1])
                    conn_client[client].send(messClient.encode("Utf8"))
        self.connexion.close()
        del conn_client[nom]
        print("Client %s deconnecte." % nom)

HOST = '127.0.0.1'
PORT = 50001

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a echoué")
    sys.exit()
print("serveur prêt, en attente de requêtes")
mySocket.listen(5)

conn_client = {} 
while True:
    """boucle et attend un nouveau client à chaque cycle"""
    connexion, adresse = mySocket.accept()
    th = ThreadClient(connexion)
    th.start()
    it = th.getName() # identifiant du thread
    conn_client[it] = connexion
    print("Client %s connecté, adresse IP %s, port %s."% (it, adresse[0], adresse[1]))