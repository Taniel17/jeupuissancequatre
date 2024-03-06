import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import requests
from GameOnline import GameOnline

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
    Crée les tous les bouttons à cliquer pour jouer.
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
    Aussi, affiche le tour du joueur actuel puis affiche celui de l'adversaire
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
        winner = requests.request("GET", game.url + "/Jeu", headers=game.headers).json()["results"][0]["Winner"]

        if game.draw == False:
            messagebox.showinfo("Victory", f"The winner is {winner}")
        else:
            messagebox.showinfo("Draw", "Restart a game to retry")
        root.destroy()
    else:
        if requests.request("GET", game.url + "/Jeu", headers=game.headers).json()["results"][0]["index"] == game.indexActualPlayer:
            turn_label.config(text=f"Au tour de {game.player}")
        else:
            response = requests.request("GET", game.url + "/Players", headers=game.headers).json()["results"]
            if len(response) > 1:
                for i in range(2):
                    if response[i]["Symbol"] != game.indexActualPlayer:
                        turn_label.config(text=f"Au tour de {response[i]["nom"]}")
                        break

def on_button_click(col):
    """
    IN: Colonne cliqué

    Si la colonne n'est pas pleine, elle fait jouer le joueur à la colonne correspondante.
    Met à jour les données sur le serveur.
    Indique le gagnant.
    Enfin, rafraichie la grille.
    """
    if requests.request("GET", game.url + "/Jeu", headers=game.headers).json()["results"][0]["index"] == game.indexActualPlayer:
        if not game.isFull(col+1):
            game.play(col + 1)
            data = {
                "tab": game.tab.tolist(),
                "index": 2 if game.indexActualPlayer == 1 else 1
            }
            objectId = requests.request("GET", game.url + "/Jeu", headers=game.headers).json()["results"][0]["objectId"]
            requests.request("PUT", game.url + "/Jeu" + "/" + objectId, headers=game.headers, json=data)

            game.verif()
            if game.gameEnded:
                data = {
                    "Winner": game.player
                }
                requests.request("PUT", game.url + "/Jeu" + "/" + objectId, headers=game.headers, json=data)
            refresh()

def update():
    """
    Met à jour le jeu.
    Récupère la liste des joueur en ligne.
    Si il y a plus d'un joueur en ligne,
        Met à jour le titre de la page avec les joueurs en ligne
    Récupère la matrice et raffraichis.
    S'éxécute toutes les 5 secondes (5000ms)
    """
    global root
    response = requests.request("GET", game.url + "/Player", headers=game.headers).json()["results"]

    if len(response) > 1:
        player1 = response[0]["nom"]
        player2 = response[1]["nom"]
        root.title(f"Puissance 4 - {player1} vs {player2}")

    game.tab = np.asarray(requests.request("GET", game.url + "/Jeu", headers=game.headers).json()["results"][0]["tab"])
    print(game.tab)
    refresh()
    root.after(5000, update)

def start(player):
    """
    IN: Joueur (issue de l'input du joueur dans la console)

    Crée une partie issu de la class "GameOnline",
    Initialise le tkinter complet (Titre, dimension, le grid, etc).
    """
    global game
    game = GameOnline(player)

    global root, turn_label
    root = tk.Tk()
    root.title("Puissance 4")
    turn_label = tk.Label(root, text="", font=("Helvetica", 12))
    turn_label.grid(row=0, columnspan=7)

    create_buttons()
    create_grid()

    refresh()
    update()
    root.mainloop()

userInput = str(input("Nom : "))
start(userInput)