#####################################################################################################################
# Fichier : algos_chiffrement.py
# ==> Contient les fonctions d'algorithmes permettants de sécuriser les communications
#####################################################################################################################

# Imoportation des modules nécessaires
import random as rd
import time
import fonctions_utiles as fu
# Modules nécessaires pour l'implémentation d'AES avec des bibliothèques
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Déclaration des variables globales utiles
liste_nb_premiers1 = [ 2, 3, 5, 7, 11, 13]
liste_nb_premiers2 = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
liste_nb_premiers3 = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                       101,	103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                       179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                       283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                       419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
                       547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
                       661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
                       811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
                       947, 953, 967, 971, 977, 983, 991, 997]

# création de la liste des nombres premiers inférieurs à 1 000 000
# print("Création liste_nb_premiers4")
liste_nb_premiers4 = fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt")

# print("Fin création liste_nb_premiers4")
"""
dico_char_a_int = {" ": 0}
liste_int_a_char = " "

for l in range(97, 123):
    dico_char_a_int[chr(l)] = l - 96
    liste_int_a_char += chr(l)
"""

dico_char_a_int = {}
liste_int_a_char = ""

for l in range(32, 127):
    dico_char_a_int[chr(l)] = l - 32
    liste_int_a_char += chr(l)

# création matrice GF
MATRICE_GF = """00 01 8D F6 CB 52 7B D1 E8 4F 29 C0 B0 E1 E5 C7
                74 B4 AA 4B 99 2B 60 5F 58 3F FD CC FF 40 EE B2
                3A 6E 5A F1 55 4D A8 C9 C1 0A 98 15 30 44 A2 C2
                2C 45 92 6C F3 39 66 42 F2 35 20 6F 77 BB 59 19
                1D FE 37 67 2D 31 F5 69 A7 64 AB 13 54 25 E9 09
                ED 5C 05 CA 4C 24 87 BF 18 3E 22 F0 51 EC 61 17
                16 5E AF D3 49 A6 36 43 F4 47 91 DF 33 93 21 3B
                79 B7 97 85 10 B5 BA 3C B6 70 D0 06 A1 FA 81 82
                83 7E 7F 80 96 73 BE 56 9B 9E 95 D9 F7 02 B9 A4
                DE 6A 32 6D D8 8A 84 72 2A 14 9F 88 F9 DC 89 9A
                FB 7C 2E C3 8F B8 65 48 26 C8 12 4A CE E7 D2 62
                0C E0 1F EF 11 75 78 71 A5 8E 76 3D BD BC 86 57
                0B 28 2F A3 DA D4 E4 0F A9 27 53 04 1B FC AC E6
                7A 07 AE 63 C5 DB E2 EA 94 8B C4 D5 9D F8 90 6B
                B1 0D D6 EB C6 0E CF AD 08 4E D7 E3 5D 50 1E B3
                5B 23 38 34 68 46 03 8C DD 9C 7D A0 CD 1A 41 1C"""
MATRICE_GF = fu.matrice_gf(MATRICE_GF)

mat_f1 = [[1, 0, 0, 0, 1, 1, 1, 1],
          [1, 1, 0, 0, 0, 1, 1, 1],
          [1, 1, 1, 0, 0, 0, 1, 1],
          [1, 1, 1, 1, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 0, 0],
          [0, 0, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 1, 1, 1, 1, 1]]

mat_f2 = [[1],
          [1],
          [0],
          [0],
          [0],
          [1],
          [1],
          [0]]

m_gf_hex_a_dec = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}

# PREAMBULE : Fonctions utiles pour la suite
def aux_modulo(x, n, m, acc_reste):
    """ Calcul de x^n modulo m avec la méthode d'exponentiation rapide"""
    if n == 1:
        return acc_reste % m
    elif n % 2 == 0:
        return aux_modulo(x*x % m, int(n/2), m, acc_reste*x % m)
    else:
        return aux_modulo(x*x % m, int((n-1)/2), m, acc_reste*x*x % m)

def modulo_exp(x:int, n:int, m:int):
    """ Fonction qui calcule x^n modulo m """
    if n == 0:
        return 1 % m
    else:
        return aux_modulo(x, n, m, x)

