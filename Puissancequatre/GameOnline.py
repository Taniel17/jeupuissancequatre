import numpy as np
import requests

class GameOnline:
    def __init__(self, player):
        """
        IN : Pseudo du player

        Initialise le jeu,
        crée la matrice,
        crée un index (qui passe de 0 à 1) en fonction du tour du joueur,
        crée une variable booléenne "égalité" par défaut sur false,
        crée une variable booléenne "jeufini" par défaut sur false.
        """
        self.player = player
        self.indexActualPlayer = 0
        self.draw = False
        self.gameEnded = False
        self.tab = np.array([[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]])

        self.url = "https://parseapi.back4app.com/classes"
        self.headers = {
            'X-Parse-Application-Id': 'uuCJGNlERJVe78UBXoXbrzzA4pMEzCbt9RCuchaF',
            'X-Parse-REST-API-Key': 'PGYymQudrbM2gAFFlSFNRK2kjN0GCvuAscqWhVvm',
            'Content-Type': 'application/json',
        }

        self.joint()

    def joint(self):
        """
         IN: self

         Cette méthode est utilisée pour rejoindre une partie en tant que joueur.
         Elle va faire une requête GET pour vérifier la liste des joueur sur le serveur.

         Puis vérifie si il n'y a aucun déja enregistré sur le serveur :
         si non, indice = 1
         si oui, indice = 2

         Ensuite Symbol (1 ou 2) et nom (nom du joueur) sont les données qui vont être envoyé au serveur.

         Enfin, elle va faire une requête POST pour envoyer les infos du joueur au serveur.
        """
        response = requests.request("GET", self.url + "/Players", headers=self.headers).json()["results"]
        if len(response) == 0:
            self.indexActualPlayer = 1
        else:
            self.indexActualPlayer = 2

        data = {
            "Symbol": self.indexActualPlayer,
            "nom": self.player
        }
        requests.request("POST", self.url + "/Players", headers=self.headers, json=data)

    def isFull(self, column):
        """
        IN : self,  column (La colonne a vérifié)
        OUT : Booléan si la colonne est pleine ou non

        Renvoit un True ou False pour savoir si la colonne est pleine ou non.
        """
        return(self.tab[0, column-1] !=0)

    def play(self, X):
        """
        IN : self , X (colonne joué)

        Joue le pion avec de la "gravité", en utilisant une boucle qui explore la colonne jusqu'à trouver un pion existant
        pour avoir la coordonée exacte à utilisé, si il ne trouve pas de pion c'est que la colonne est vide, le valeur
        par défaut est donc 5.
        """
        temp = 5
        for i in range(6):
            if self.tab[i, X-1] != 0 :
                temp = i-1
                break
        self.tab[temp, X-1] = self.indexActualPlayer

    def verif(self):
        """
        IN : self

        OUT : Booléen si oui ou non le jeu est terminé

        Vérifie si le jeu est terminé.
        """
        for i in range(self.tab.shape[0]):
            for j in range(self.tab.shape[1]):
                if self.tab[i][j] != 0:
                    #Column
                    if i <= 2 and self.tab[i][j] == self.tab[i + 1][j] == self.tab[i + 2][j] == self.tab[i + 3][j]:
                        self.gameEnded = True
                        return True
                    #Row
                    if j <= 3 and self.tab[i][j] == self.tab[i][j + 1] == self.tab[i][j + 2] == self.tab[i][j + 3]:
                        self.gameEnded = True
                        return True
                    #Diag right
                    if i <= 2 and j <= 3 and self.tab[i][j] == self.tab[i + 1][j + 1] == self.tab[i + 2][j + 2] == \
                            self.tab[i + 3][j + 3]:
                        self.gameEnded = True
                        return True
                    #Diag left
                    if i <= 2 and j >= 3 and self.tab[i][j] == self.tab[i + 1][j - 1] == self.tab[i + 2][j - 2] == \
                            self.tab[i + 3][j - 3]:
                        self.gameEnded = True
                        return True
        if self.isFull(1) == True and self.isFull(2) == True and \
                self.isFull(3) == True and self.isFull(4) == True and \
                self.isFull(5) == True and self.isFull(6) == True and \
                self.isFull(7) == True:
            self.gameEnded = True
            self.draw = True
            return True
        return False


    def displayTab(self):
        """
        IN : self

        Affiche la matrice dans le terminal.
        """
        print(self.tab)


