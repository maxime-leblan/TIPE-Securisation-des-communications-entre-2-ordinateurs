import threading
import socket
import sys
import hashlib
import algos_chiffrement as algos
import fonctions_utiles as fu

class Client_RSA:
    """ Classe permettant de simuler un client pouvant se connecter à un serveur informatique simplifié
    à l'aide du module socket, qui base le chiffrement sur l'algorithme du RSA """

    def __init__(self, id: int, liste_nb_premiers, host="localhost", port=6390):
        self.id = id
        self.host = host
        self.port = port
        self.socket = None
        self.cle_pv_RSA = None
        self.cle_pb_RSA = None
        self.cles_pb_RSA_autres = {}
        self.liste_nb_premiers = liste_nb_premiers
        self.init_envoi = False # permet de savoir si self.initialisation_RSA() a déjà été exécutée dans self.envoyer()
        self.init_recu = False  # permet de savoir si self.initialisation_RSA() a déjà été exécutée dans self.reception()
        # messages envoyés de la forme : "Client_X:taille_msg:message_chiffre"
        # On renomme les indices que l'on utilise dans le code pour pouvoir les modifier plus facilement
        # et pour plus de visibilité
        self.i_client = 0
        self.i_taille_msg = 1
        self.i_msg_chiffre = 2

    def initialisation_RSA(self, message: str, separateur="|"):
        """ Fonction qui crée la clé privée et la clé publique du client pour l'algo de chiffrement RSA.
        Elle est exécutée à l'initialisation de la connection avec le serveur et partage la clé publique du client
        avec un autre client connecté au serveur avec lequel il veut communiquer."""

        cles = algos.creation_cles(self.liste_nb_premiers)
        self.cle_pb_RSA = cles[0]
        self.cle_pv_RSA = cles[1]
        msg = fu.compression_arg_str([self.cle_pb_RSA[0], self.cle_pb_RSA[1]])
        msg = message + separateur + msg

        return msg

    def envoyer(self, socket):
        """ Fonction permettant d'envoyer un message à un client en passant par le serveur """
        try:
            while True:
                msg = input("-->")
                if msg == "/S -init" and not self.init_envoi:
                    socket.send(self.initialisation_RSA(msg).encode("utf-8"))
                    self.init_envoi = True
                elif msg == "/S -close":
                    socket.send(msg.encode("utf-8"))
                else:
                    try:
                        if self.id == 1: # on chiffre le message avec la clé publique du bon client
                            # msg_chiffre = algos.chiffrer_RSA(algos.string_to_int(msg), self.cles_pb_RSA_autres["2"])
                            msg_chiffre = algos.chiffrer_chaine_RSA(msg, self.cles_pb_RSA_autres["2"], taille_facteur=3)
                        else:
                            # msg_chiffre = algos.chiffrer_RSA(algos.string_to_int(msg), self.cles_pb_RSA_autres["1"])
                            msg_chiffre = algos.chiffrer_chaine_RSA(msg, self.cles_pb_RSA_autres["1"], taille_facteur=3)
                        # on transforme le message sous forme de liste en chaine de caractères
                        msg_chiffre = fu.compression_arg_str(msg_chiffre)
                        msg_envoye = str(len(msg)) + "|" + str(msg_chiffre) # on ajoute la longueur du message chiffré au message envoyé
                        msg_envoye = msg_envoye.encode("utf-8")
                        socket.send(msg_envoye)
                    except AssertionError:
                        print("Erreur lors de la tentative de chiffrement du message. Veuillez essayer à nouveau")
        except ConnectionResetError:
            print("Déconnexion du serveur...")
            sys.exit()

    def reception(self, socket):
        """ Fonction qui réceptionne les messages reçus du serveur """
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                # requete_serveur est de la forme : "Client_X:taille_msg:message_chiffre"
                decomp_msg = fu.decomposition_chaine(requete_serveur)
                id_expediteur = fu.id_client(requete_serveur)
                #print("\ndecomp_msg : \n", decomp_msg, "\n")
                #print("\nrequete_serveur : \n", requete_serveur, "\n")

                if "/S -init" in decomp_msg and not self.init_recu: # si on a pas enregistré les clés publiques de l'autre client, on le fait
                    self.cles_pb_RSA_autres[id_expediteur] = fu.extraction_arg_str(decomp_msg[self.i_msg_chiffre])
                    self.init_recu = True
                    # print("\n", requete_serveur)
                    if not self.init_envoi: # si on a pas échangé notre clé publique, on le fait
                        socket.send(self.initialisation_RSA("/S -init").encode("utf-8"))
                        self.init_envoi = True
                else:
                    taille_msg = int(decomp_msg[self.i_taille_msg])
                    # on reconvertit le message chiffré (str) en liste d'entiers pour pouvoir ensuite le déchiffrer
                    msg_chiffre = fu.extraction_arg_str(decomp_msg[self.i_msg_chiffre])
                    # on vérifie qui est l'expéditeur pour prendre sa clé publique correspondante
                    if id_expediteur == 1:
                        # msg_dechiffre = algos.dechiffrer_RSA(int(decomp_msg[2]), self.cle_pv_RSA, self.cle_pb_RSA[0])
                        msg_dechiffre = algos.dechiffrer_chaine_RSA(msg_chiffre, self.cle_pv_RSA, self.cle_pb_RSA[0], taille_entiers=3)
                    else:
                        msg_dechiffre = algos.dechiffrer_chaine_RSA(msg_chiffre, self.cle_pv_RSA, self.cle_pb_RSA[0], taille_entiers=3)
                    print("\n", decomp_msg[self.i_client] + ":" + msg_dechiffre)
                print("\n-->", end="")
        except ConnectionResetError:
            print("Connexion interrompue\nSi le terminal est en attente, appuyez sur Entrée")
            sys.exit()

    def connection(self):
        """ Fonction permettant de connecter le client à un serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        envoi = threading.Thread(target=self.envoyer, args=[self.socket])
        recep = threading.Thread(target=self.reception, args=[self.socket])

        envoi.start()
        recep.start()



class Client_AES_RSA(Client_RSA):
    """ Classe fille de Client_RSA permettant de simuler un client pouvant se connecter à un serveur informatique simplifié
    à l'aide du module socket, qui base le chiffrement sur une combinaison de l'algorithme RSA et AES """

    def __init__(self, id: int, liste_nb_premiers):
        Client_RSA.__init__(self, id, liste_nb_premiers)

        # messages envoyés de la forme : "Client_X|taille_msg|cle_AES|vect_AES|message_chiffre"
        # On renomme les indices que l'on utilise dans le code pour pouvoir les modifier plus facilement
        # et pour plus de visibilité
        self.i_client = 0
        self.i_taille_msg = 1
        self.i_cle_AES = 2
        self.i_vect_AES = 3
        self.i_msg_chiffre = 4

    def envoyer(self, socket):
        """ Fonction permettant d'envoyer un message à un client en passant par le serveur """
        try:
            while True:
                msg = input("-->")
                if msg == "/S -init" and not self.init_envoi:
                    # on envoie notre clé publique à l'autre client
                    socket.send(self.initialisation_RSA(msg, separateur="|").encode("utf-8"))
                    self.init_envoi = True
                elif msg == "/S -close":
                    socket.send(msg.encode("utf-8"))
                elif msg == "/S -check":
                    # on construit le hash de la clé publique de l'expéditeur et on l'envoie à l'autre client
                    cle_pb = str(self.cle_pb_RSA[0]) + "/" + str(self.cle_pb_RSA[1])
                    hash_cle = hashlib.sha256(cle_pb.encode())
                    hash_cle = hash_cle.hexdigest()
                    msg += "|" + hash_cle
                    socket.send(msg.encode())
                else:
                    try:
                        cle_AES = fu.generateur_alea_chaine(32)
                        vecteur_AES = fu.generateur_alea_chaine(16)
                        # si on veut envoyer un msg au client 1, on chiffre avec la clé publique du client 2
                        if self.id == 1:  # on chiffre le message avec la clé publique du bon client
                            destinataire = "2"
                        else: # sinon c'est l'inverse
                            destinataire = "1"

                        # On chiffre le message avec la cle et le vecteur AES
                        msg_chiffre = algos.chiffrer_AES(msg, fu.encode_ascii(cle_AES), fu.encode_ascii(vecteur_AES))
                        msg_chiffre = msg_chiffre.decode("latin-1")

                        # On chiffre la cle et le vecteur pour AES avec le RSA
                        cle_AES = algos.chiffrer_chaine_RSA(cle_AES, self.cles_pb_RSA_autres[destinataire], taille_facteur=4)
                        vecteur_AES = algos.chiffrer_chaine_RSA(vecteur_AES, self.cles_pb_RSA_autres[destinataire], taille_facteur=4)

                        # on transforme le message, la clé et le vecteur sous forme de liste en chaine de caractères
                        msg_chiffre = fu.compression_arg_str([msg_chiffre])
                        cle_AES = fu.compression_arg_str(cle_AES)
                        vecteur_AES = fu.compression_arg_str(vecteur_AES)

                        # On construit le message que l'on va envoyer contenant toutes les infos nécessaires pour le destinataire
                        msg_envoye = str(len(msg)) + "|" + cle_AES + "|" + vecteur_AES + "|" + msg_chiffre
                        msg_envoye = msg_envoye.encode("utf-8")
                        socket.send(msg_envoye)
                    except AssertionError:
                        print("Erreur lors de la tentative de chiffrement du message. Veuillez essayer à nouveau")
        except ConnectionResetError:
            print("Déconnexion du serveur...")
            sys.exit()

    def reception(self, socket):
        """ Fonction qui réceptionne les messages reçus du serveur """
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                decomp_msg = fu.decomposition_chaine(requete_serveur, separateur="|")
                id_expediteur = fu.id_client(requete_serveur)
                # print("\ndecomp_msg : \n", decomp_msg, "\n")
                # print("\nrequete_serveur : \n", requete_serveur, "\n")
                # print("init_recu : ", self.init_recu)
                # print("condition if : ", ("/S -init" in decomp_msg and not self.init_recu))

                if "/S -init" in decomp_msg and not self.init_recu:  # si on a pas enregistré les clés publiques de l'autre client, on le fait
                    # print("dans le init ==================\n\n")
                    self.cles_pb_RSA_autres[id_expediteur] = fu.extraction_arg_str(decomp_msg[2])
                    self.init_recu = True
                    # print("\n", requete_serveur)
                    if not self.init_envoi:  # si on a pas échangé notre clé publique, on le fait
                        socket.send(self.initialisation_RSA("/S -init", separateur="|").encode("utf-8"))
                        self.init_envoi = True
                elif "/S -check" in requete_serveur:
                    print("\nComparaison des clés en cours...")
                    # on construit le hash de la clé de l'autre client à partir de notre base de donnée
                    cle_pb = str(self.cles_pb_RSA_autres[id_expediteur][0]) + "/" + str(self.cles_pb_RSA_autres[id_expediteur][1])
                    hash_cle = hashlib.sha256(cle_pb.encode())
                    hash_cle = hash_cle.hexdigest()
                    # on récupère le hash envoyé par l'autre client
                    hash_autre_cle = decomp_msg[-1]
                    if hash_autre_cle != hash_cle:
                        print("La communication n'est plus sécurisée /!\ ")
                    else:
                        print("La communication est sécurisée")
                else:
                    # On extrait et déchiffre la clé et le vecteur AES
                    cle_AES = fu.extraction_arg_str(decomp_msg[self.i_cle_AES])
                    cle_AES = algos.dechiffrer_chaine_RSA(cle_AES, self.cle_pv_RSA, self.cle_pb_RSA[0], taille_entiers=4)
                    vecteur_AES = fu.extraction_arg_str(decomp_msg[self.i_vect_AES])
                    vecteur_AES = algos.dechiffrer_chaine_RSA(vecteur_AES, self.cle_pv_RSA, self.cle_pb_RSA[0], taille_entiers=4)

                    # on récupère le message chiffré et on le déchiffre
                    msg_chiffre = decomp_msg[self.i_msg_chiffre]
                    msg_chiffre = msg_chiffre.encode("latin-1")
                    msg_dechiffre = algos.dechiffrer_AES(msg_chiffre, fu.encode_ascii(cle_AES), fu.encode_ascii(vecteur_AES))
                    print("\n", decomp_msg[self.i_client] + ":" + msg_dechiffre)
                print("\n-->", end="")
        except ConnectionResetError:
            print("Connexion interrompue\nSi le terminal est en attente, appuyez sur Entrée")
            sys.exit()