def string_to_int(chaine: str, base=27):
    """ Fonction qui convertit une chaîne de caractères en entier et renvoie cet entier """

    n = len(chaine)
    entier = 0
    # i = 1
    for k in range(1, n+1):
        # print("chaine " + str(k) + " : " + chaine[k-1])
        # if chaine[k-1] == ".":
            # print("=========== Fin phrase " + str(i) + " ===========")
            # i += 1
        entier += dico_char_a_int[chaine[k-1]] * base**(n - k)
    return entier

def int_to_string(entier: int, taille_mot: int, b=27):
    """ Fonction qui convertit un entier en chaîne de caractères et renvoie cette chaîne """

    quotient = 0
    diviseur = 0
    dividende = entier
    mot = ""
    # print("entier : ", entier, " | taille mot : ", taille_mot, " | base : ", b)

    for i in range(taille_mot - 1, 0, -1):
        diviseur = b**i
        quotient = dividende // diviseur
        # print("i : ", i)
        # print("dividende : ", dividende)
        # print("diviseur : ", diviseur)
        # print("quotient : ", quotient)
        mot += liste_int_a_char[quotient]
        # print("mot : ", mot)
        # print()
        dividende -= quotient * diviseur
    mot += liste_int_a_char[dividende%b]

    return mot

# Création de l'exception "InvNotFound" utile dans la suite
class InvNotFound(Exception):
    pass

def inverse_mod(b: int, n: int):
    """ Fonction qui prend en paramètre deux entiers b et n et renvoie l'inverse de b modulo n (ie b^(-1))
    ou bien renvoie l'erreur 'InvNotFound' si b^(-1) n'existe pas """
    n_0 = n
    b_0 = b
    t_0 = 0
    t = 1
    q = int(n_0/b_0)
    r = n_0 - q * b_0
    while r > 0:
        temp = t_0 - q * t
        if temp >= 0:
            temp = temp % n
        else:
            temp = n - ((-temp) % n)
        t_0 = t
        t = temp
        n_0 = b_0
        b_0 = r
        q = int(n_0/b_0)
        r = n_0 - q * b_0
    if b_0 != 1:
        raise InvNotFound()
    else:
        return t

# Implémentation algorithme RSA
def creation_cles(lst_nb_prem: list):
    """ Fonction prenant en paramètre une liste de nombres premiers et qui crée puis renvoie un couple de la forme
     (cle_publique, cle_privee) en suivant la méthode de création des clés de l'algorithme de chiffrement RSA\n
     - cle_publique : tuple int \n
     - cle_privee : int """

    # lst_e_phi_n_premiers = []
    e = 2

    # On choisit aléatoirement les valeurs de p et q distinctes
    p = lst_nb_prem.pop(rd.randint(0, len(lst_nb_prem) - 1))
    q = rd.choice(lst_nb_prem)
    # print("Choix de p : ", p)
    # print("Choix de q : ", q)

    # On choisit e et phi_n
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # print("Valeur de n = p * q : ", n)
    # print("Valeur de phi_n = (p-1) * (q-1) : ", phi_n)

    for i in range(2, phi_n): # on cherche le premier e qui convient en partant de e = 2
        if fu.pgcd(i, phi_n) == 1:
            e = i
            break

    # print("Pour e tel que PGCD(e, phi_n) = 1, on a e : ", e)
    d = inverse_mod(e, phi_n)
    # print("Valeur de d inverse modulaire de e mod phi_n : ", d)

    return ((n, e), d) # on renvoie (clé publique, clé privée)

def chiffrer_RSA_naif(m: int, cle_pb: tuple):
    """ Fonction qui prend en paramètre un entier m qui correspond au message à chiffrer et un tuple cle_pb qui
    correspond à la clé de chiffrement. Elle renvoie un entier correspondant au message chiffré """

    assert (m < cle_pb[0])
    # print("début calcul chiffrement et cle_pb : ", cle_pb)
    reste = 1
    for _ in range(cle_pb[1]):
        reste *= m
        reste = reste % cle_pb[0]
    return reste
    # effectue l'opération m**(cle_pb[1]) % cle_pb[0]

