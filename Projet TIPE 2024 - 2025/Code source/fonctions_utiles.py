#####################################################################################################################
# Fichier : fonctions_utiles.py
# ==> Contient les fonctions utiles aux différentes fonctions des autres fichiers .py
#####################################################################################################################
# Import des modules utiles
import random as rd
#####################################################################################################################


def copie_dict(dico:dict):
    """ Fonction qui renvoie une copie indépendante du dictionnaire 'dico' """
    dico_copie = {}
    for cle, valeur in dico.items():
        dico_copie[cle] = valeur

    return dico_copie

def pgcd(a: int, b: int):
    """ Fonction qui prend en paramètre 2 entiers naturel a et b et renvoie leur PGCD """

    dividende = max(a, b)
    diviseur = min(a, b)
    temp = 0
    while (dividende % diviseur) != 0 :
        temp = dividende % diviseur
        dividende = diviseur
        diviseur = temp

    return diviseur

def compression_arg_str(liste_args: list, separateur="/"):
    """ Fonction qui prend en paramètre une liste d'objets pouvant être convertis en chaine de caractères, un séparateur
     '/' et renvoie une chaine de caractères contenant n paramètres et qui est de la forme 'arg[1]/arg[2]/.../arg[n]' """

    arguments = ""
    for i in range(len(liste_args)):
        if i != len(liste_args) - 1:
            arguments += str(liste_args[i]) + separateur
        else:
            arguments += str(liste_args[i])

    return arguments

def extraction_arg_str(chaine_args: str, separateur="/"):
    """ Fonction qui prend en paramètre une chaine de caractères contenant n arguments et de la forme
    'arg[1]/arg[2]/.../arg[n]', un séparateur '/' et renvoie une liste contenant les n arguments de type int"""

    chiffres = "0123456789"
    liste_args = []
    arg_courant = ""
    for i in range(len(chaine_args)):
        if chaine_args[i] != separateur and chaine_args[i] in chiffres:
            arg_courant += chaine_args[i]
        else:
            liste_args.append(int(arg_courant))
            arg_courant = ""

    if arg_courant != "":
        liste_args.append(int(arg_courant))

    return liste_args

def decomposition_chaine(chaine: str, separateur="|"):
    """ Fonction qui prend en paramètre une chaîne de caractères que l'on peut diviser en sous-chaînes séparées par
    un séparateur ':' et renvoie une liste contenant ces sous-chaînes """

    liste_sous_chaines = []
    arg_courant = ""
    for i in range(len(chaine)):
        if chaine[i] != separateur:
            arg_courant += chaine[i]
        else:
            liste_sous_chaines.append(arg_courant)
            arg_courant = ""

    if arg_courant != "":
        liste_sous_chaines.append(arg_courant)

    return liste_sous_chaines

def id_client(chaine: str):
    """ Fonction qui prend une chaine de caractères de type '<Client- * > *** ' et renvoie l'entier * en chaine de
    caractères """

    chiffres = "0123456789"
    id_passe = False
    id = ""
    for char in chaine:
        if char in chiffres:
            id_passe = True
            id += char
        elif id_passe:
            break

    return id

def importer_fichier(nom_fichier:str, type="int"):
    """ Importe un fichier texte et ajoute chaque ligne du fichier dans une liste Python que la fonction
     renvoie """
    liste_nb_premiers = []
    with open(nom_fichier, "r") as fichier:
        contenu = fichier.readlines()

    for ligne in contenu:
        ligne_actuelle = ligne.rstrip("\n")
        if type == "int":
            liste_nb_premiers.append(int(ligne_actuelle))
        else:
            liste_nb_premiers.append(ligne_actuelle)

    return liste_nb_premiers

def generateur_alea_chaine(taille_chaine:int):
    """ Fonction qui génère aléatoirement une chaine de caractères de taille 'taille_chaine',
    composée des lettres de l'alphabet en minuscule, et la renvoie """

    liste_int_a_char = "abcdefghijklmnopqrstuvwxyz"
    nb_char = len(liste_int_a_char)
    chaine_alea = ""

    for _ in range(taille_chaine):
        i = rd.randint(0, nb_char - 1)
        chaine_alea += liste_int_a_char[i]

    return chaine_alea

def concat_chaine(chaine:str, n:int):
    """ Fonction qui renvoie la concaténation de 'chaine' (n-1) fois """
    chaine_finale = ""
    for _ in range(n):
        chaine_finale += chaine
    return chaine_finale

def encode_ascii(chaine:str):
    """ Fonction qui transforme une chaine str en bstr (ie en code ASCII)\n
    NB : elle fait la même chose que la fonction native bytes(chaine, encoding="ascii") """

    return bytes(chaine, encoding="utf-8")

