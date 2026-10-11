import client
import fonctions_utiles as fu

code_RSA = False

if code_RSA:
    client_1 = client.Client_RSA(1, fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))
else:
    client_1 = client.Client_AES_RSA(1, fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))
client_1.connection()