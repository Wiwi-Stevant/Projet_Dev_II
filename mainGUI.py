from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import os
from PIL import Image, ImageTk
from tkinter import filedialog



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
        self.iconbitmap("img\logos\jeanReviseSansLogo.ico")

        # données
        self.chapitres = {}
        self.quiz = None
        self.flashcards = None
        self.carte_actuelle = None
        self.selected_chapter = None

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
        # clearing selection when returning to main menu
        if name == "MenuPrincipal":
            self.selected_chapter = None
        frame.actualiser()
        frame.tkraise()

    def open_and_select(self, frame_name):
        # prompt the user to choose a chapter before opening the frame
        if not self.chapitres:
            messagebox.showinfo("Aucun chapitre", "Aucun chapitre disponible.")
            # still show the frame so user can create chapters in Gestion
            self.selected_chapter = None
            return self.show_frame(frame_name)

        sel = self._choose_chapter()
        if not sel:
            return

        # prevent launching Quiz or Flashcards if the chapter has no cards
        chap = self.chapitres.get(sel)
        if frame_name in ("QuizView", "FlashcardView"):
            if not chap or not chap.cartes:
                messagebox.showwarning("Chapitre vide", "Le chapitre sélectionné ne contient aucune carte.\nVeuillez ajouter des cartes avant de lancer le Quiz ou les Flashcards.")
                return

        self.selected_chapter = sel
        self.show_frame(frame_name)

    def _choose_chapter(self):
        # modal dialog to choose a chapter from the existing list
        dlg = Toplevel(self)
        dlg.title("Choisir un chapitre")
        dlg.transient(self)
        dlg.grab_set()

        Label(dlg, text="Sélectionnez un chapitre:").pack(padx=10, pady=8)
        lb = Listbox(dlg, height=8)
        lb.pack(padx=10, pady=4)
        for nom in self.chapitres:
            lb.insert(END, nom)

        selected = {"name": None}

        def on_ok():
            try:
                selected["name"] = lb.get(ACTIVE)
            except Exception:
                selected["name"] = None
            dlg.destroy()

        def on_cancel():
            dlg.destroy()

        # allow creating a new chapter from the chooser
        def on_create():
            create_dlg = Toplevel(dlg)
            create_dlg.title("Créer un chapitre")
            create_dlg.transient(dlg)
            create_dlg.grab_set()

            Label(create_dlg, text="Nom du chapitre:").pack(padx=10, pady=8)
            entry_name = Entry(create_dlg)
            entry_name.pack(padx=10, pady=4)

            def create_ok():
                name = entry_name.get().strip()
                if not name:
                    messagebox.showwarning("Nom manquant", "Veuillez entrer un nom de chapitre.", parent=create_dlg)
                    return
                # create and persist the chapter
                chap = Chapitres(name)
                chap.sauvegarder_cartes()
                self.chapitres[name] = chap
                selected["name"] = name
                create_dlg.destroy()
                dlg.destroy()

            def create_cancel():
                create_dlg.destroy()

            btns = Frame(create_dlg)
            btns.pack(pady=8)
            Button(btns, text="Créer", width=10, command=create_ok).pack(side="left", padx=5)
            Button(btns, text="Annuler", width=10, command=create_cancel).pack(side="left", padx=5)

        btn_frame = Frame(dlg)
        btn_frame.pack(pady=8)
        Button(btn_frame, text="Créer un chapitre", width=14, command=on_create).pack(side="left", padx=5)
        Button(btn_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=5)
        Button(btn_frame, text="Annuler", width=10, command=on_cancel).pack(side="left", padx=5)

        self.wait_window(dlg)
        return selected["name"]

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
        self.btn_quiz = Button(self.inner, text="Quiz", font=btn_font, command=lambda: app.open_and_select("QuizView"))
        self.btn_flash = Button(self.inner, text="Flashcards", font=btn_font, command=lambda: app.open_and_select("FlashcardView"))
        self.btn_gestion = Button(self.inner, text="Gérer chapitres", font=btn_font, command=lambda: app.open_and_select("GestionChapitreView"))
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
        # show/hide chapter list depending on whether a chapter was preselected
        if self.app.selected_chapter:
            try:
                self.liste.pack_forget()
            except Exception:
                pass
        else:
            # ensure listbox is visible and populated
            try:
                self.liste.pack()
            except Exception:
                pass
            self.liste.delete(0, END)
            for nom in self.app.chapitres:
                self.liste.insert(END, nom)
        

    def lancer(self):
        if self.app.selected_chapter:
            nom = self.app.selected_chapter
        else:
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

        # === AJOUT ===
        self.image_label = Label(self.center)
        self.image_label.pack(pady=10)

        self.photo = None  # IMPORTANT pour garder la référence de l'image


        self.btn_show = Button(self.center, text="Suivant", command=self.afficher)
        self.btn_ok = Button(self.center, text="Je connais", command=self.connait)
        self.btn_nok = Button(self.center, text="Je ne connais pas", command=self.ne_connait_pas)
        self.btn_retour = Button(self.center, text="Retour", command=lambda: app.show_frame("MenuPrincipal"))

        for b in (self.btn_show, self.btn_ok, self.btn_nok, self.btn_retour):
            b.pack(pady=5)
        # flag to track whether the current card's question is shown and next click should show answer
        self._showing_answer = False

    def actualiser(self):
        # show/hide chapter list depending on whether a chapter was preselected
        if self.app.selected_chapter:
            try:
                self.liste.pack_forget()
            except Exception:
                pass
        else:
            try:
                self.liste.pack()
            except Exception:
                pass
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
        # cacher les boutons tant qu'aucune question n'est affichée
        self.btn_ok.pack_forget()
        self.btn_nok.pack_forget()

        # reset du bouton principal
        self.btn_show.pack(pady=5)
        self.btn_show.configure(text="Suivant")


    def afficher(self):
        self.btn_show.pack(pady=5)
        # initialisation des flashcards
        if not self.app.flashcards:
            if self.app.selected_chapter:
                nom = self.app.selected_chapter
            else:
                nom = self.liste.get(ACTIVE)

            self.app.flashcards = FlashCards(self.app.chapitres[nom])
            self.app.carte_actuelle = None

        # aucune carte → tirer une carte
        if not self.app.carte_actuelle:
            self.app.carte_actuelle = self.app.flashcards.tirer_carte()
            self.question.config(text=self.app.carte_actuelle.question)
            self.afficher_image(self.app.carte_actuelle)  # === AJOUT ===

            self.btn_ok.pack(pady=5)
            self.btn_nok.pack(pady=5)

            self._showing_answer = False
            self.btn_show.configure(text="Afficher réponse")
            return

        # afficher la réponse
        if not self._showing_answer:
            self.question.config(text=self.app.carte_actuelle.reponse)
            self.afficher_image(self.app.carte_actuelle)  # === AJOUT ===

            self._showing_answer = True
            self.btn_show.configure(text="Revoir la question")
            self.image_label.config(image="")


        # revenir à la question
        else:
            self.question.config(text=self.app.carte_actuelle.question)
            self.afficher_image(self.app.carte_actuelle)  # === AJOUT ===

            self._showing_answer = False
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
        if self.app.carte_actuelle:
            self.question.config(text=self.app.carte_actuelle.question)
            self.afficher_image(self.app.carte_actuelle)

        else:
            self.question.config(text="")
        self.btn_ok.pack(pady=5)
        self.btn_nok.pack(pady=5)

    def apply_theme(self, t):
        self.configure(bg=t["bg"])
        self.center.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        self.question.configure(bg=t["bg"], fg=t["fg"])
        for w in (self.liste, self.btn_show, self.btn_ok, self.btn_nok, self.btn_retour):
            w.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)
    # ===== AJOUT AFFICHAGE IMAGE =====
    def afficher_image(self, carte):
        if not carte or not carte.img:
            self.image_label.config(image="")
            self.photo = None
            return

        if not os.path.exists(carte.img):
            self.image_label.config(image="", text="Image introuvable")
            self.photo = None
            return

        img = Image.open(carte.img)
        img.thumbnail((350, 250))
        self.photo = ImageTk.PhotoImage(img)

        self.image_label.config(image=self.photo)


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

        # list of chapters (used when no chapter preselected)
        self.liste = Listbox(self.center, height=8)
        self.liste.pack(pady=10)

        # (removed single-line chapter entry — selection/creation handled via modals)

        # management UI for a selected chapter
        self.chapter_label = Label(self.center, text="", font=("Helvetica", 20, "bold"))

        self.btn_add_card = Button(self.center, text="Ajouter une carte", command=self.add_card)
        self.btn_modify_card = Button(self.center, text="Modifier une carte", command=self.modify_card)
        self.btn_delete_card = Button(self.center, text="Supprimer une carte", command=self.delete_card)
        self.btn_view_cards = Button(self.center, text="Voir les cartes", command=self.view_cards)
        self.btn_return_main = Button(self.center, text="Retour au menu principal", command=lambda: app.show_frame("MenuPrincipal"))

        for b in (self.btn_add_card, self.btn_modify_card, self.btn_delete_card, self.btn_view_cards, self.btn_return_main):
            # don't pack yet; will be packed when a chapter is selected
            pass

    def actualiser(self):
        # show/hide chapter list depending on whether a chapter was preselected
        if self.app.selected_chapter:
            try:
                self.liste.pack_forget()
            except Exception:
                pass
            # show chapter management header + buttons
            self.chapter_label.config(text=f"Chapitre : {self.app.selected_chapter}")
            try:
                self.chapter_label.pack(pady=8)
            except Exception:
                pass
            # pack action buttons
            self.btn_add_card.pack(pady=5)
            self.btn_modify_card.pack(pady=5)
            self.btn_delete_card.pack(pady=5)
            self.btn_view_cards.pack(pady=5)
            self.btn_return_main.pack(pady=10)
        else:
            # ensure management UI is hidden
            try:
                self.chapter_label.pack_forget()
            except Exception:
                pass
            for b in (self.btn_add_card, self.btn_modify_card, self.btn_delete_card, self.btn_view_cards, self.btn_return_main):
                try:
                    b.pack_forget()
                except Exception:
                    pass

            try:
                self.liste.pack()
            except Exception:
                pass
            self.liste.delete(0, END)
            for nom in self.app.chapitres:
                self.liste.insert(END, nom)

    def creer(self):
        # prompt user for chapter name (used if UI calls creer directly)
        name = simpledialog.askstring("Créer un chapitre", "Nom du chapitre:", parent=self)
        if not name:
            return
        nom = name.strip()
        if not nom:
            return
        chap = Chapitres(nom)
        chap.sauvegarder_cartes()
        self.app.chapitres[nom] = chap
        # if we created the chapter that was selected, keep it
        if self.app.selected_chapter == nom:
            self.app.selected_chapter = nom
        self.actualiser()

    def supprimer(self):
        if self.app.selected_chapter:
            nom = self.app.selected_chapter
        else:
            try:
                nom = self.liste.get(ACTIVE)
            except Exception:
                return
        if messagebox.askyesno("Confirmation", f"Supprimer {nom} ?"):
            path = self.app.chapitres[nom]._get_data_path()
            if os.path.exists(path):
                os.remove(path)
            del self.app.chapitres[nom]
            # if we deleted the selected chapter, clear selection
            if self.app.selected_chapter == nom:
                self.app.selected_chapter = None
            self.actualiser()

    # ---------------------
    # Chapter management actions
    # ---------------------
    def _get_current_chap(self):
        name = self.app.selected_chapter or (self.liste.get(ACTIVE) if self.liste.size() > 0 else None)
        if not name:
            messagebox.showwarning("Aucun chapitre", "Aucun chapitre sélectionné.")
            return None
        return self.app.chapitres.get(name)

    def add_card(self):
        chap = self._get_current_chap()
        if not chap:
            return
        dlg = Toplevel(self)
        dlg.title("Ajouter une carte")
        dlg.transient(self)
        dlg.grab_set()

        Label(dlg, text="Question:").pack(padx=10, pady=(10,0))
        e_q = Entry(dlg, width=60)
        e_q.pack(padx=10, pady=4)
        Label(dlg, text="Réponse:").pack(padx=10, pady=(8,0))
        e_r = Entry(dlg, width=60)
        e_r.pack(padx=10, pady=4)
                        # === AJOUT IMAGE ===
        img_path = {"path": ""}

        def choisir_image():
            src = filedialog.askopenfilename(
                title="Choisir une image",
                filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")]
            )
            if not src:
                return

            images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
            os.makedirs(images_dir, exist_ok=True)

            filename = os.path.basename(src)
            dest = os.path.join(images_dir, filename)


            img_path["path"] = dest
            lbl_img.config(text=filename)

        Button(dlg, text="Choisir une image", command=choisir_image).pack(pady=5)
        lbl_img = Label(dlg, text="Aucune image sélectionnée")
        lbl_img.pack()

        def on_valider():
            q = e_q.get().strip()
            r = e_r.get().strip()
            if not q or not r:
                messagebox.showwarning("Données manquantes", "Question et réponse requises.", parent=dlg)
                return
            chap.cree_cartes(q, r, img_path["path"])  # === MODIFIÉ ===

            # if messagebox.askyesno("Confirmation", f"Créer la carte ?\nQuestion: {q}\nRéponse: {r}"):
            #     chap.cree_cartes(q, r)
            messagebox.showinfo("Créé", "La carte a été créée avec l'image.", parent=dlg)
            dlg.destroy()

        Button(dlg, text="Valider", command=on_valider).pack(pady=10)

    def modify_card(self):
        chap = self._get_current_chap()
        if not chap:
            return

        sel = Toplevel(self)
        sel.title("Sélectionner une carte à modifier")
        sel.transient(self)
        sel.grab_set()

        lb = Listbox(sel, height=10, width=80)
        lb.pack(padx=10, pady=8)
        ids = []
        for c in chap.cartes.values():
            lb.insert(END, f"{c.id} - Q: {c.question} | R: {c.reponse}")
            ids.append(c.id)

        def on_select():
            idx = lb.curselection()
            if not idx:
                return
            chosen_id = ids[idx[0]]
            c = chap.cartes[chosen_id]
            sel.destroy()

            edit = Toplevel(self)
            edit.title("Modifier la carte")
            edit.transient(self)
            edit.grab_set()

            Label(edit, text="Ancienne question:").pack(padx=10, pady=(8,0))
            Label(edit, text=c.question, wraplength=500).pack(padx=10, pady=4)
            Label(edit, text="Nouvelle question:").pack(padx=10, pady=(8,0))
            nq = Entry(edit, width=60)
            nq.insert(0, c.question)
            nq.pack(padx=10, pady=4)

            Label(edit, text="Ancienne réponse:").pack(padx=10, pady=(8,0))
            Label(edit, text=c.reponse, wraplength=500).pack(padx=10, pady=4)
            Label(edit, text="Nouvelle réponse:").pack(padx=10, pady=(8,0))
            nr = Entry(edit, width=60)
            nr.insert(0, c.reponse)
            nr.pack(padx=10, pady=4)

            def on_modify():
                new_q = nq.get().strip()
                new_r = nr.get().strip()
                if not new_q or not new_r:
                    messagebox.showwarning("Données manquantes", "Question et réponse requises.", parent=edit)
                    return
                if messagebox.askyesno("Confirmation", f"Modifier la carte ?\nQuestion: {new_q}\nRéponse: {new_r}"):
                    chap.modifier_carte(chosen_id, new_q, new_r, c.img)
                    messagebox.showinfo("Modifié", "La carte a été modifiée.", parent=edit)
                    edit.destroy()

            Button(edit, text="Valider", command=on_modify).pack(pady=10)

        Button(sel, text="Modifier la carte sélectionnée", command=on_select).pack(pady=6)

    def delete_card(self):
        chap = self._get_current_chap()
        if not chap:
            return

        dlg = Toplevel(self)
        dlg.title("Supprimer une carte")
        dlg.transient(self)
        dlg.grab_set()

        lb = Listbox(dlg, height=10, width=80)
        lb.pack(padx=10, pady=8)
        ids = []
        for c in chap.cartes.values():
            lb.insert(END, f"{c.id} - Q: {c.question} | R: {c.reponse}")
            ids.append(c.id)

        def on_del():
            sel = lb.curselection()
            if not sel:
                return
            cid = ids[sel[0]]
            c = chap.cartes[cid]
            if messagebox.askyesno("Confirmation", f"Supprimer la carte ?\nQuestion: {c.question}\nRéponse: {c.reponse}"):
                chap.supprimer_carte(cid)
                messagebox.showinfo("Supprimé", "La carte a été supprimée.", parent=dlg)
                dlg.destroy()

        Button(dlg, text="Supprimer la carte sélectionnée", command=on_del).pack(pady=6)

    def view_cards(self):
        chap = self._get_current_chap()
        if not chap:
            return
        dlg = Toplevel(self)
        dlg.title(f"Cartes du chapitre {chap.nom}")
        dlg.transient(self)
        dlg.grab_set()

        text = Text(dlg, width=100, height=25)
        text.pack(padx=10, pady=8)
        for c in chap.cartes.values():
            text.insert(END, f"ID: {c.id}\nQuestion: {c.question}\nRéponse: {c.reponse}\nImage: {c.img}\nNiveau: {c.niveau}\n---\n")
        Button(dlg, text="Retour", command=dlg.destroy).pack(pady=6)

    def apply_theme(self, t):
        self.configure(bg=t["bg"])
        self.center.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        # configure list/label (chapter header may not exist yet)
        for w in (self.liste, getattr(self, 'chapter_label', None)):
            if w is None:
                continue
            try:
                w.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)
            except Exception:
                pass
        # configure action buttons (if present)
        for b in (getattr(self, 'btn_add_card', None), getattr(self, 'btn_modify_card', None), getattr(self, 'btn_delete_card', None), getattr(self, 'btn_view_cards', None), getattr(self, 'btn_return_main', None)):
            if b is None:
                continue
            try:
                b.configure(bg=t["button_bg"], fg=t["button_fg"], bd=0)
            except Exception:
                pass


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
