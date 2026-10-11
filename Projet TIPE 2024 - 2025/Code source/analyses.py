import matplotlib.pyplot as plt
import fonctions_utiles as fu
import algos_chiffrement as algos
import time
import math
import hashlib


def ecrire(liste:list, ordre_grandeur:int):
    """ Fonction qui écrit les 100 derniers éléments de la liste dans un fichier texte """
    n = len(liste)
    with open("nombres_premiers/liste_nb_premiers_10e" + str(ordre_grandeur) + ".txt", 'w') as sortie:
        for i in range(n - 1, n - 101, -1):
            print("Nombre premier ", liste[i], " écrit dans le fichier txt")
            sortie.write(str(liste[i]) + "\n")

def nb_premier(maximum:int):
    """ Renvoie la liste des nombres premiers inférieurs à 'maximum' """
    length = maximum // 3
    if maximum % 3 == 0 or maximum % 3 == 1 and maximum % 6 != 1: length -= 1
    flags = [True] * length
    number = 1
    addition = 4
    toggle = 6
    for indexe in range(length):
        number += addition
        addition = toggle - addition
        if not flags[indexe]: continue
        start = (number * number * 2 - 5) // 6
        if start >= length: break
        step = 2 * number
        flags[start::step] = [False] * ((length - start + step - 1) // step)
        advance = (indexe + 2) // 2
        start += number - 2 * advance + (indexe % 2) * 4 * advance
        flags[start::step] = [False] * ((length - start + step - 1) // step)
    print(f"{sum(flags) + 2} nombres premiers dans l'intervalle [1, {maximum}")
    primes = [2, 3] + [i // 2 * 6 + 5 + i % 2 * 2 for i in range(length) if flags[i]]

    return primes

def execution_RSA(nom_fichier_nb_premier: str, nom_fichier_msg, taille_facteurs=1, cle=((0, 0), 0)):
    """ Fonction qui déchiffre et chiffre le texte contenu dans
    le fichier 'nom_fichier_msg' avec l'algorithme RSA utilisant les nombres premiers contenu dans
    'nom_fichier_nb_premier', et renvoie son propre temps d'exécution"""

    if ".txt" in nom_fichier_msg:
        decomp_msg = fu.importer_fichier(nom_fichier_msg, type="str")
        msg = ""

        for ligne in decomp_msg:
            msg += ligne + " "
    else:
        msg = nom_fichier_msg

    liste_nb_premiers = fu.importer_fichier(nom_fichier_nb_premier)
    if cle == ((0, 0), 0):
        cles = algos.creation_cles(liste_nb_premiers)
    else:
        cles = cle

    # print("cles : ", cles)

    debut_envoie_msg = time.perf_counter()
    mot_chiffre = algos.chiffrer_chaine_RSA(msg, cles[0], taille_facteur=taille_facteurs)
    mot_dechiffre = algos.dechiffrer_chaine_RSA(mot_chiffre, cles[1], cles[0][0], taille_entiers=taille_facteurs)
    fin_envoie_msg = time.perf_counter()

    return round(fin_envoie_msg - debut_envoie_msg, 5)

def execution_AES(msg:str, cle:bytes, vecteur:bytes):
    """ Fonction qui chiffre et déchiffre 'msg' avec l'algo AES(cle, vecteur) et renvoie
    son propre temps d'exécution """

    debut = time.perf_counter()
    msg_chiffre = algos.chiffrer_AES(msg, cle, vecteur)
    msg_dechiffre = algos.dechiffrer_AES(msg_chiffre, cle, vecteur)
    fin = time.perf_counter()
    return round(fin - debut, 5)

def tracer_graphe(abscisses: list, ordonnees: list, titre="", xlabel="", ylabel="", xticks=([], [])):
    """ Fonction qui prend en paramètre une liste d'abscisses et une autre d'ordonnées et trace
    le graphe engendré par ces coordonnées """

    # axe = plt.subplots()
    # axe[1].set_ylim(0, 1)
    plt.plot(abscisses, ordonnees, marker="*")
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xticks != ([], []):
        plt.xticks(xticks[0], xticks[1])
    plt.show()
    plt.close()

#####################################################################################################################
# Tests

if __name__ == "__main__":

    def tracer_graphe_RSA_nb_premiers(p_debut, p_fin):
        abscisses = [i for i in range(p_debut, p_fin + 1)]
        ordonnees = []
        n = len(abscisses)
        xticks = ([i for i in range(3, n + 3)], ["10e" + str(i) for i in range(3, n + 3)])

        for i in range(p_debut, p_fin + 1):
            fichier_nb_premiers = "nombres_premiers/liste_nb_premiers_10e" + str(i) + ".txt"
            ordonnees.append(execution_RSA(fichier_nb_premiers, "msg_test.txt", 3))

        tracer_graphe(abscisses, ordonnees, "Exécution de RSA en fonction de l'ordre de grandeur des nb_premiers"
                      , "nombres premiers (ordre de grandeur)", "temps (s)", xticks=xticks)

    def tracer_graphe_RSA_taille_msg(borne:int, log=False):
        liste_msg = []
        msg_courant = "tttttttttt"
        for i in range(1, borne + 1):
            liste_msg.append(msg_courant)
            msg_courant += msg_courant

        if log:
            abscisses = [math.log(len(mot)) for mot in liste_msg]
            xlabel = "ln(taille message)"
        else:
            abscisses = [len(mot) for mot in liste_msg]
            xlabel = "taille message"

        ordonnees = []
        i = 1

        cles = algos.creation_cles(fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))

        for mot in liste_msg:
            ordonnees.append(execution_RSA("nombres_premiers/liste_nb_premiers_10e8.txt", mot, 3, cle=cles))
            print("mot ", i, " testé")
            i += 1

        tracer_graphe(abscisses, ordonnees, "Exécution de RSA en fonction de la taille des mots"
                      , xlabel, "temps (s)")

        print("abscisses :\n", abscisses)
        print("ordonnees :\n", ordonnees)

    def tracer_graphe_AES(borne:int, log=False):
        liste_msg = []
        msg_courant = "tttttttttt"
        for i in range(1, borne + 1):
            liste_msg.append(msg_courant)
            msg_courant += msg_courant

        cle_RSA = fu.generateur_alea_chaine(32)
        cles = algos.creation_cles(fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))
        temps_cle_RSA = execution_RSA("nombres_premiers/liste_nb_premiers_10e8.txt", cle_RSA, 3, cle=cles)

        if log:
            abscisses = [math.log(len(mot)) for mot in liste_msg]
            xlabel = "ln(taille message)"
        else:
            abscisses = [len(mot) for mot in liste_msg]
            xlabel = "taille message"

        ordonnees = []
        cle = b"clesclesclesclesclesclesclescles"
        vecteur = b"clesclesclescles"
        i = 1

        for mot in liste_msg:
            ordonnees.append(round(execution_AES(mot, cle, vecteur) + temps_cle_RSA, 5))
            print("mot ", i, " testé")
            i += 1

        abscisses.pop(0)
        ordonnees.pop(0)

        tracer_graphe(abscisses, ordonnees, "Exécution de AES en fonction de la taille des mots"
                      , xlabel, "temps (s)")

        print("abscisses :\n", abscisses)
        print("ordonnees :\n", ordonnees)

    def creer_fichier_nb_premier(puissance:int):
        maximum = 10**puissance
        liste_nb_premiers = nb_premier(maximum)
        ecrire(liste_nb_premiers, puissance)

    def tracer_graphe_SHA(borne:int):
        liste_msg = []
        msg_courant = "0123456789"
        for i in range(1, borne + 1):
            liste_msg.append(msg_courant)
            msg_courant += msg_courant

        abscisses = [len(mot) for mot in liste_msg]
        xlabel = "taille clé"

        ordonnees = []
        i = 1

        for mot in liste_msg:
            debut = time.perf_counter()
            hash_mot = hashlib.sha256(mot.encode())
            hash_mot = hash_mot.hexdigest()
            fin = time.perf_counter()
            ordonnees.append(fin - debut)
            print("mot ", i, " testé")
            i += 1

        # abscisses.pop(0)
        # ordonnees.pop(0)

        tracer_graphe(abscisses, ordonnees, "Exécution de SHA256 en fonction de la taille des clés"
                      , xlabel, "temps (s)")

    tracer_graphe_AES(18, log=False)
    # tracer_graphe_RSA_taille_msg(18, log=False)
    # tracer_graphe_RSA_nb_premiers(3, 8)
    # creer_fichier_nb_premier(9)
    # tracer_graphe_SHA(18)


