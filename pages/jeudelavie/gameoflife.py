import tkinter
from tkinter import ttk
from tkinter import NORMAL, DISABLED
from array import array


class MatriceLongue:
    def __init__(self, largeur: int, hauteur: int):
        self.donnees = array('L', (0 for i in range(largeur*hauteur)))
        self.largeur = largeur
        self.hauteur = hauteur

    def _verifier_limites(self, ligne: int, colonne: int):
        if not (0 <= ligne < self.hauteur):
            raise IndexError(f'indice de ligne hors limites pour la matrice {self.largeur}x{self.hauteur} : {ligne}')

        if not (0 <= colonne < self.largeur):
            raise IndexError(f'indice de colonne hors limites pour la matrice {self.largeur}x{self.hauteur} : {colonne}')

    def __getitem__(self, ligne_colonne: tuple[int, int]) -> int:
        ligne = ligne_colonne[0]
        colonne = ligne_colonne[1]
        self._verifier_limites(ligne, colonne)
        return self.donnees[ligne*self.largeur + colonne]

    def __setitem__(self, ligne_colonne: tuple[int, int], valeur: int):
        ligne = ligne_colonne[0]
        colonne = ligne_colonne[1]
        self._verifier_limites(ligne, colonne)
        self.donnees[ligne*self.largeur + colonne] = valeur


class CommandeRepetee:
    """Appelle une fonction de manière répétée à un certain intervalle sans saturer la boucle d'événements."""
    def __init__(self,
                 racine: tkinter.Tk,
                 intervalle_ms: int,
                 fonction,
                 *args,
                 **kwargs):
        self.racine = racine
        self.intervalle = str(intervalle_ms)
        self.commande_inactive = racine.register(self.planifier_inactive)
        self.commande_intervalle = racine.register(self.planifier_intervalle)
        self.handle = None
        self.fonction = fonction
        self.args = args
        self.kwargs = kwargs

    def demarrer(self):
        self.handle = self.racine.call('after', 'idle', self.commande_intervalle)

    def annuler(self):
        self.racine.call('after', 'cancel', self.handle)
        self.handle = None

    def planifier_inactive(self):
        self.fonction(*self.args, **self.kwargs)
        self.handle = self.racine.call('after', 'idle', self.commande_intervalle)

    def planifier_intervalle(self):
        self.handle = self.racine.call('after', self.intervalle, self.commande_inactive)


