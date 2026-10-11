import client
import fonctions_utiles as fu

client_malv = client.ClientMalveillant(3, fu.importer_fichier("nombres_premiers/liste_nb_premiers_10e8.txt"))
client_malv.connection()