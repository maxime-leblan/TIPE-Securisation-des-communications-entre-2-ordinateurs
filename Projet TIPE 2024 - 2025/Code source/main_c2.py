import client
import fonctions_utiles as fu

code_RSA = False

if code_RSA:
    client_2 = client.Client_RSA(2, fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))
else:
    client_2 = client.Client_AES_RSA(2, fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))
client_2.connection()