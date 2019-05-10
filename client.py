import socket
import os
import joueur
import pickle

def connection():
    hote = "localhost"
    port = 12800
    no_joueur = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    print("Connexion avec le serveur")

    msg_recv = sock.recv(10)
    print(msg_recv.decode()+'\n')
    if "J1" in msg_recv.decode():
        no_joueur = False
        msg_recv = sock.recv(23)
        print(msg_recv.decode()+'\n')
        msg_recv = sock.recv(15)
        print(msg_recv.decode()+'\n')
    else:
        no_joueur = True
    msg_recv = sock.recv(24)
    print(msg_recv.decode()+'\n')

    return sock, no_joueur

def info_joueur(sock):
    msg_recv = sock.recv(1)
    nom = input("Pseudo : ")
    sock.send(nom.encode())
    msg_recv = sock.recv(7)
    print(msg_recv.decode())

    return nom

def creation_joueur(sock):
    
    compteur = 2
    while compteur:

        msg_recv = sock.recv(1024)
        print(msg_recv.decode())
        sock.send(b'1')

        # Affichage du plateau
        plateau = sock.recv(1024)
        plateau = pickle.loads(plateau)
        plateau.afficher()
        sock.send(b'1')

        # Récupération du sens du bateau
        msg_recv = sock.recv(1024)
        sens = input(msg_recv.decode())
        sock.send(sens.encode())

        # Récupération des coordonnées du bateau
        msg_recv = sock.recv(1024)
        coor = input(msg_recv.decode())
        sock.send(coor.encode())

        # Affichage erreur ou pas
        msg_recv = sock.recv(1024)
        print(msg_recv.decode())
        sock.send(b'1')

        # Gestion du compteur
        if "Succes" in msg_recv.decode():
            compteur -= 1
        else:
            print("Dommage ! On va retenter ça \n")
        
        # os.system("clear")


def attaque(sock, pseudo):
    
    print("===== Attaque ====")
        
    # Affichage du plateau
    plateau = sock.recv(1024)
    plateau = pickle.loads(plateau)
    plateau.afficher()

    # Récupération des coordonnées d'attaque
    attaque = input("{}, à quelle position se trouve votre attaque ? ".format(pseudo))
    sock.send(attaque.encode())

    # Récupération du résultat de l'attaque
    res_attq = sock.recv(1024)
    print(res_attq.decode())

    # Fin du tour

def partie(sock, pseudo, etat_attaque):
    
    etat_partie = True
    
    while etat_partie: 
        if etat_attaque:
            attaque(sock, pseudo)
            etat_attaque = False
        else:
            res_attq = sock.recv(1024)
            print(res_attq.decode())
            sock.send(b"a")
            etat_attaque = True
        msg_end = sock.recv(10)
        if "end" in msg_end.decode():
            etat_partie = False

sock, no_joueur = connection()

pseudo = info_joueur(sock)
creation_joueur(sock)

if no_joueur:
    print("J2")
else:
    print("J1")

partie(sock, pseudo, no_joueur)
etat_win = sock.recv(5)

if "win" in etat_win.decode():
    print("Bien joué {}, vous avez gagné !".format(pseudo))
else:
    print("Dommage loser , c'est une défaite cuisante")
