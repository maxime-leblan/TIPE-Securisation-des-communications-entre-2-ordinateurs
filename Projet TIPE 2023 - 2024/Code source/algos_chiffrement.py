#####################################################################################################################
# Algorithme : algos_chiffrement.py
# ==> Contient les fonctions permettants de sécuriser les communications
#####################################################################################################################

ALPHABET_L_TO_I = {}
ALPHABET_I_TO_L = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(len(ALPHABET_I_TO_L)):
    ALPHABET_L_TO_I[ALPHABET_I_TO_L[i]] = i


# PREAMBULE : Fonctions utiles pour la suite
def modulo(nombre:int, modulo:int, decalage=0): # O(1)
    """ Fonction améliorée de la fonction native en python '%' qui renvoie la congruence de 'nombre'
    modulo 'modulo' avec un éventuel décalage (permettant de gérer les valeurs décimales des caractères ASCII
    que peut prendre la variable 'nombre')"""
    res = nombre - decalage
    if res < 0:
        return (modulo + decalage) + res
    else:
        return (res % modulo) + decalage

def occurence_char(char:str, chaine:str): # O(taille chaine)
    """ Fonction qui prend en paramètre une chaine de caractères 'chaine' et un caractère 'char' et renvoie
    le nombre d'occurences de 'char' dans 'chaine' """

    occurence = 0

    for element in chaine: # on parcourt la chaine et on ajoute 1 à 'occurence' dès que element = 'char'
        if element == char:
            occurence += 1

    return occurence

def est_une_phrase(chaine:str):
    """ Fonction qui prend en paramètre une chaine et renvoie True si la chaine a de fortes chances
    d'être une phrase française et False sinon """

    ponctuation = ".;:!?,()[]-/&#{}|\@$¤£%µ*+=~§<>^`"
    occurence_ponctuation = 0
    occurence_espace = 0

    # On compte le nombre d'occurence de l'espace et des caractères contenus dans 'ponctuation'
    for i in range(len(chaine)):
        if chaine[i] in ponctuation:
            occurence_ponctuation += 1
        elif chaine[i] == " ":
            occurence_espace += 1

    # On regarde si la fréquence d'apparition de l'espace et celle de la ponctuation correspondent
    # à celles constatées dans un texte français en général (0.02 pour la ponctuation et 0.15 pour les espaces)
    return (occurence_ponctuation / len(chaine) <= 0.1) and (occurence_espace / len(chaine) >= 0.1)

def nombre_lettres(chaine:str): # O(taille chaine)
    """ Fonction qui prend en paramètre un texte dans 'chaine' et qui renvoie le nombre
    de lettres que contient 'chaine' """

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    nb_lettres = 0
    texte = chaine.lower()

    for char in texte:
        if char in alphabet:
            nb_lettres += 1

    return nb_lettres

# PARTIE I : Le Code de César

def code_cesar(mode:str, chaine:str, cle:int): # Complexité = O(taille chaine)
    """ Fonction prenant comme paramètres :
            - mode : variable de type str() comportant la valeur 'chiffrer' ou 'dechiffrer', indique si
            l'utilisateur veut chiffrer ou déchiffrer un message\n
            - chaine : variable de type str() contenant le message à chiffrer/déchiffrer
            - cle : variable de type int() contenant la clé de décalage
        et renvoyant une variable de type str() contenant le texte de 'chaine' chiffré avec le Code de César"""

    chaine_final = ""
    if mode == "chiffrer": # si on est en mode chiffrement, on effectue l'algorithme ci-dessous
        for char in chaine:
            if char in ALPHABET_I_TO_L:
                # les caractères codés vont de 0 à 51 inclu
                nouveau_char = ALPHABET_I_TO_L[modulo((ALPHABET_L_TO_I[char] + cle), 52)] # on calcule la lettre équivalente à celle contenue
                # dans chaine
            else:
                nouveau_char = char
            chaine_final = chaine_final + nouveau_char # on l'ajoute dans la variable final
    else: # sinon, on est dans l'autre cas
        for char in chaine:
            if char in ALPHABET_I_TO_L:
                # les caractères codés vont de 0 à 51 inclu
                nouveau_char = ALPHABET_I_TO_L[modulo((ALPHABET_L_TO_I[char] - cle), 52)]  # on calcule la lettre équivalente à celle contenue
                # dans chaine
            else:
                nouveau_char = " "
            chaine_final = chaine_final + nouveau_char  # on l'ajoute dans la variable final
    return chaine_final

