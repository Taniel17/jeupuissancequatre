import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from GameIA import GameIA

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)

def create_buttons():
    for i in range(7):
        button = tk.Button(root, text="⬇", width=12, height=2, bg="white", command=lambda col=i: on_button_click(col))
        button.grid(row=0, column=i)

def create_grid():
    global empty_image, red_image, yellow_image
    empty_image = resize_image("empty.png", 100, 100)
    red_image = resize_image("red.png", 100, 100)
    yellow_image = resize_image("yellow.png", 100, 100)
    for i in range(6):
        for j in range(7):
            square = tk.Label(root, bg="#000000", image=empty_image, borderwidth=0, highlightthickness=0)
            square.grid(row=i + 2, column=j, padx=0, pady=0)

def refresh():
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

    if game.verif(game.tab) == True:
        if game.draw == False :
            messagebox.showinfo("Victory", f"The winner is {game.winner}")
        else:
            messagebox.showinfo("Draw", "Restart a game to retry")
        root.destroy()

def on_button_click(col):
    if not game.isFull(col+1, game.tab):
        game.play(1, col+1, game.tab)
        if game.level == 1:
            game.playLevel1()
        elif game.level == 2:
            game.playLevel2()
        elif game.level == 3:
            game.playLevel3()
        refresh()

def start(player1, level):
    global game
    game = GameIA(player1, level)

    global root
    root = tk.Tk()
    root.title(f"Puissance 4 - {game.player1} vs IA level {game.level}")


    global empty_image, red_image, yellow_image
    empty_image = resize_image("empty.png", 100, 100)
    red_image = resize_image("red.png", 100, 100)
    yellow_image = resize_image("yellow.png", 100, 100)


    create_buttons()
    create_grid()

    root.mainloop()