class ClientMalveillant(Client_AES_RSA):
    """ Classe fille de la classe Client_AES_RSA qui initialise le client malveillant voulant lire des conversations
    sécurisées entre les autres clients connectés au même serveur, dans le cadre du modèle n°3 avec la fonction
     de hachage et le canal secret"""

    def __init__(self, id: int, liste_nb_premiers):
        Client_AES_RSA.__init__(self, id, liste_nb_premiers)

        # Compteur indiquant le nombre d'échanges de clés que le Client Malveillant a effectué avec
        # les autres clients
        self.nb_cles_echangees = 0

    def initialisation_RSA(self, message: str, separateur="|", expediteur="", destinataire=""):
        """ Fonction qui crée la clé privée et la clé publique du client pour l'algo de chiffrement RSA.
        Elle est exécutée à l'initialisation de la connection avec le serveur et partage la clé publique du client
        avec un autre client connecté au serveur avec lequel il veut communiquer."""
        if self.cle_pv_RSA == None: # si on a pas encore créé nos clés, on le fait
            cles = algos.creation_cles(self.liste_nb_premiers)
            self.cle_pb_RSA = cles[0]
            self.cle_pv_RSA = cles[1]
        msg = fu.compression_arg_str([self.cle_pb_RSA[0], self.cle_pb_RSA[1]])
        print("clé envoyée : ", msg)
        msg = fu.compression_arg_str([msg, expediteur, destinataire], separateur="|")
        msg = message + separateur + msg

        return msg

    def reception(self, socket):
        """ Fonction qui réceptionne les messages reçus du serveur """
        try:
            while True:
                requete_serveur = socket.recv(500)
                requete_serveur = requete_serveur.decode("utf-8")
                decomp_msg = fu.decomposition_chaine(requete_serveur, separateur="|")
                id_expediteur = fu.id_client(requete_serveur)
                # print("\ndecomp_msg : \n", decomp_msg, "\n")
                # print("\nrequete_serveur : \n", requete_serveur, "\n")
                # print("init_recu : ", self.init_recu)
                # print("condition if : ", ("/S -init" in decomp_msg and not self.init_recu))

                if "/S -init" in decomp_msg:  # si on reçoit une clé publique, on l'enregistre
                    # print("dans le init ==================\n\n")
                    self.cles_pb_RSA_autres[id_expediteur] = fu.extraction_arg_str(decomp_msg[2])
                    # print("\n", requete_serveur)
                    print("clé reçue : ", fu.extraction_arg_str(decomp_msg[2]))
                    # on envoie notre propre clé publique au bon destinataire
                    if id_expediteur == "1":
                        socket.send(self.initialisation_RSA("/S -init", separateur="|", expediteur=id_expediteur, destinataire="2").encode("utf-8"))
                    else:
                        socket.send(self.initialisation_RSA("/S -init", separateur="|", expediteur=id_expediteur, destinataire="1").encode("utf-8"))
                else:
                    # On extrait et déchiffre la clé et le vecteur AES
                    cle_AES = fu.extraction_arg_str(decomp_msg[self.i_cle_AES])
                    cle_AES = algos.dechiffrer_chaine_RSA(cle_AES, self.cle_pv_RSA, self.cle_pb_RSA[0], taille_entiers=4)
                    vecteur_AES = fu.extraction_arg_str(decomp_msg[self.i_vect_AES])
                    vecteur_AES = algos.dechiffrer_chaine_RSA(vecteur_AES, self.cle_pv_RSA, self.cle_pb_RSA[0], taille_entiers=4)

                    # on récupère le message chiffré et on le déchiffre
                    msg_chiffre = decomp_msg[self.i_msg_chiffre]
                    msg_chiffre = msg_chiffre.encode("latin-1")
                    msg_dechiffre = algos.dechiffrer_AES(msg_chiffre, fu.encode_ascii(cle_AES), fu.encode_ascii(vecteur_AES))
                    print("\n", decomp_msg[self.i_client] + ":" + msg_dechiffre)

                    # on renvoie le message au destinataire chiffré avec la clé publique du destinataire
                    # si on veut envoyer un msg au client 1, on chiffre avec la clé publique du client 2
                    if id_expediteur == "1":  # on chiffre le message avec la clé publique du bon client
                        destinataire = "2"
                    else:  # sinon c'est l'inverse
                        destinataire = "1"

                    # On chiffre le message avec la cle et le vecteur AES
                    msg_chiffre = algos.chiffrer_AES(msg_dechiffre, fu.encode_ascii(cle_AES), fu.encode_ascii(vecteur_AES))
                    msg_chiffre = msg_chiffre.decode("latin-1")

                    # On chiffre la cle et le vecteur pour AES avec le RSA
                    cle_AES = algos.chiffrer_chaine_RSA(cle_AES, self.cles_pb_RSA_autres[destinataire],
                                                        taille_facteur=4)
                    vecteur_AES = algos.chiffrer_chaine_RSA(vecteur_AES, self.cles_pb_RSA_autres[destinataire],
                                                            taille_facteur=4)

                    # on transforme le message, la clé et le vecteur sous forme de liste en chaine de caractères
                    msg_chiffre = fu.compression_arg_str([msg_chiffre])
                    cle_AES = fu.compression_arg_str(cle_AES)
                    vecteur_AES = fu.compression_arg_str(vecteur_AES)

                    # On construit le message que l'on va envoyer contenant toutes les infos nécessaires pour le destinataire
                    msg_envoye = str(len(msg_dechiffre)) + "|" + cle_AES + "|" + vecteur_AES + "|" + msg_chiffre + "|" + id_expediteur + "|" + destinataire
                    msg_envoye = msg_envoye.encode("utf-8")
                    socket.send(msg_envoye)
        except ConnectionResetError:
            print("Connexion interrompue\nSi le terminal est en attente, appuyez sur Entrée")
            sys.exit()

    def connection(self):
        """ Fonction permettant de connecter le client à un serveur """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        recep = threading.Thread(target=self.reception, args=[self.socket])

        recep.start()