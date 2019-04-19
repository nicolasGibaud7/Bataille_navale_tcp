class Coor:
    def __init__(self, x, y):
        self.x = x*2-1
        self.y = y*2
    
class Bateau:
    def __init__(self, longueur, sens, x, y):
        self.vie = longueur
        # Les coordonnées représentent le point le plus en haut à gauche du bateau
        self.coordonnes=Coor(x, y)
        self.cases = []
        compteur = 0
        while compteur < longueur:
            # sens = 1 --> horizontale && sens = 0 --> verticale
            if sens:
                self.cases.append(Coor(x+compteur, y))
            else:
                self.cases.append(Coor(x, y+compteur))
            compteur += 1
    
    def afficher_infos(self):
        print("Coordonnées :", self.coordonnes.x, "-", self.coordonnes.y)
        print("Cases : ")
        for case in self.cases:
            print(case.x,case.y)

    def test_case(self, coordonnees):
        for case in self.cases:
            if case.x == coordonnees.x and case.y == coordonnees.y:
                return True
        return False 


# A1 --> (2,1) ; B5 --> ()