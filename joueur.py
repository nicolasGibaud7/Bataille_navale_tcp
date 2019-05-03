from plateau import *
from bateau import *
import os
import pickle

class Joueur:
    def __init__(self, nom, plateau, nb_bateau, co_j):
        self.nom = nom
        self.plateau = plateau
        self.bateaux = []
        self.nb_bateau = nb_bateau
        compteur = 0
        alpha = "abcdefghijklmnopqrstuvwxyz"
        while compteur < nb_bateau:
            test_bateau = False
            #self.plateau.afficher()
            co_j.send(b"=== Positionnement bateau ===")
            co_j.recv(1)
            plateau_b = pickle.dumps(self.plateau)
            co_j.send(plateau_b)
            co_j.recv(1)
            co_j.send(b"Sens ? (0 : Verticale - 1 : Horizontale ) : ")
            sens = co_j.recv(1).decode()
            co_j.send(b"Coordonnees du bateau ? ")
            coordonnees = co_j.recv(2).decode()
            x=alpha.index(coordonnees[0].lower())
            y=int(coordonnees[1])
            coordonnees_test=Coor(x,y)
            # Test si y a la place sur le plateau
            if ( x+1 > self.plateau.taille-2 and sens == '1') or (y > (self.plateau.taille-2) and sens == '0' ):
                co_j.send(b"Pas la place")
            else:
                # Test si y a déjà un bateau à cet emplacement
                for bateau in self.bateaux:
                    for case in bateau.cases:
                        if coordonnees_test.x== case.x and coordonnees_test.y == case.y:
                            co_j.send(b"Erreur, il y a deja un bateau ici")
                            test_bateau=True
                    if test_bateau:
                        break
                else:
                    self.bateaux.append(Bateau(3, int(sens), alpha.index(coordonnees[0].lower())+1, int(coordonnees[1])))
                    self.bateaux[compteur].afficher_infos()
                    co_j.send(b"Succes : Bateau ajoute")
                    co_j.recv(1)
                    compteur += 1

    def is_attacked(self, coordonnees, autre_joueur, co_j_att, co_j_is_att):
        for index, bateau in enumerate(self.bateaux):
            if bateau.test_case(coordonnees):
                self.bateaux[index].vie -= 1  
                autre_joueur.plateau.plateau[coordonnees.y] = autre_joueur.plateau.plateau[coordonnees.y][:coordonnees.x] + 'X' + autre_joueur.plateau.plateau[coordonnees.y][coordonnees.x+1:]
                if self.bateaux[index].vie == 0:
                    self.nb_bateau -= 1
                    co_j_att.send(b"ca touche et ca coule ")
                    co_j_is_att.send(b"ca touche et ca coule, cest chaud")
                else:
                    co_j_att.send(b"ca touche ")
                    co_j_is_att.send(b"ca touche attention")
                break
        else:
            co_j_att.send(b"ca touche pas, dommage")
            co_j_is_att.send(b"hop, tranquille, ca touche pas")
            autre_joueur.plateau.plateau[coordonnees.y] = autre_joueur.plateau.plateau[coordonnees.y][:coordonnees.x] + 'O' + autre_joueur.plateau.plateau[coordonnees.y][coordonnees.x+1:]

    def enregistrer_infos_joueurs(self, nom_fichier):
        with open(nom_fichier, 'a', encoding='utf-8') as mon_fichier:
            for bateau in self.bateaux :
                ligne = ""
                for case in bateau.case:
                    ligne += str(case.x) + ' - ' + str(case.y) + '\n'
                mon_fichier.write(ligne)