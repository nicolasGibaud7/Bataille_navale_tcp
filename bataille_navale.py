from joueur import *
import socket

alpha = "abcdefghijklmnopqrstuvwxyz"

print("Bonjour, bienvenue sur ce jeu incroyable de bataille navale ! ")
print("Ceci sera une partie en 2 bateaux de taille 3.")
nom = input("Nom joueur 1 ?  ")
un_plateau = Plateau(8)

joueur_1 = Joueur(nom, un_plateau, 2)
tour=1


nom = input("Nom joueur 2 ?  ")
un_autre_plateau = Plateau(8)
joueur_2 = Joueur(nom, un_autre_plateau, 2)

while joueur_1.nb_bateau != 0 and joueur_2.nb_bateau != 0:
    if tour == 1:
        joueur_1.plateau.afficher()
        attaque = input("{}, à quelle position se trouve votre attaque ? ".format(joueur_1.nom))
        joueur_2.is_attacked(Coor(alpha.index(attaque[0].lower())+1,int(attaque[1])), joueur_1)
        tour += 1
    elif tour == 2 :
        joueur_2.plateau.afficher()
        attaque = input("{}, à quelle position se trouve votre attaque ? ".format(joueur_2.nom))
        joueur_1.is_attacked(Coor(alpha.index(attaque[0].lower())+1,int(attaque[1])), joueur_2)
        tour -= 1
       
if joueur_1.nb_bateau:
    print("Victoire de {} ! Quel chance incroyable alors que son adversaire {} était vraiment très fort".format(joueur_1.nom, joueur_2.nom))
else:
    print("Victoire de {} !!!! {} s'est fait écraser ...".format(joueur_2.nom, joueur_1.nom))

joueur_1.enregistrer_infos_joueurs("/home/nicolas/python/bataille_navalle_udp/coordonnees")
joueur_2.enregistrer_infos_joueurs("/home/nicolas/python/bataille_navalle_udp/coordonnees")