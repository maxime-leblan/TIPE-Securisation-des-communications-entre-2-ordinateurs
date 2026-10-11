import threading
import socket
import sys
import algos_chiffrement as algos

class Client:
    """ Classe permettant de simuler un client pouvant se connecter à un serveur informatique simplifié
    à l'aide du module socket """

    def __init__(self, host="localhost", port=6390):
        self.host = host
        self.port = port
        self.socket = None
        self.cle_vigenere = "cle"

    def envoyer_cesar(self, socket):
        """ Fonction permettant d'envoyer un message à un client en passant par le serveur """
        try:
            while True:
                msg = input("-->")
                msg_chiffre = algos.code_cesar("chiffrer", msg, 34)
                msg_chiffre = msg_chiffre.encode("utf-8")
                socket.send(msg_chiffre)
        except ConnectionResetError:
            print("Déconnexion du serveur...")
            sys.exit()

    def envoyer_vigenere(self, socket):
        """ Fonction permettant d'envoyer un message à un client en passant par le serveur """
        try:
            while True:
                msg = input("-->")
                msg_chiffre = algos.chiffre_vigenere("chiffrer", msg, self.cle_vigenere)
                msg_chiffre = msg_chiffre.encode("utf-8")
                socket.send(msg_chiffre)
        except ConnectionResetError:
            print("Déconnexion du serveur...")
            sys.exit()

    def reception_cesar(self, socket):
        """ Fonction qui réceptionne les messages reçus du serveur """
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                info_expediteur = ""
                msg_dechiffre = ""
                fin_info = False

                for lettre in requete_serveur:
                    if lettre != ":" and not fin_info:
                        info_expediteur = info_expediteur + lettre
                    elif lettre == ":" and not fin_info:
                        info_expediteur = info_expediteur + lettre
                        fin_info = True
                    else:
                        msg_dechiffre = msg_dechiffre + lettre


                msg_dechiffre = algos.code_cesar("dechiffrer", msg_dechiffre, 34)
                print("\n", info_expediteur + msg_dechiffre)
                print("\n-->", end="")
        except ConnectionResetError:
            print("Connexion interrompue\nSi le terminal est en attente, appuyez sur Entrée")
            sys.exit()

    def reception_vigenere(self, socket):
        """ Fonction qui réceptionne les messages reçus du serveur """
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                info_expediteur = ""
                msg_dechiffre = ""
                fin_info = False

                for lettre in requete_serveur:
                    if lettre != ":" and not fin_info:
                        info_expediteur = info_expediteur + lettre
                    elif lettre == ":" and not fin_info:
                        info_expediteur = info_expediteur + lettre
                        fin_info = True
                    else:
                        msg_dechiffre = msg_dechiffre + lettre


                msg_dechiffre = algos.chiffre_vigenere("dechiffrer", msg_dechiffre, self.cle_vigenere)
                print("\n", info_expediteur + msg_dechiffre)
                print("\n-->", end="")
        except ConnectionResetError:
            print("Connexion interrompue\nSi le terminal est en attente, appuyez sur Entrée")
            sys.exit()

    def connection_cesar(self):
        """ Fonction permettant de connecter le client à un serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        envoi = threading.Thread(target=self.envoyer_cesar, args=[self.socket])
        recep = threading.Thread(target=self.reception_cesar, args=[self.socket])

        envoi.start()
        recep.start()

    def connection_vigenere(self):
        """ Fonction permettant de connecter le client à un serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        envoi = threading.Thread(target=self.envoyer_vigenere, args=[self.socket])
        recep = threading.Thread(target=self.reception_vigenere, args=[self.socket])

        envoi.start()
        recep.start()

class ClientMalveillant(Client):
    """ Classe fille de la classe Client qui initialise le client malveillant voulant lire des conversations
    sécurisées entre les autres clients connectés au même serveur """

    def __init__(self):
        Client.__init__(self)

    def reception_decryptee_cesar(self, socket):
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                dico_msg_clair = algos.code_cesar_force_brute(requete_serveur)
                print("\nMessage chiffré : ", requete_serveur, "\n\n")
                algos.afficher_solutions_potentielles(dico_msg_clair)
        except ConnectionResetError:
            print("Déconnexion du serveur...")
            sys.exit()

    def reception_decryptee_vigenere(self, socket):
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                msg_clair = algos.chiffre_vigenere_friedman(requete_serveur)
                print("\nMessage chiffré : ", requete_serveur, "\n\n")
                print("\nMessage clair : ", msg_clair, "\n\n")
        except ConnectionResetError:
            print("Déconnexion du serveur...")
            sys.exit()

    def connection_cesar(self):
        """ Fonction permettant de connecter le client à un serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # recep = threading.Thread(target=self.reception, args=[self.socket])
        recep_decrypte = threading.Thread(target=self.reception_decryptee_cesar, args=[self.socket])

        # recep.start()
        recep_decrypte.start()

    def connection_vigenere(self):
        """ Fonction permettant de connecter le client à un serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # recep = threading.Thread(target=self.reception, args=[self.socket])
        recep_decrypte = threading.Thread(target=self.reception_decryptee_vigenere, args=[self.socket])

        # recep.start()
        recep_decrypte.start()