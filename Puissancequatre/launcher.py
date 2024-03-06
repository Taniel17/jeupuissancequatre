import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import gui
import guiIA

def start_game():
    game_type = game_type_var.get()
    player1 = player1_name_var.get()
    player2 = player2_name_var.get()
    ia_level = ia_level_var.get()

    if game_type == "local":
        if not player1 or not player2:
            messagebox.showerror("Erreur", "Veuillez entrer les noms des joueurs.")
            return
        root.destroy()
        gui.start(player1, player2)
    elif game_type == "ia":
        if not player1:
            messagebox.showerror("Erreur", "Veuillez entrer le nom du joueur.")
            return
        root.destroy()
        guiIA.start(player1, ia_level)

def toggle_player2_frame():
    if game_type_var.get() == "local":
        player2_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        ia_frame.grid_remove()
    else:
        ia_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        player2_frame.grid_remove()

def toggle_game_mode():
    if game_type_var.get() == "local":
        local_radio.config(image=checked_icon, bg="#636363")
        ia_radio.config(image=unchecked_icon, bg="#636363")
        player2_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        ia_frame.grid_remove()
    else:
        ia_radio.config(image=checked_icon, bg="#636363")
        local_radio.config(image=unchecked_icon, bg="#636363")
        ia_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        player2_frame.grid_remove()

root = tk.Tk()
root.geometry("350x500")
root.title("Puissance 4")
root.iconbitmap("icone.ico")
root.config(background="#292929")


checked_image = Image.open("checked.png").resize((50, 50))
unchecked_image = Image.open("notchecked.png").resize((50, 50))
checked_icon = ImageTk.PhotoImage(checked_image)
unchecked_icon = ImageTk.PhotoImage(unchecked_image)

game_type_var = tk.StringVar(value="ia")
player1_name_var = tk.StringVar()
player2_name_var = tk.StringVar()
ia_level_var = tk.IntVar()

title_label = tk.Label(root, text="Puissance 4", font=("Arial", 20, "bold"), bg="#292929", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

game_type_frame = tk.LabelFrame(root, text="Choisissez le mode de jeu", bg="#292929", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
game_type_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

local_radio = tk.Radiobutton(game_type_frame, text="Joueur contre Joueur", variable=game_type_var, value="local", command=toggle_game_mode, bg="#292929", fg="black", font=("Arial", 10), indicatoron=False, compound="left")
local_radio.grid(row=0, column=0, sticky="w")
local_radio.config(image=unchecked_icon, bg="#636363")

ia_radio = tk.Radiobutton(game_type_frame, text="Joueur contre IA", variable=game_type_var, value="ia", command=toggle_game_mode, bg="#292929", fg="black", font=("Arial", 10), indicatoron=False, compound="left")
ia_radio.grid(row=1, column=0, sticky="w")
ia_radio.config(image=checked_icon, bg="#636363")

player1_frame = tk.LabelFrame(root, text="Nom du joueur 1", bg="#292929", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
player1_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
tk.Entry(player1_frame, textvariable=player1_name_var, font=("Arial", 10)).pack(fill="x")

player2_frame = tk.LabelFrame(root, text="Nom du joueur 2", bg="#292929", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
player2_entry = tk.Entry(player2_frame, textvariable=player2_name_var, font=("Arial", 10))
player2_entry.pack(fill="x")

ia_frame = tk.LabelFrame(root, text="Paramètres de l'IA", bg="#292929", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
tk.Label(ia_frame, text="Niveau de l'IA : ", bg="#292929", fg="white", font=("Arial", 10)).pack(side="left")
tk.OptionMenu(ia_frame, ia_level_var, *range(1, 4)).pack(side="left")

start_button = tk.Button(root, text="Commencer la partie", command=start_game, bg="#007ACC", fg="white", font=("Arial", 12, "bold"))
start_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

toggle_player2_frame()

root.mainloop()

