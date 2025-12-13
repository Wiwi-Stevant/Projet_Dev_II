from tkinter import *
from tkinter import messagebox
import os

from modules.chapitre import Chapitres
from modules.quiz import Quiz
from modules.flashCard import FlashCards

"""
GUI FINAL – VERSION A (UN SEUL FICHIER)
Esthétique inspirée de la V1 fournie (Jean Révise)
Logique complètement connectée à TES classes.
"""

# =====================
# APPLICATION PRINCIPALE
# =====================
class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Jean Révise")
        self.geometry("1080x720")
        self.minsize(600, 400)

        # données
        self.chapitres = {}
        self.quiz = None
        self.flashcards = None
        self.carte_actuelle = None

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

        self.charger_chapitres()
        self.creer_widgets()
        self.apply_theme()

    # =====================
    # CHARGEMENT DES CHAPITRES
    # =====================
    def charger_chapitres(self):
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        for file in os.listdir(data_dir):
            if file.endswith(".json"):
                nom = file.replace(".json", "")
                chap = Chapitres(nom)
                chap.charger_cartes()
                self.chapitres[nom] = chap

    # =====================
    # WIDGETS
    # =====================
    def creer_widgets(self):
        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)
        # ensure the single grid cell containing frames expands so child frames
        # can be centered within the window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuPrincipal, QuizView, FlashcardView, GestionChapitreView):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # bouton thème
        self.toggle_btn = Button(self, text="Mode sombre", command=self.toggle_theme)
        self.toggle_btn.place(relx=1.0, rely=1.0, anchor="se", x=-12, y=-12)

        self.show_frame("MenuPrincipal")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.actualiser()
        frame.tkraise()

    # =====================
    # THÈMES
    # =====================
    def apply_theme(self):
        t = self.themes[self.current_theme]
        self.configure(bg=t["bg"])
        self.container.configure(bg=t["bg"])

        for frame in self.frames.values():
            frame.apply_theme(t)

        self.toggle_btn.configure(bg=t["small_btn_bg"], fg=t["small_btn_fg"], bd=0)
        self.toggle_btn.configure(text="Mode sombre" if self.current_theme == "light" else "Mode clair")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()


# =====================
# MENU PRINCIPAL
# =====================
class MenuPrincipal(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # center everything in this frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.center = Frame(self)
        self.center.grid(row=0, column=0)

        self.title_label = Label(self.center, text="Menu Principal", font=("Helvetica", 32, "bold"))
        self.title_label.pack(pady=30)

        self.inner = Frame(self.center)
        self.inner.pack(expand=True)

        btn_font = ("Helvetica", 20, "bold")
        self.btn_quiz = Button(self.inner, text="Quiz", font=btn_font, command=lambda: app.show_frame("QuizView"))
        self.btn_flash = Button(self.inner, text="Flashcards", font=btn_font, command=lambda: app.show_frame("FlashcardView"))
        self.btn_gestion = Button(self.inner, text="Gérer chapitres", font=btn_font, command=lambda: app.show_frame("GestionChapitreView"))
        self.btn_quitter = Button(self.inner, text="Quitter", font=btn_font, command=app.destroy)

        for i in range(2):
            self.inner.grid_columnconfigure(i, weight=1)
            self.inner.grid_rowconfigure(i, weight=1)

        self.btn_quiz.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.btn_flash.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.btn_gestion.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.btn_quitter.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.buttons = [self.btn_quiz, self.btn_flash, self.btn_gestion, self.btn_quitter]

    def actualiser(self):
        pass

    def apply_theme(self, t):
        self.configure(bg=t["bg"])
        self.center.configure(bg=t["bg"])
        self.inner.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        for b in self.buttons:
            b.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)


# =====================
# QUIZ
# =====================
class QuizView(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # center everything in this frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.center = Frame(self)
        self.center.grid(row=0, column=0)

        self.title_label = Label(self.center, text="Quiz", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=20)

        self.liste = Listbox(self.center, height=6)
        self.liste.pack(pady=10)

        self.question = Label(self.center, text="", wraplength=800, font=("Helvetica", 16))
        self.question.pack(pady=20)

        self.reponse = Entry(self.center, width=40)
        self.reponse.pack()

        self.btn_valider = Button(self.center, text="Valider", command=self.valider)
        self.btn_lancer = Button(self.center, text="Lancer", command=self.lancer)
        self.btn_retour = Button(self.center, text="Retour", command=lambda: app.show_frame("MenuPrincipal"))

        self.btn_lancer.pack(pady=5)
        self.btn_valider.pack(pady=5)
        self.btn_retour.pack(pady=20)

    def actualiser(self):
        self.liste.delete(0, END)
        for nom in self.app.chapitres:
            self.liste.insert(END, nom)
        

    def lancer(self):
        nom = self.liste.get(ACTIVE)
        self.app.quiz = Quiz(self.app.chapitres[nom])
        self.app.carte_actuelle = self.app.quiz.tirer_cartes()
        self.question.config(text=self.app.carte_actuelle.question)

    def valider(self):
        carte = self.app.carte_actuelle
        if not carte:
            return
        if self.reponse.get().lower() == carte.reponse.lower():
            carte.connue()
            messagebox.showinfo("Quiz", "Bonne réponse")
        else:
            carte.pas_connue()
            messagebox.showinfo("Quiz", f"Mauvaise réponse : {carte.reponse}")
        self.app.quiz.chapitre.sauvegarder_cartes()
        self.reponse.delete(0, END)
        self.app.carte_actuelle = self.app.quiz.tirer_cartes()
        self.question.config(text=self.app.carte_actuelle.question)

    def apply_theme(self, t):
        self.configure(bg=t["bg"])
        self.center.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        self.question.configure(bg=t["bg"], fg=t["fg"])
        for w in (self.liste, self.reponse, self.btn_lancer, self.btn_valider, self.btn_retour):
            w.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)


