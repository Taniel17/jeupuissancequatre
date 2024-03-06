import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Game import Game

def resize_image(image_path, width, height):
    """
    IN: L'image, la hauteur et la largeur
    OUT: L'image redimensionnée

    Redimensionne une image.
    """
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)

def create_buttons():
    """
    Crée les tous les bouttons à cliquer pour jouer
    """
    for i in range(7):
        button = tk.Button(root, text="⬇", width=12, height=2, bg="white", command=lambda col=i: on_button_click(col))
        button.grid(row=1, column=i)

def create_grid():
    """
    Crée la grille complète de jeu.
    """
    global empty_image, red_image, yellow_image
    empty_image = resize_image("empty.png", 100, 100)
    red_image = resize_image("red.png", 100, 100)
    yellow_image = resize_image("yellow.png", 100, 100)
    for i in range(6):
        for j in range(7):
            square = tk.Label(root, bg="#000000", image=empty_image, borderwidth=0, highlightthickness=0)
            square.grid(row=i + 2, column=j, padx=0, pady=0)

def refresh():
    """
    Raffraichi la grille de jeu
    en mettant l'image du pion jaune aux endroits ou le joueur1 à joué
    et un pion rouge aux endroits où le joueur2 à joué.
    Vérifie aussi si le jeu n'est pas finis (gagnant ou égalité).
    """
    for i in range(6):
        for j in range(7):
            if game.tab[i][j] == 0:
                image = empty_image
            elif game.tab[i][j] == 1:
                image = yellow_image
            elif game.tab[i][j] == 2:
                image = red_image


            square = tk.Label(root, bg="#000000", image=image, borderwidth=0, highlightthickness=0)
            square.grid(row=i + 2, column=j)
            square.image = image

    game.verif()
    if game.gameEnded:
        if game.draw == False :
            if game.indexActualPlayer == 0:
                messagebox.showinfo("Victory", f"The winner is {game.player2}")
            else:
                messagebox.showinfo("Victory", f"The winner is {game.player1}")
        else:
            messagebox.showinfo("Draw", "Restart a game to retry")
        root.destroy()
    else:
        if game.indexActualPlayer == 0:
            turn_label.config(text=f"Au tour de {game.player1}")
        else:
            turn_label.config(text=f"Au tour de {game.player2}")

def on_button_click(col):
    """
    IN: Colonne cliqué

    Si la colonne n'est pas pleine, elle fait jouer le joueur à la colonne correspondante.
    """
    if not game.isFull(col+1):
        game.play(col + 1)
        game.indexActualPlayer = (game.indexActualPlayer + 1) % 2
        refresh()

def start(player1, player2):
    """
    IN: Pseudo du joueur1, pseudo du joueur2

    Démarre le tkinter complet,
    initialise la page tkinter complète,
    crée la partie issue de la class "Game" avec le player1 et player2
    """
    global game
    game = Game(player1, player2)

    global root, turn_label
    root = tk.Tk()
    root.title(f"Puissance 4 - {game.player1} vs {game.player2}")
    turn_label = tk.Label(root, text="", font=("Helvetica", 12))
    turn_label.grid(row=0, columnspan=7)

    create_buttons()
    create_grid()

    refresh()
    root.mainloop()