def code_cesar_force_brute(chaine:str): # Complexité = O(taille chaine)
    """ Fonction prenant en paramètre la variable 'chaine' de type str() contenant un message à décoder
    par force brute et renvoie un tableau associatif contenant les solutions potentielles"""

    solutions_potentielles = {}
    for cle in range(1, 52):
        solutions_potentielles[str(cle)] = code_cesar("dechiffrer", chaine, cle)
        # print("Décryptage avec la clé " + str(cle) + " : ", solutions_potentielles[str(cle)])
    return solutions_potentielles

def afficher_solutions_potentielles(dico:dict):
    """ Fonction qui prend en paramètre un dictionnaire contenant les solutions potentielles du
    décryptage d'une chaine chiffrée à l'aide du Code de César, et affiche ces solutions"""

    for cle, valeur in dico.items():
        print("Décryptage avec la clé " + cle + " : " + valeur)


# PARTIE II : Le Chiffre de Vigenère

def chiffre_vigenere(mode:str, chaine:str, cle:str): # O(taille chaine)
    """ Fonction prenant comme paramètres :
            - mode : variable de type str() comportant la valeur 'encode' ou 'decode', indique si
            l'utilisateur veut chiffrer ou déchiffrer un message\n
            - chaine : variable de type str() contenant le message à chiffrer/déchiffrer
            - cle : variable de type str() contenant la clé permettant de chiffrer le message
        et renvoyant une variable de type str() contenant le texte de 'chaine' chiffré avec le
        Chiffre de Vigenère"""

    chaine_final = str()
    chaine_cle = str()
    long_cle = len(cle)
    indice = 0

    # On construit la chaine composée de la clé répétée un certain nombre de fois, qui servira à encoder ou
    # à décoder le message passé en paramètre de la fonction
    for lettre in chaine:
        if lettre != " ":
            chaine_cle += cle[indice % long_cle]
            indice += 1
        else:
            chaine_cle += " "

    # print(chaine_cle)

    for i in range(len(chaine)):
        if chaine[i] != " ":
            cle_code_cesar = ALPHABET_L_TO_I[chaine_cle[i]] # on calcule la clé de décalage à partir de la lettre
            # d'indice i de chaine_cle
            chaine_final += code_cesar(mode, chaine[i], cle_code_cesar)
        else:
            chaine_final += " "

    return chaine_final

def indice_coincidence(chaine:str): # O(taille chaine)
    """ Fonction qui prend en paramètre une chaine de caractère 'chaine', calcule son indice de
    coïncidence et le renvoie"""

    n = nombre_lettres(chaine)
    liste_occurences = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    i_coincidence = 0

    if n > 1: # Pour éviter les divisions par 0
        for lettre in alphabet:
            liste_occurences.append(occurence_char(lettre, chaine.lower()))

        for n_i in liste_occurences:
            i_coincidence += (n_i * (n_i - 1))/(n * (n - 1))
    else: # On renvoie -1 pour dire qu'on a pas pu calculer l'indice de coïncidence
        i_coincidence = -1

    return i_coincidence

def decoupage_texte(chaine:str, long_cle:int): # O(taille chaine)
    """ Fonction qui prend en paramètre une chaîne de caractères 'chaine' et renvoie une liste
    contenant le découpage de 'chaine' en chaine de caractères de taille long_cle"""

    decoupage_chaine = ["" for _ in range(long_cle)]
    i = 0

    # On découpe la chaine en long_cle textes que l'on stocke dans decoupage_chaine
    for char in chaine:
        if char in ALPHABET_I_TO_L:
            decoupage_chaine[i % long_cle] += char
            i += 1

    return decoupage_chaine

