import threading
import socket
import algos_chiffrement as algos

class Serveur:
    """ Classe permettant de simuler un serveur informatique simplifié à l'aide du module socket """

    def __init__(self, port=6390):
        self.host = ""
        self.port = port
        self.socket = None
        self.clients = []
        self.threads = {}
        self.id_client = 1
        self.arret = False
        self.cle_vigenere = "cle"

    def close(self):
        """ Fonction qui vérifie si le serveur doit s'éteindre ou non """
        while True:
            if self.arret == True:
                break

    def connections_cesar(self):
        """ Fonction qui gère les connexions au serveur d'éventuels clients en temps réel """
        while True:
            client, ip = self.socket.accept()
            self.clients.append((self.id_client, client, ip))
            self.threads[str(self.id_client)] = threading.Thread(target=self.reception_cesar, args=[client, self.id_client])
            self.threads[str(self.id_client)].start()

            print("Le client ", self.id_client, " d'adresse ", ip, " s'est connecté")
            self.id_client += 1

    def connections_vigenere(self):
        """ Fonction qui gère les connexions au serveur d'éventuels clients en temps réel """
        while True:
            client, ip = self.socket.accept()
            self.clients.append((self.id_client, client, ip))
            self.threads[str(self.id_client)] = threading.Thread(target=self.reception_vigenere, args=[client, self.id_client])
            self.threads[str(self.id_client)].start()

            print("Le client ", self.id_client, " d'adresse ", ip, " s'est connecté")
            self.id_client += 1

    def transfert(self, expediteur:str, destinataire, message:str):
        """ Fonction qui transfert un message entre 2 clients """
        new_msg = "<Client-" + expediteur + ">: " + message
        destinataire.send(new_msg.encode("utf-8"))

    def reception_cesar(self, client, id_client:int):
        """ Fonction qui réceptionne les requêtes des clients et qui les traite """
        while True:
            requete_client = client.recv(500)
            requete_client = requete_client.decode("utf-8")
            print("<Client-" + str(id_client) + ">:", requete_client)
            if algos.code_cesar("dechiffrer", requete_client, 34) == "S close":
                print("CLOSE")
                self.arret = True
            elif id_client == 1:
                self.transfert(str(id_client), self.clients[1][1], requete_client)
            else:
                self.transfert(str(id_client), self.clients[0][1], requete_client)
            self.clients[2][1].send(requete_client.encode("utf-8"))

    def reception_vigenere(self, client, id_client:int):
        """ Fonction qui réceptionne les requêtes des clients et qui les traite """
        while True:
            requete_client = client.recv(500)
            requete_client = requete_client.decode("utf-8")
            print("<Client-" + str(id_client) + ">:", requete_client)
            if algos.chiffre_vigenere("dechiffrer", requete_client, self.cle_vigenere) == "S close":
                print("CLOSE")
                self.arret = True
            elif id_client == 1:
                self.transfert(str(id_client), self.clients[1][1], requete_client)
            else:
                self.transfert(str(id_client), self.clients[0][1], requete_client)
            self.clients[2][1].send(requete_client.encode("utf-8"))

    def run_cesar(self):
        """ Fonction qui démarre et ferme le serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        print("Le serveur est démarré...")

        self.socket.listen(1)

        connections = threading.Thread(target=self.connections_cesar, args=[])
        connections.start()

        execution = threading.Thread(target=self.close, args=[])
        execution.start()

        execution.join()

        for client in self.clients:
            client[1].close()
        self.socket.close()

    def run_vigenere(self):
        """ Fonction qui démarre et ferme le serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        print("Le serveur est démarré...")

        self.socket.listen(1)

        connections = threading.Thread(target=self.connections_vigenere, args=[])
        connections.start()

        execution = threading.Thread(target=self.close, args=[])
        execution.start()

        execution.join()

        for client in self.clients:
            client[1].close()
        self.socket.close()