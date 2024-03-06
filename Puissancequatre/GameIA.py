import numpy as np
from random import *
class GameIA:
    def __init__(self, player1, level):
        """
        Initialise la classe
        """
        self.player1 = player1
        self.level = level
        self.indexActualPlayer = 0
        self.gameEnded = False
        self.draw = False
        self.winner = "IA"
        self.tab = np.array([[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]])


    def startGame(self):
        """
        IN : self

        Démarre la partie avec une boucle qui s'éxécute tant que la partie n'est pas fini.
        """
        while (self.verif(self.tab)!=True) :
            self.turn()
            self.verif(self.tab)
            self.displayTab()
            self.indexActualPlayer = (self.indexActualPlayer + 1) % 2
        if self.verif(self.tab) == True :
            print("The winner is", self.winner)

    def turn(self):
        """
        IN : self

        Continue la partie avec une itération qui définit le tour puis une boucle qui permet de choisir la colonne
        où jouer
        """
        if self.indexActualPlayer == 0:
            print("Player ", self.player1, " it's your turn !")
            while True:
                column = int(input("Please enter the column you want to play. (Between 1 and 7)"))
                if column >= 1 and column <= 7 and not self.isFull(column, self.tab):
                    break
            self.play(self.indexActualPlayer+1, column, self.tab)
        else:
            if self.level == 1 :
                self.playLevel1()
            elif self.level == 2:
                self.playLevel2()
            elif self.level == 3:
                self.playLevel3()


    def playLevel1(self):
        while True:
            columnIA = randint(1, 7)
            if self.isFull(columnIA, self.tab) == False:
                break
        self.play(2, columnIA, self.tab)
    def playLevel2(self):
        for col in range(1, 8):
            if self.isFull(col, self.tab) == False:
                temp_tab = np.copy(self.tab)
                self.play(1, col, temp_tab)
                if self.verif(temp_tab) == True:
                    self.play(2, col, self.tab)
                    return
                temp_tab = np.copy(self.tab)
        while True:
            columnIA = randint(1, 7)
            if not self.isFull(columnIA, self.tab):
                break
        self.play(2, columnIA, self.tab)

    def playLevel3(self):
        for col in range(1, 8):
            if self.isFull(col, self.tab) == False:
                temp_tab = np.copy(self.tab)
                self.play(2, col, temp_tab)
                if self.verif(temp_tab) == True:
                    self.play(2, col, self.tab)
                    return
                temp_tab = np.copy(self.tab)
        for col in range(1, 8):
            if self.isFull(col, self.tab) == False:
                temp_tab = np.copy(self.tab)
                self.play(1, col, temp_tab)
                if self.verif(temp_tab) == True:
                    self.play(2, col, self.tab)
                    return
                temp_tab = np.copy(self.tab)
        while True:
            columnIA = randint(1, 7)
            if not self.isFull(columnIA, self.tab):
                break
        self.play(2, columnIA, self.tab)


    def isFull(self, column, mat):
        """
        IN : self,  column
        OUT : Booléan pour colonne pleine

        Renvoit un True ou False pour savoir si la colonne est pleine ou non
        """
        return(mat[0, column-1] !=0)


    def play(self, p, X, mat):
        """
        IN : self , p (pour le pion (1 ou 2) et X (colonne joué)

        Joue le pion avec de la "gravité", en utilisant une boucle qui explore la colonne jusqu'à trouver un pion existant
        pour avoir la coordonée exacte à utilisé, si il ne trouve pas de pion c'est que la colonne est vide, le valeur
        par défaut est donc 5
        """
        temp = 5
        for i in range(6):
            if mat[i, X-1] != 0 :
                temp = i-1
                break
        mat[temp, X-1] = p

    def verif(self, mat):
        """
        Vérifie si le jeu est terminé.
        """
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if mat[i][j] != 0:
                    # Column
                    if i <= 2 and mat[i][j] == mat[i + 1][j] == mat[i + 2][j] == mat[i + 3][j]:
                        self.winner = self.player1 if mat[i][j] == 1 else "IA"
                        return True
                    # Row
                    if j <= 3 and mat[i][j] == mat[i][j + 1] == mat[i][j + 2] == mat[i][j + 3]:
                        self.winner = self.player1 if mat[i][j] == 1 else "IA"
                        return True
                    # Diag right
                    if i <= 2 and j <= 3 and mat[i][j] == mat[i + 1][j + 1] == mat[i + 2][j + 2] == mat[i + 3][j + 3]:
                        self.winner = self.player1 if mat[i][j] == 1 else "IA"
                        return True
                    # Diag left
                    if i <= 2 and j >= 3 and mat[i][j] == mat[i + 1][j - 1] == mat[i + 2][j - 2] == mat[i + 3][j - 3]:
                        self.winner = self.player1 if mat[i][j] == 1 else "IA"
                        return True
        #Cas de draw
        if self.isFull(1, mat) == True and self.isFull(2, mat) == True and\
            self.isFull(3, mat) == True and self.isFull(4, mat) == True and\
            self.isFull(5, mat) == True and self.isFull(6, mat) == True and\
            self.isFull(7, mat) == True:
            self.draw = True
            return(True)
        return False

    def displayTab(self):
        """
        IN :
        OUT :

        Initialise la class
        """
        print(self.tab)