def chiffrer_RSA_v2(m: int, cle_pb: tuple):
    """ Fonction qui prend en paramètre un entier m qui correspond au message à chiffrer et un tuple cle_pb qui
    correspond à la clé de chiffrement. Elle renvoie un entier correspondant au message chiffré """

    assert (m < cle_pb[0])
    return modulo_exp(m, cle_pb[1], cle_pb[0])
    # effectue l'opération m**(cle_pb[1]) % cle_pb[0]

def dechiffrer_RSA_naif(x: int, cle_pv: int, n: int):
    """ Fonction prenant en paramètre un entier x correspondant au message à déchiffrer, cle_pv un entier
    correspondant à la clé de déchiffrement et n issue de la cle de chiffrement du message. Elle renvoie un entier
    correspondant au message déchiffré """

    # print("début calcul déchiffrement et cle_pv : ", cle_pv)
    reste = 1
    for _ in range(cle_pv):
        reste *= x
        reste = reste % n
    return reste
    # effectue l'opération x**(cle_pv) % n

def dechiffrer_RSA_v2(x: int, cle_pv: int, n: int):
    """ Fonction prenant en paramètre un entier x correspondant au message à déchiffrer, cle_pv un entier
    correspondant à la clé de déchiffrement et n issue de la cle de chiffrement du message. Elle renvoie un entier
    correspondant au message déchiffré """

    # print("début calcul déchiffrement et cle_pv : ", cle_pv)
    return modulo_exp(x, cle_pv, n)
    # effectue l'opération x**(cle_pv) % n

def chiffrer_chaine_RSA(chaine:str, cle_pb:tuple, taille_facteur=-1):
    """ Fonction qui prend en paramètre une chaine de caractères 'chaine' et un tuple 'cle_pb' et renvoie
    une liste d'entiers correspondants aux facteurs de taille 'taille_facteur', chiffrés avec la fonction 'chiffrer_RSA(...)',
    dont la concaténation forme la chaine 'chaine' avant son chiffrement """

    if taille_facteur == (-1):
        taille_facteur = len(chaine)

    chaine_chiffree = []
    chaine_fractionnee = []
    chaine_courante = ""

    for i in range(len(chaine)): # On décompose 'chaine' en une liste de facteurs de taille 'taille_facteur'
        chaine_courante += chaine[i]
        if len(chaine_courante) % taille_facteur == 0:
            # print("chaine courante : ", chaine_courante)
            chaine_fractionnee.append(chaine_courante)
            chaine_courante = ""

    if chaine_courante != "":
        for i in range(len(chaine_courante), taille_facteur): # on ajoute des espaces pour que le dernier facteur soit de taille taille_facteur
            chaine_courante += " "
        # print("chaine courante : ", chaine_courante, "/")
        chaine_fractionnee.append(chaine_courante) # on ajoute le dernier facteur de taille < 'taille_facteur' (sans compter les espaces)

    for facteur in chaine_fractionnee: # On chiffre tous les facteurs avec la fonction 'chiffrer_RSA(...)'
        int_facteur_courant = string_to_int(facteur, base=95)
        # print("facteur : ", facteur, " | facteur entier : ", int_facteur_courant)
        chaine_chiffree.append(chiffrer_RSA_v2(int_facteur_courant, cle_pb))

    # print("chaine chiffree : ", chaine_chiffree)
    return chaine_chiffree

def dechiffrer_chaine_RSA(liste:list, cle_pv: int, n: int, taille_entiers=1):
    """ Fonction qui prend en paramètre une liste d'entiers 'liste', un entier 'cle_pv' et un entier n et
    renvoie la concaténation des chaines de caractères déchiffrées avec 'dechiffrer_RSA(...)' à partir des entiers
    contenu dans 'liste' représentant des chaines de caractères de taille 'taille_entiers' """

    chaine_dechiffree = ""

    for i in range(len(liste)): # On déchiffre tous les termes de liste sauf le dernier
        # print("chaine_courante dechiffre entière : ", dechiffrer_RSA_v2(liste[i], cle_pv, n))
        chaine_courante = int_to_string(dechiffrer_RSA_v2(liste[i], cle_pv, n), taille_entiers, b=95)
        # print("chaine courante : ", chaine_courante)
        chaine_dechiffree += chaine_courante

    """
    print("chaine dechiffree : ", end="")
    for lettre in chaine_dechiffree:
        print("'" + lettre + "' ", end="")
    print()
    """
    return chaine_dechiffree

