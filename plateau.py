class Plateau:
    
    def __init__(self, cote):
        self.plateau = []
        self.taille = cote
        lignes = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        colonnes = "123456789"
        cpt = 0
        cpt_ligne=0
        ligne= ""
        while cpt_ligne < cote:
            ligne+= ' ' + lignes[cpt_ligne]
            cpt_ligne += 1
        
        self.plateau.append(ligne)
        while cpt < cote:
            self.plateau.append("--"*cote + '-')
            self.plateau.append("| "*cote + '| '+ colonnes[cpt])
            cpt+=1
        self.plateau.append("--"*cote+'-')
        self.liste_coups=[]

    def afficher(self):
        for ligne in self.plateau:
            for carac in ligne:
                print(carac, end="")
            print()