def matrice_gf(chaine: str, taille=16):
    """ Renvoie la matrice GF sous forme de matrice de type list[list] """
    matrice_gf = decomposition_chaine(chaine, separateur=" ")
    matrice_gf_bis = []
    matrice_gf_finale = []
    ligne_gf = []

    for i in range(len(matrice_gf)):
        if "\n" in matrice_gf[i]:
            matrice_gf_bis.append(matrice_gf[i][:(-1)])
        elif matrice_gf[i] != "":
            matrice_gf_bis.append(matrice_gf[i])

    for i in range(taille):
        for j in range(taille):
            ligne_gf.append(matrice_gf_bis[i*taille + j])
            if j == taille - 1:
                matrice_gf_finale.append(ligne_gf)
                ligne_gf = []

    return matrice_gf_finale

def conversion_matrice(matrice: list[list], fonction, base=10):
    """ Fonction qui applique la fonction de conversion 'fonction' sur chaque case de la matrice carrée """
    res = matrice.copy()
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if base != 10:
                res[i][j] = fonction(res[i][j], base)
            else:
                res[i][j] = fonction(res[i][j])

    return res

def produit_matriciel(m1: list[list[int]], m2: list[list[int]], n1=(-1, -1), n2=(-1, -1)):
    """ Fonction qui renvoie le produit matriciel des matrices m1 et m2 """
    assert(n1[1] == n2[0])

    if n1 == (-1,-1):
        n = len(m1)
        p = n
        q = n
    else:
        n, p = n1[0], n1[1]
        q = n2[1]

    res = [[0 for _ in range(q)] for _ in range(n)]

    for i in range(n):
        for j in range(q):
            somme = 0
            for k in range(p):
                somme += m1[i][k] * m2[k][j]
            res[i][j] = somme
    return res

def somme_matricielle(m1: list[list[int]], m2: list[list[int]], n: int, p: int):
    """ Fonction qui renvoie la somme des matrices m1 et m2 """
    res = [[0 for _ in range(p)] for _ in range(n)]

    for i in range(n):
        for j in range(p):
            res[i][j] = m1[i][j] + m2[i][j]

    return res

def bin_vers_dec(x:str):
    """ Fonction qui convertit un élément de type int binaire en élément de type int décimal"""
    x_str = str(x)
    x_liste = [int(c) for c in x_str]
    x_liste.reverse()
    x_int = 0
    k = 0
    for c in x_liste:
        x_int += 2**k * c
        k += 1

    return x_int

def remplir_zeros(x, n: int):
    """ Rajoute des zéros jusqu'à ce que 'x' soit un nombre binaire codé sur n bits """
    x_str = str(x)
    while len(x_str) < n:
        x_str = "0" + x_str

    return x_str

def affiche_matrice(m: list[list]):
    """ Fonction qui affiche une matrice carrée """
    for i in range(len(m)):
        for j in range(len(m)):
            print(m[i][j], " ", end="")
        print()

def decale_liste(liste: list, d: int):
    """ Fonction qui décale les éléments de la liste de 'd' vers la droite
    et renvoie le résultat"""
    liste_bis = liste.copy()
    liste_finale = []
    d_bis = d

    if d == 0:
        return liste

    while d_bis > 0:
        liste_finale = []
        liste_finale.append(liste_bis.pop())
        for el in liste_bis:
            liste_finale.append(el)
        liste_bis = liste_finale.copy()
        d_bis -= 1

    return liste_finale

# Jeu de tests
if __name__ == "__main__":
    def tests_generateur_alea_chaine():
        chaine = generateur_alea_chaine(5)
        print("Chaine aléatoire : ", chaine)

    def tests_encode_ascii():
        cle1 = "test"
        cle1b = b'Cha\xc3\xaene accentu\xc3\xa9e'
        print(cle1b[1])
        print(type(cle1b))
        cle3 = 'Chaîne accentuée'
        cle3b = cle3.encode("utf-8")
        print(type(cle3b))
        print("cle1b decode : ", cle1b.decode("utf-8"))
        print("cle3 encode : ", cle3b)
        print("cle3 decode : ", cle3b.decode("utf-8"))


    def tests_compression_args_str():
        print(compression_arg_str(["salut", "toi"]))
        print(compression_arg_str(["salut"]))

    def tests_extraction_arg_str():
        print(extraction_arg_str("98/16"))
        print(extraction_arg_str("98"))

    def test_decale():
        l = [1, 2, 3, 4]
        for d in range(0, 5):
            print(decale_liste(l, d))

    m1 = [[2, 3],
          [1, 4]]
    m2 = [[2, 2],
          [3, 1]]

    # tests_generateur_alea_chaine()
    # tests_encode_ascii()
    # tests_compression_args_str()
    # tests_extraction_arg_str()
    # print(produit_matriciel(m1, m2))
    test_decale()