def aux_bytesub(a: str):
    """ Fonction auxiliaire de bytesub qui prend en entrée un élément codé en hexadécimal et renvoie le résultat
    de la fonction ByteSub appliquée à celui-ci """

    # on construit b_prime = GF(a)
    print("paquet : ", a)
    m_gf_i = m_gf_hex_a_dec[a[0]]
    m_gf_j = m_gf_hex_a_dec[a[1]]
    b_prime = MATRICE_GF[m_gf_i][m_gf_j]
    print("paquet <- GF(paquet) : ", b_prime)
    # on construit b à partir de b_prime
    b_prime = int(b_prime, 16)
    print("paquet <- int(paquet) : ", b_prime)
    b_prime = str(bin(b_prime))
    b_prime = b_prime[2:]
    b_prime = fu.remplir_zeros(b_prime, 8)
    print("paquet <- bin(paquet) : ", b_prime)
    b_prime = [[int(b_prime[i])] for i in range(len(b_prime))]
    b = fu.produit_matriciel(mat_f1, b_prime, (len(mat_f1), len(mat_f1)), (len(b_prime), 1))
    b = fu.somme_matricielle(b, mat_f2, len(mat_f2), 1)
    for i in range(len(b)):
        b[i][0] = b[i][0] % 2
    b_final = ""
    for chiffre in b:
        b_final += str(chiffre[0])
    b_final = fu.remplir_zeros(b_final, 8)
    print("paquet <- f(paquet) : ", b_final)
    b_final = fu.bin_vers_dec(b_final)
    b_final = str(hex(b_final))

    return b_final[2:]

def bytesub(matrice: list[list]):
    """ Fonction bytesub qui prend en entrée une matrice codée en hexadécimal et renvoie le résultat
    de la fonction aux_bytesub de AES appliquée à celle-ci """

    return [[aux_bytesub(matrice[i][j]) for j in range(len(matrice))] for i in range(len(matrice))]

def shiftrows(matrice: list[list]):
    """ Fonction qui applique la fonction ShiftRows de AES sur la matrice """
    n = len(matrice)
    matrice_finale = []
    for d in range(n):
        matrice_finale.append(fu.decale_liste(matrice[d], d))

    return matrice_finale

# Algorithme AES implémenté avec une bibliothèque
def chiffrer_AES(message:str, cle:bytes, vecteur:bytes):
    """ Fonction qui prend en paramètre un message, une clé et un vecteur et renvoie une chaine de
    caractère correspondant au chiffrement de 'message' avec l'algorithme AES en utilisant la clé 'cle'
    et le vecteur d'initialisation 'vecteur'\n
    - message : chaine de caractères\n
    - cle : chaine de caractères sur 32 octets\n
    - vecteur : chaine de caractères sur 16 octets"""

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode('utf-8'))
    padded_data += padder.finalize()

    cipher = Cipher(algorithms.AES(cle), modes.CBC(vecteur), backend=default_backend())
    encryptor = cipher.encryptor()
    message_chiffre = encryptor.update(padded_data) + encryptor.finalize()

    return message_chiffre

def dechiffrer_AES(message_chiffre, cle:bytes, vecteur:bytes):
    """ Fonction qui prend en paramètre un message, une clé et un vecteur et renvoie une chaine de
        caractère correspondant au déchiffrement de 'message_chiffre' avec l'algorithme AES en utilisant la clé 'cle'
        et le vecteur d'initialisation 'vecteur'\n
        - message_chiffre : chaine de caractères\n
        - cle : chaine de caractères sur 32 octets\n
        - vecteur : chaine de caractères sur 16 octets"""

    decryptor = Cipher(algorithms.AES(cle), modes.CBC(vecteur), backend=default_backend()).decryptor()
    decrypted_data = decryptor.update(message_chiffre) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data)
    unpadded_data += unpadder.finalize()

    return unpadded_data.decode('utf-8')

