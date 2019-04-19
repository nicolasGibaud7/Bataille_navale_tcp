from plateau import *
from bateau import *
import os

class Joueur:
    def __init__(self, nom, plateau, nb_bateau):
        self.nom = nom
        self.plateau = plateau
        self.bateaux = []
        self.nb_bateau = nb_bateau
        compteur = 0
        alpha = "abcdefghijklmnopqrstuvwxyz"
        while compteur < nb_bateau:
            test_bateau = False
            self.plateau.afficher()
            print("=== Positionnement bateau", compteur+1, "===")
            sens = input("Sens ? (0 : Verticale - 1 : Horizontale ) : ")
            coordonnees = input("Coordonnées du bateau ? (Point le plus en haut à gauche du bateau -- ex : A4) : ")
            x=alpha.index(coordonnees[0].lower())
            y=int(coordonnees[1])
            coordonnees_test=Coor(x,y)
            # Test si y a la place sur le plateau
            if ( x+1 > self.plateau.taille-2 and sens == '1') or (y > (self.plateau.taille-2) and sens == '0' ):
                print("Pas la place")
            else:
                # Test si y a déjà un bateau à cet emplacement
                for bateau in self.bateaux:
                    for case in bateau.cases:
                        if coordonnees_test.x== case.x and coordonnees_test.y == case.y:
                            print("Erreur, il y a déjà un bateau ici")
                            test_bateau=True
                    if test_bateau:
                        break
                else:
                    self.bateaux.append(Bateau(3, int(sens), alpha.index(coordonnees[0].lower())+1, int(coordonnees[1])))
                    self.bateaux[compteur].afficher_infos()
                    compteur += 1
                    os.system("clear")

    def is_attacked(self, coordonnees, autre_joueur):
        for index, bateau in enumerate(self.bateaux):
            if bateau.test_case(coordonnees):
                self.bateaux[index].vie -= 1  
                print("Touché !")
                autre_joueur.plateau.plateau[coordonnees.y] = autre_joueur.plateau.plateau[coordonnees.y][:coordonnees.x] + 'X' + autre_joueur.plateau.plateau[coordonnees.y][coordonnees.x+1:]
                if self.bateaux[index].vie == 0:
                    self.nb_bateau -= 1
                    print("Coulé !!!")
                break
        else:
            print("Pas touché ...")
            autre_joueur.plateau.plateau[coordonnees.y] = autre_joueur.plateau.plateau[coordonnees.y][:coordonnees.x] + 'O' + autre_joueur.plateau.plateau[coordonnees.y][coordonnees.x+1:]

    def enregistrer_infos_joueurs(self, nom_fichier):
        with open(nom_fichier, 'a', encoding='utf-8') as mon_fichier:
            for bateau in self.bateaux :
                ligne = ""
                for case in bateau.cases:
                    ligne += str(case.x) + ' - ' + str(case.y) + '\n'
                mon_fichier.write(ligne)