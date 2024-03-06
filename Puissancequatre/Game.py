import numpy as np
class Game:
    def __init__(self, player1, player2):
        """
        IN : Pseudo du player1 puis pseudo du player2

        Initialise le jeu,
        crée la matrice,
        crée un index (qui passe de 0 à 1) en fonction du tour du joueur,
        crée une variable booléenne "égalité" par défaut sur false,
        crée une variable booléenne "jeufini" par défaut sur false.
        """
        self.player1 = player1
        self.player2 = player2
        self.indexActualPlayer = 0
        self.draw = False
        self.gameEnded = False
        self.tab = np.array([[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]])
        #print("Game start !")
        # self.displayTab()
        # self.startGame()



    def startGame(self):
        """
        IN : self

        Démarre la partie avec une boucle qui s'éxécute tant que la partie n'est pas fini.
        """
        while (self.gameEnded == False) :
            self.turn()
            self.verif()
            self.displayTab()
            self.indexActualPlayer = (self.indexActualPlayer + 1) % 2
        #if self.indexActualPlayer == 1 :
            #print("The winner is", self.player1)
        #else :
            #print("The winner is", self.player2)

    def turn(self):
        """
        IN : self

        Joue le tour du joueur correspondant,
        demmande la colonne a joué.

        """
        #if self.indexActualPlayer == 0:
            #print("Player ", self.player1, " it's your turn !")
        #else:
            #print("Player ", self.player2, " it's your turn !")
        while True:
            column = int(input("Please enter the column you want to play. (Between 1 and 7)"))
            if column >= 1 and column <= 7 and not self.isFull(column):
                break
        self.play(column)

    def isFull(self, column):
        """
        IN : self,  column
        OUT : Booléan si colonne pleine ou non

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
        self.tab[temp, X-1] = self.indexActualPlayer+1

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