#####################################################################################################################
#------------------------------------------------- TESTS -------------------------------------------------------------
#####################################################################################################################
if __name__ == "__main__":

    def test_chiffrement_AES():
        cle = b"clesclesclesclesclesclesclescles"
        vecteur = b"clesclesclescles"
        print(cle)
        cle2 = "clesclesclesclesclesclesclescles"
        cle3 = bytes(cle2, encoding="ascii")
        print(cle3)
        msg = "tester son espece de gentil voisin"
        msg_chiffre = chiffrer_AES(msg, cle, vecteur)
        print("Message chiffré :\n", msg_chiffre)
        msg2 = msg_chiffre.decode("latin-1")
        print("test decode : ", msg2)
        print("test encode : ", msg2.encode("latin-1"))
        msg2_dechiffre = dechiffrer_AES(msg2.encode("latin-1"), cle, vecteur)
        print("msg2 dechiffré : ", msg2_dechiffre)

        #print("caractère 1 msg_chiffre : ", msg_chiffre[2])
        msg_dechiffre = dechiffrer_AES(msg_chiffre, cle, vecteur)
        print("Message déchiffré : ", msg_dechiffre)

    def chiffrer_chaine_RSA_V2():
        mot = "tester"
        int_mot = string_to_int(mot)
        print("mot initial : ", mot)
        print("transformation entière : ", int_mot)
        print("/Début phase création des clés/")
        cles = creation_cles(liste_nb_premiers4)
        print("/Fin phase création des clés/")

        debut_envoie_msg = time.perf_counter()
        mot_chiffre = chiffrer_chaine_RSA(mot, cles[0])
        print("Mot chiffré : ", mot_chiffre)
        mot_dechiffre = dechiffrer_chaine_RSA(mot_chiffre, cles[1], cles[0][0], taille_entiers=6)
        print("Mot déchiffré : ", mot_dechiffre)
        fin_envoie_msg = time.perf_counter()
        print("Temps d'exécution : ", fin_envoie_msg - debut_envoie_msg)

    def tests_int_to_str():
        texte = "salut toi comment tu te porte j espele que tu vas bien parce que moi perso c est la dech"
        debut = time.perf_counter()
        texte_entier = string_to_int(texte)
        print("texte entier : ", texte_entier)
        texte_str = int_to_string(texte_entier, len(texte))
        print("texte str : ", texte_str)
        fin = time.perf_counter()
        print("temps : ", fin - debut)

    def affiche_dico():
        print("Dico char : ", dico_char_a_int)
        print("Liste char : ", liste_int_a_char)

    def tests_str_to_int():
        texte1 = "tes"
        texte2 = "tes   "
        print(string_to_int(texte1))
        print(string_to_int(texte2))

    def test_RSA():
        m = 32
        print("Message à chiffrer : ", m)
        cles = creation_cles(liste_nb_premiers4)
        print("Clé publique (n, e) : ", cles[0])
        print("Clé privée d : ", cles[1])
        m_prime = chiffrer_RSA_v2(m, cles[0])
        print("Chiffrement de m : ", m_prime)
        m_bis = dechiffrer_RSA_v2(m_prime, cles[1], cles[0][0])
        print("Déchiffrement de m' : ", m_bis)

    def matrice_gf():
        m_gf = fu.conversion_matrice(MATRICE_GF, int, 16)
        for ligne in m_gf:
            print(ligne)
        print("taille matrice : ", len(m_gf))

    def test_bytesub():
        m = """9B 01 8D F6
         74 B4 AA 4B
          EF 6E 5A F1
           2C 45 92 EF"""
        m = fu.matrice_gf(m, 4)
        fu.affiche_matrice(m)
        print()
        fu.affiche_matrice(bytesub(m))

    def test_shiftrows():
        m = """9B 01 8D F6
                 74 B4 AA 4B
                  EF 6E 5A F1
                   2C 45 92 EF"""
        m = fu.matrice_gf(m, 4)
        fu.affiche_matrice(m)
        print()
        fu.affiche_matrice(shiftrows(m))

    # test_chiffrement_AES()
    # chiffrer_chaine_RSA_V2()
    # tests_int_to_str()
    # affiche_dico()
    # tests_str_to_int()
    # test_RSA()
    # matrice_gf()
    # test_bytesub()
    print("paquet <- hex(paquet) : ", aux_bytesub("9B"))
    # test_shiftrows()