# =====================
# FLASHCARDS
# =====================
class FlashcardView(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # center everything in this frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.center = Frame(self)
        self.center.grid(row=0, column=0)

        self.title_label = Label(self.center, text="Flashcards", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=20)

        self.liste = Listbox(self.center, height=6)
        self.liste.pack(pady=10)

        self.question = Label(self.center, text="", wraplength=800, font=("Helvetica", 16))
        self.question.pack(pady=30)

        self.btn_show = Button(self.center, text="Suivant", command=self.afficher)
        self.btn_ok = Button(self.center, text="Je connais", command=self.connait)
        self.btn_nok = Button(self.center, text="Je ne connais pas", command=self.ne_connait_pas)
        self.btn_retour = Button(self.center, text="Retour", command=lambda: app.show_frame("MenuPrincipal"))

        for b in (self.btn_show, self.btn_ok, self.btn_nok, self.btn_retour):
            b.pack(pady=5)
        # flag to track whether the current card's question is shown and next click should show answer
        self._showing_answer = False

    def actualiser(self):
        self.liste.delete(0, END)
        for nom in self.app.chapitres:
            self.liste.insert(END, nom)
        # reset flashcard state when the flashcard view is refreshed
        self.app.flashcards = None
        self.app.carte_actuelle = None
        self._showing_answer = False
        try:
            self.btn_show.configure(text="Suivant")
        except Exception:
            pass
        self.question.config(text="")

    def afficher(self):
        # initialize flashcards for selected chapter if needed
        if not self.app.flashcards:
            nom = self.liste.get(ACTIVE)
            self.app.flashcards = FlashCards(self.app.chapitres[nom])
            self.app.carte_actuelle = None
            self._showing_answer = False

        # if there is no current card, draw one and show its question
        if not self.app.carte_actuelle:
            self.app.carte_actuelle = self.app.flashcards.tirer_carte()
            self.question.config(text=self.app.carte_actuelle.question)
            self._showing_answer = True
            # after drawing question, button should offer to show the answer
            self.btn_show.configure(text="Afficher réponse")
            return

        # if question currently shown, show the answer
        if self._showing_answer:
            # ensure the label update is visible before modal dialog
            self.update_idletasks()
            messagebox.showinfo("Réponse", self.app.carte_actuelle.reponse)
            self._showing_answer = False
            # after showing answer, button goes back to initial action
            self.btn_show.configure(text="Afficher réponse")
        else:
            # show a new question (draw next random card)
            self.app.carte_actuelle = self.app.flashcards.tirer_carte()
            self.question.config(text=self.app.carte_actuelle.question)
            self._showing_answer = True
            self.btn_show.configure(text="Afficher réponse")

    def connait(self):
        if self.app.carte_actuelle:
            self.app.carte_actuelle.connue()
            self.suivant()

    def ne_connait_pas(self):
        if self.app.carte_actuelle:
            self.app.carte_actuelle.pas_connue()
            self.suivant()

    def suivant(self):
        self.app.flashcards.chapitre.sauvegarder_cartes()
        self.app.carte_actuelle = self.app.flashcards.tirer_carte()
        self.question.config(text=self.app.carte_actuelle.question)

    def apply_theme(self, t):
        self.configure(bg=t["bg"])
        self.center.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        self.question.configure(bg=t["bg"], fg=t["fg"])
        for w in (self.liste, self.btn_show, self.btn_ok, self.btn_nok, self.btn_retour):
            w.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)


# =====================
# GESTION DES CHAPITRES
# =====================
class GestionChapitreView(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # center everything in this frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.center = Frame(self)
        self.center.grid(row=0, column=0)

        self.title_label = Label(self.center, text="Gestion des chapitres", font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=20)

        self.liste = Listbox(self.center, height=8)
        self.liste.pack(pady=10)

        self.nom = Entry(self.center)
        self.nom.pack(pady=5)

        self.btn_add = Button(self.center, text="Créer", command=self.creer)
        self.btn_del = Button(self.center, text="Supprimer", command=self.supprimer)
        self.btn_retour = Button(self.center, text="Retour", command=lambda: app.show_frame("MenuPrincipal"))

        for b in (self.btn_add, self.btn_del, self.btn_retour):
            b.pack(pady=5)

    def actualiser(self):
        self.liste.delete(0, END)
        for nom in self.app.chapitres:
            self.liste.insert(END, nom)

    def creer(self):
        nom = self.nom.get().strip()
        if not nom:
            return
        chap = Chapitres(nom)
        chap.sauvegarder_cartes()
        self.app.chapitres[nom] = chap
        self.nom.delete(0, END)
        self.actualiser()

    def supprimer(self):
        nom = self.liste.get(ACTIVE)
        if messagebox.askyesno("Confirmation", f"Supprimer {nom} ?"):
            path = self.app.chapitres[nom]._get_data_path()
            if os.path.exists(path):
                os.remove(path)
            del self.app.chapitres[nom]
            self.actualiser()

    def apply_theme(self, t):
        self.configure(bg=t["bg"])
        self.center.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        for w in (self.liste, self.nom, self.btn_add, self.btn_del, self.btn_retour):
            w.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
