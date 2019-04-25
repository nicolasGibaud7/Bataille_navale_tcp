import socket
from joueur import *


def config_reseau():
    # Configuration réseau
    TCP_PORT = 12800

    # Création d'une socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # On écoute le socket
    sock.bind(('', TCP_PORT))

    # On limite le nombre de connexions simultanées à deux
    sock.listen(2)

    # Pḧase de connexion au serveur des joueurs
    co_j1, infos_co_j1 = sock.accept()
    print("J1 connecté d'adresse IP " + infos_co_j1[0])
    co_j1.send(b"Bonjour J1")
    co_j1.send(b"Attente deuxieme joueur")

    co_j2, infos_co_j2 = sock.accept()
    print("J2 connecté d'adresse IP " + infos_co_j2[0])
    co_j2.send(b"Bonjour J2")
    co_j1.send(b"Joueur 2 trouve")
    co_j2.send(b"Lancement de la partie !")
    co_j1.send(b"Lancement de la partie !")

    return (sock, co_j1, co_j2)

def close_connection(sock, co_j1, co_j2):
    # Fermeture des différentes connexions
    co_j1.close()
    co_j2.close()
    sock.close()

def info_joueur(sock, co_j):
    # Demande de pseudo
    co_j.send(b'1')
    msg_recv = co_j.recv(1024)
    nom = msg_recv.decode()

    print("Pseudo joueur : " + nom)

    co_j.send(b"Ok cool")

    return nom

sock, co_j1, co_j2 = config_reseau()
nom_j1 = info_joueur(sock, co_j1)
j1 = Joueur(nom_j1, Plateau(8), 2, co_j1)
nom_j2 = info_joueur(sock, co_j2)
j2 = Joueur(nom_j2, Plateau(8), 2, co_j2)


close_connection(sock, co_j1, co_j2)
