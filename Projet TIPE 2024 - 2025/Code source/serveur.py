import threading
import socket
import fonctions_utiles as fu
# import algos_chiffrement as algos

class Serveur:
    """ Classe permettant de simuler un serveur informatique simplifié à l'aide du module socket """

    def __init__(self, modele:int, port=6390):
        self.host = ""
        self.port = port
        self.socket = None
        self.clients = []
        self.threads = {}
        self.id_client = 1
        self.arret = False
        self.modele = modele

    def close(self):
        """ Fonction qui vérifie si le serveur doit s'éteindre ou non """
        while True:
            if self.arret == True:
                break

    def connections(self):
        """ Fonction qui gère les connexions au serveur d'éventuels clients en temps réel """
        while True:
            client, ip = self.socket.accept()
            self.clients.append((self.id_client, client, ip))
            # on lance un fil d'exécution pour chaque nouveau client afin de pouvoir recevoir ses messages
            # on choisit la bonne fonction de réception en fonction du modèle utilisé
            if self.modele != 3:
                self.threads[str(self.id_client)] = threading.Thread(target=self.reception, args=[client, self.id_client])
            else:
                self.threads[str(self.id_client)] = threading.Thread(target=self.reception_cm, args=[client, self.id_client])
            self.threads[str(self.id_client)].start()

            print("Le client ", self.id_client, " d'adresse ", ip, " s'est connecté")
            self.id_client += 1

    def transfert(self, expediteur:str, destinataire, message:str, separateur=":"):
        """ Fonction qui transfert un message entre 2 clients """
        new_msg = "<Client-" + expediteur + ">" + separateur + message
        destinataire.send(new_msg.encode("utf-8"))

    def reception(self, client, id_client:int):
        """ Fonction qui réceptionne les requêtes des clients et qui les traite pour les modèles 1 et 2"""
        while True:
            requete_client = client.recv(500)
            requete_client = requete_client.decode("utf-8")
            print("<Client-" + str(id_client) + ">:", requete_client)
            print() # on passe une ligne pour aérer l'affichage
            if requete_client == "/S -close":
                print("CLOSE")
                self.arret = True
            else: # on envoie le message au bon destinataire en fonction de l'expéditeur
                if id_client == 1:
                    self.transfert(str(id_client), self.clients[1][1], requete_client, separateur="|")
                else:
                    self.transfert(str(id_client), self.clients[0][1], requete_client, separateur="|")

    def reception_cm(self, client, id_client:int):
        """ Fonction qui réceptionne les requêtes des clients et qui les traite pour le modèle 3 """
        while True:
            requete_client = client.recv(500)
            requete_client = requete_client.decode("utf-8")
            decomp_msg = fu.decomposition_chaine(requete_client, separateur="|")
            print("<Client-" + str(id_client) + ">:", requete_client)
            print() # on passe une ligne pour aérer l'affichage
            if requete_client == "/S -close":
                print("CLOSE")
                self.arret = True
            elif "/S -check" in requete_client:
                if id_client == 1:
                    destinataire = 1
                else:
                    destinataire = 0
                self.transfert(str(id_client), self.clients[destinataire][1], requete_client, separateur="|")
            elif "/S -init" in requete_client:
                if len(decomp_msg) > 2: # si le client malveillant veut envoyer une clé altérée
                    # on l'envoie au bon destinataire
                    expediteur = decomp_msg[2]
                    destinataire = int(decomp_msg[3]) - 1
                    # on supprime les infos concernant l'expéditeur et le destinataire
                    decomp_msg.pop()
                    decomp_msg.pop()
                    requete_client = fu.compression_arg_str(decomp_msg, separateur="|")
                    self.transfert(expediteur, self.clients[destinataire][1], requete_client, separateur="|")
                else: # sinon c'est la clé d'origine d'un client normal
                    # on envoie donc sa clé au client malveillant
                    self.transfert(str(id_client), self.clients[2][1], requete_client, separateur="|")
            elif id_client != 3: # si le serveur reçoit un message d'un client normal
                # on l'envoit au client malveillant
                self.transfert(str(id_client), self.clients[2][1], requete_client, separateur="|")
            else:
                # on l'envoie au bon destinataire
                expediteur = decomp_msg[4]
                destinataire = int(decomp_msg[5]) - 1
                # on supprime les infos concernant l'expéditeur et le destinataire
                decomp_msg.pop()
                decomp_msg.pop()
                requete_client = fu.compression_arg_str(decomp_msg, separateur="|")
                self.transfert(expediteur, self.clients[destinataire][1], requete_client, separateur="|")

    def run(self):
        """ Fonction qui démarre et ferme le serveur """
        # création du socket pour "démarrer" le serveur
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        print("Le serveur est démarré...")

        self.socket.listen(1) # on le met en mode récepteur

        connections = threading.Thread(target=self.connections, args=[])
        connections.start()

        execution = threading.Thread(target=self.close, args=[])
        execution.start()

        execution.join()

        for client in self.clients:
            client[1].close()
        self.socket.close()