def recherche_taille_cle(chaine:str, debut_recherche:int): # O(taille_chaine^3)
    """ Fonction qui prend en parametre une chaine de caractère chiffrée à l'aide du
    chiffre de Vigenère et un entier indiquant la taille de la clé à prendre en premier.
    Elle renvoie la longueur probable de la clé qui a été utilisée pour chiffrer la chaine
    de caractères passée en paramètre """
    ic_moyen = 0
    ic_fr = 0.077
    taille_decoupage = 0

    # On teste la méthode pour toutes les tailles possibles de clés
    for n in range (debut_recherche, nombre_lettres(chaine) + 1):
        decoupage = decoupage_texte(chaine, n)
        taille_decoupage = len(decoupage)
        # On calcule l'indice de coïncidence moyen des éléments de découpage
        for element in decoupage:
            ic_courant = indice_coincidence(element)
            if ic_courant > 0:
                ic_moyen += ic_courant
            else:
                taille_decoupage -= 1
        try:
            ic_moyen = ic_moyen / taille_decoupage
        except ZeroDivisionError:
            continue
        # Si ic_moyen est à peu près égal à ic_fr, alors on a trouvé la taille de la clé
        if  0.95 * ic_fr <= ic_moyen and ic_moyen <= 1.05 * ic_fr:
            return n
        ic_moyen = 0

    return -1

def restitution_message_clair(chaine:str, long_cle:int):
    """ Fonction qui prend en paramètre une chaine de caractère chiffrée à l'aide du
    chiffre de Vigenère et un entier correspondant à la taille de la clé utilisée pour chiffrer
    cette même chaine. Elle renvoie la chaine de caractère passée en paramètre après son
    déchiffrement """

    chaine_decryptee = str()
    liste_textes = ["" for _ in range(long_cle)]
    liste_indices_textes = [0 for _ in range(long_cle)]
    j = 0
    nb_max_occurence = (0, "")
    nb_courant_occurence = (0, "")
    cle_code_cesar = 0

    for char in chaine:
        liste_textes[j % long_cle] += char
        if char in ALPHABET_I_TO_L:
            j += 1

    for i in range(long_cle):
        for char in liste_textes[i]:
            if char in ALPHABET_I_TO_L:
                nb_courant_occurence = (occurence_char(char, liste_textes[i]), char)
                if nb_courant_occurence[0] > nb_max_occurence[0]:
                    nb_max_occurence = nb_courant_occurence

        cle_code_cesar = modulo(ALPHABET_L_TO_I[nb_max_occurence[1]] - ALPHABET_L_TO_I["e"], 52)
        liste_textes[i] = code_cesar("dechiffrer", liste_textes[i], cle_code_cesar)
        nb_max_occurence = (0, "")

    for i in range (len(chaine)):
        indice = i % long_cle
        if liste_indices_textes[indice] < len(liste_textes[indice]):
            chaine_decryptee += liste_textes[indice][liste_indices_textes[indice]]
            if liste_textes[indice][liste_indices_textes[indice]] not in ALPHABET_I_TO_L:
                chaine_decryptee += liste_textes[indice][liste_indices_textes[indice] + 1]
                liste_indices_textes[indice] += 1
            liste_indices_textes[indice] += 1

    return chaine_decryptee

def chiffre_vigenere_friedman(chaine:str): # O(taille_chaine^3)
    """ Fonction qui prend en paramètre une chaine de caractères chiffrée à l'aide du
    chiffre de Vigenère et renvoie cette même chaine déchiffrée, en ayant utilisé la méthode
    de Friedman """

    taille_cle = recherche_taille_cle(chaine, 2)
    return restitution_message_clair(chaine, taille_cle)

