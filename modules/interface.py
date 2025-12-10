from tkinter import *

#Interface graphique    chatgpt
class Interface(Tk):
    def __init__(self, chapitres_dict=None, callbacks=None):
        super().__init__()
        self.chapitres = chapitres_dict or {}
        # callbacks: dict avec 'quizz', 'flashcards', 'gestion', 'quit'
        self.callbacks = callbacks or {}
        self.config_fenetre()
        self.creer_widgets()
        # thèmes
        self.themes = {
            "light": {
                "bg": "#5AEBFC",
                "fg": "#1749B3",
                "button_bg": "#ffffff",
                "button_fg": "#1749B3",
                "small_btn_bg": "#1749B3",
                "small_btn_fg": "#ffffff",
            },
            "dark": {
                "bg": "#000F3B",
                "fg": "#E8F6FF",
                "button_bg": "#1749B3",
                "button_fg": "#E8F6FF",
                "small_btn_bg": "#E8F6FF",
                "small_btn_fg": "#000F3B",
            }
        }
        self.current_theme = "light"

#configuration de base de la fenetre
    def config_fenetre(self):
        self.title("Jean Révise")
        self.geometry("1080x720")
        self.minsize(480, 360)
        #self.iconbitmap("../img/logos/jeanReviseLogo.ico")
        self.config(background='#5AEBFC')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

#ajout du texte, boutons, etc...
    def creer_widgets(self):
        self.center_frame = Frame(self, padx=20, pady=20)
        self.center_frame.grid(row=0, column=0, sticky="nsew")
        self.center_frame.grid_rowconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)

         # Un frame pour centrer verticalement/horizontalement
        self.inner = Frame(self.center_frame)
        self.inner.place(relx=0.5, rely=0.5, anchor="center")

        btn_font = ("Helvetica", 20, "bold")
        btn_width = 24
        btn_height = 2

        # Quatre gros boutons centraux
        self.btn_quiz = Button(self.inner, text="Quiz", font=btn_font, width=btn_width, height=btn_height, command=self.open_quiz)
        self.btn_flash = Button(self.inner, text="Flashcards", font=btn_font, width=btn_width, height=btn_height, command=self.open_flashcards)
        self.btn_gestion = Button(self.inner, text="Gérer chapitres", font=btn_font, width=btn_width, height=btn_height, command=self.open_gestion)
        self.btn_quitter = Button(self.inner, text="Quitter", font=btn_font, width=btn_width, height=btn_height, command=self.quit_app)

        # Empilement vertical avec espaces
        self.btn_quiz.pack(pady=(0, 12))
        self.btn_flash.pack(pady=(0, 12))
        self.btn_gestion.pack(pady=(0, 12))
        self.btn_quitter.pack()

        # petit bouton bas-droite pour bascule thème
        self.toggle_btn = Button(self, text="Mode sombre", font=("Helvetica", 9), width=12, command=self.toggle_theme)
        # place en bas droite avec marge
        self.toggle_btn.place(relx=1.0, rely=1.0, anchor="se", x=-12, y=-12)

        # garder listes pour appliquer thème facilement
        self._big_buttons = [self.btn_quiz, self.btn_flash, self.btn_gestion, self.btn_quitter]
        self._all_widgets = [self, self.center_frame, self.inner] + self._big_buttons + [self.toggle_btn]

    def apply_theme(self):
        t = self.themes[self.current_theme]
        # fenêtre de fond
        try:
            self.configure(bg=t["bg"])
        except Exception:
            pass

        # centre et inner
        self.center_frame.configure(bg=t["bg"])
        self.inner.configure(bg=t["bg"])

        # label/button styles
        for b in self._big_buttons:
            b.configure(bg=t["button_bg"], fg=t["button_fg"], activebackground=t["button_bg"], activeforeground=t["button_fg"], bd=0, highlightthickness=0)

        self.toggle_btn.configure(bg=t["small_btn_bg"], fg=t["small_btn_fg"], activebackground=t["small_btn_bg"], activeforeground=t["small_btn_fg"], bd=0)

        # mettre à jour le texte du toggle
        if self.current_theme == "light":
            self.toggle_btn.configure(text="Mode sombre")
        else:
            self.toggle_btn.configure(text="Mode clair")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    # Placeholder callbacks — remplacez par intégration avec votre logique
    def open_quiz(self):
        cb = self.callbacks.get('quizz')
        if callable(cb):
            cb()   # appelle la fonction quizz() dans main.py
        else:
            print("Ouvrir Quiz (à connecter)")

    def open_flashcards(self):
        cb = self.callbacks.get('flashcards')
        if callable(cb):
            cb()
        else:
            print("Ouvrir Flashcards (à connecter)")

    def open_gestion(self):
        cb = self.callbacks.get('gestion')
        if callable(cb):
            cb()
        else:
            print("Ouvrir Gestion Chapitres (à connecter)")

    def quit_app(self):
        self.destroy()

#ajout d'évenements de clavier et souris
    def creer_bindings(self):
        pass

if __name__ == "__main__":
    appli = Interface()
    appli.mainloop()