class JeuDeLaVie:
    def __init__(self,
                 titre: str = 'Jeu de la Vie',
                 taille_pixel: tuple[int, int] = (1000, 500),
                 taille_grille: tuple[int, int] = (50, 25),
                 pas_ms: int = 250):
        self.pas_ms = pas_ms
        self.taille_grille = taille_grille
        self.racine = tkinter.Tk()
        self.racine.title(titre)
        self.largeur_ecran = self.racine.winfo_screenwidth()
        self.hauteur_ecran = self.racine.winfo_screenheight()
        # centrer la fenêtre
        self.racine.geometry(
            f'+{(self.largeur_ecran - taille_pixel[0]) // 2}'
            f'+{(self.hauteur_ecran - taille_pixel[1]) // 2}'
        )
        self.largeur_canvas = taille_pixel[0]
        self.hauteur_canvas = taille_pixel[1]
        self.contenu = ttk.Frame()
        self.contenu.grid()

        self.canvas = tkinter.Canvas(self.racine,
                                     width=self.largeur_canvas + 2,
                                     height=self.hauteur_canvas + 2,
                                     highlightthickness=0)
        self.canvas.config(background='white')
        self.canvas.bind('<Button-1>', self.toggle_cell)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.bouton_start_stop = ttk.Button(text='Démarrer', command=self.démarrer_arrêter)
        self.bouton_start_stop.grid(row=1, column=0)
        self.en_cours = False

        self.bouton_reset = ttk.Button(text='Réinitialiser', command=self.reset, state=DISABLED)
        self.bouton_reset.grid(row=1, column=1)

        # chaque cellule du jeu correspond à un rectangle sur le canvas.
        self.largeur_cellule = taille_pixel[0] / taille_grille[0]
        self.hauteur_cellule = taille_pixel[1] / taille_grille[1]
        # La grille a trois lignes et colonnes hors écran de chaque côté pour garantir
        # que les motifs visibles se propagent correctement. Les cellules en dehors de la grille
        # sont toujours considérées comme mortes.
        self.cellules = MatriceLongue(taille_grille[0] + 6, taille_grille[1] + 6)
        bits_id = self.cellules.donnees.itemsize * 8 - 2
        for y in range(taille_grille[1] + 6):
            for x in range(taille_grille[0] + 6):
                tkid = self.canvas.create_rectangle(
                    (x - 3)*self.largeur_cellule + 1,
                    (y - 3)*self.hauteur_cellule + 1,
                    (x - 2)*self.largeur_cellule + 1,
                    (y - 2)*self.hauteur_cellule + 1,
                    width=2,
                    fill='white',
                    outline='grey'
                )
                # le bit du bas est l'état actuel,
                # le bit suivant est l'état suivant,
                # le reste des bits est l'id
                if tkid.bit_length() > bits_id:
                    raise ValueError("id de l'élément canvas trop grand !")
                self.cellules[y, x] = tkid << 2

        self.repeateur_pas = CommandeRepetee(self.racine, self.pas_ms, self.pas)

    def lancer(self):
        self.racine.mainloop()

    def toggle_cell(self, e: tkinter.Event):
        ligne = int(e.y // self.hauteur_cellule) + 3
        colonne = int(e.x // self.largeur_cellule) + 3
        cellule = self.cellules[ligne, colonne]
        if cellule & 1:  # la cellule est vivante
            cellule &= ~1  # effacer le bit du bas
            self.canvas.itemconfigure(cellule >> 2, fill='white')
        else:
            cellule |= 1  # définir le bit du bas
            self.canvas.itemconfigure(cellule >> 2, fill='black')
        self.cellules[ligne, colonne] = cellule

    def reset(self):
        for ligne in range(self.cellules.hauteur):
            for colonne in range(self.cellules.largeur):
                self.cellules[ligne, colonne] &= ~3  # effacer les deux derniers bits
                self.canvas.itemconfigure(self.cellules[ligne, colonne] >> 2, fill='white')

    def démarrer_arrêter(self):
        if self.en_cours:
            self.bouton_start_stop['text'] = 'Démarrer'
            self.bouton_reset['state'] = NORMAL
            self.repeateur_pas.annuler()
            self.en_cours = False
        else:
            self.bouton_start_stop['text'] = 'Arrêter'
            self.bouton_reset['state'] = DISABLED
            self.repeateur_pas.demarrer()
            self.en_cours = True

    def pas(self):
        voisins_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]
        for y in range(self.cellules.hauteur):
            for x in range(self.cellules.largeur):
                compteur_voisins = 0
                cette_cellule = self.cellules[y, x]
                # compter le nombre de voisins vivants pour cette cellule
                for x_offset, y_offset in voisins_offsets:
                    voisin_x = x + x_offset
                    voisin_y = y + y_offset
                    # tous les voisins qui sont hors de la grille sont considérés comme morts
                    if voisin_x < 0 or voisin_y < 0:
                        continue
                    if self.cellules.largeur <= voisin_x or self.cellules.hauteur <= voisin_y:
                        continue
                    compteur_voisins += self.cellules[voisin_y, voisin_x] & 1

                if cette_cellule & 1:
                    if 2 <= compteur_voisins <= 3:
                        cette_cellule |= 2  # définir le deuxième bit
                    else:
                        cette_cellule &= ~2  # effacer le deuxième bit
                else:
                    if compteur_voisins == 3:
                        cette_cellule |= 2
                    else:
                        cette_cellule &= ~2

                if cette_cellule & 2:
                    self.canvas.itemconfigure(cette_cellule >> 2, fill='black')
                else:
                    self.canvas.itemconfigure(cette_cellule >> 2, fill='white')

                self.cellules[y, x] = cette_cellule

        for ligne in range(self.cellules.hauteur):
            for colonne in range(self.cellules.largeur):
                cette_cellule = self.cellules[ligne, colonne]
                # cette_cellule & ~3 efface les deux derniers bits
                self.cellules[ligne, colonne] = (cette_cellule & ~3) | ((cette_cellule & 2) >> 1)


if __name__ == '__main__':
    JeuDeLaVie().lancer()