#####################################################################################################################
#------------------------------------------------- TESTS -------------------------------------------------------------
#####################################################################################################################
if __name__ == "__main__":
    """
    chaine = "Ceci est un message secret"
    chaine_chiffree = code_cesar2("chiffrer", chaine, 17)
    print("Texte chiffré : ", chaine_chiffree)
    print("Texte déchiffré : ", code_cesar2("dechiffrer", chaine_chiffree, 17))
    print("\n")

    dico = code_cesar_force_brute(chaine_chiffree)
    
    afficher_solutions_potentielles(dico)
    """
    
    chaine = "J adore ecouter la radio toute la journee"
    chaine_chiffree = chiffre_vigenere("chiffrer", chaine, "MUSIQUE")
    print("Texte chiffré : ", chaine_chiffree)
    print("Texte déchiffré : ", chiffre_vigenere("dechiffrer", chaine_chiffree, "MUSIQUE"))


    """
    fichier = open("texte.txt", "r")
    contenu = fichier.read()
    fichier.close()
    """

    chaine = "Bienvenue a Poudlard dit le professeur McGonagall Le banquet de debut d annee va bientot commencer mais avant que vous preniez place dans la Grande Salle vous allez etre repartis dans les differentes maisons Cette repartition constitue une ceremonie tres importante Vous devez savoir en effet que tout au long de votre sejour a l ecole votre maison sera pour vous comme une seconde famille Vous y suivrez les memes cours vous y dormirez dans le meme dortoir et vous passerez votre temps libre dans la meme salle commune Les maisons sont au nombre de quatre Elles ont pour nom Gryffondor Poufsouffle Serdaigle et Serpentard Bienvenue a Poudlard dit le professeur McGonagall Le banquet de debut d annee va bientot commencer mais avant que vous preniez place dans la Grande Salle vous allez etre repartis dans les differentes maisons Cette repartition constitue une ceremonie tres importante Vous devez savoir en effet que tout au long de votre sejour a l ecole votre maison sera pour vous comme une seconde famille Vous y suivrez les memes cours vous y dormirez dans le meme dortoir et vous passerez votre temps libre dans la meme salle commune Les maisons sont au nombre de quatre Elles ont pour nom Gryffondor Poufsouffle Serdaigle et Serpentard Bienvenue a Poudlard dit le professeur McGonagall Le banquet de debut d annee va bientot commencer mais avant que vous preniez place dans la Grande Salle vous allez etre repartis dans les differentes maisons Cette repartition constitue une ceremonie tres importante Vous devez savoir en effet que tout au long de votre sejour a l ecole votre maison sera pour vous comme une seconde famille Vous y suivrez les memes cours vous y dormirez dans le meme dortoir et vous passerez votre temps libre dans la meme salle commune Les maisons sont au nombre de quatre Elles ont pour nom Gryffondor Poufsouffle Serdaigle et Serpentard"

    chaine2 = """Nearly ten years had passed since the Dursleys had woken up to find their nephew on the front step, but Privet Drive had hardly changed at all. The sun rose on the same tidy front gardens and lit up the brass number four on the Dursleys' front door; it crept into their living room, which was almost exactly the same as it had been on the night when Mr. Dursley had seen that fateful news report about the owls. Only the photographs on the mantelpiece really showed how much time had passed."""

    """
    # print("indice texte.txt : ", indice_coincidence(contenu))
    print("indice chaine : ", indice_coincidence(chaine))
    print(decoupage_texte(chaine, 3))
    """

    texte_test = "saluttoutlemondejesperequevousallezbienlejourducouronnementestarrivevousalleztousdevoirvousprosternerdevantvotrenouveauroileseigneurvadorquiadecidedevenirapportelapaixlalibertelajusticeetlasecuriteasonnouvelempiremaislejediarepondutonnouvelempirecommentcatunaspasdempire"


    texte_test2 = "Ceci est un message qui n est pas encore chiffre"
    texte_test3 = "Bienvenue a Poudlard dit le professeur McGonagall Le banquet de debut d annee va bientot commencer mais avant que vous preniez place dans la Grande Salle vous allez etre repartis dans les differentes maisons Cette repartition constitue une ceremonie tres importante"
    print("indice texte.txt : ", indice_coincidence(texte_test2))

    chaine_cryptee = chiffre_vigenere("chiffrer", texte_test3, "cle")
    print("\nMessage chiffré : ", chaine_cryptee)
    print("Message clair : ", chiffre_vigenere_friedman(chaine_cryptee))
