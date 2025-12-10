from tkinter import *

#Interface graphique    chatgpt
class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.config_fenetre()
        self.creer_widgets()

#configuration de base de la fenetre
    def config_fenetre(self):
        self.title("Jean Révise")
        self.geometry("1080x720")
        self.minsize(480, 360)
        #self.iconbitmap("../img/logos/jeanReviseLogo.ico")
        self.config(background='#5AEBFC')

#ajout du texte, boutons, etc...
    def creer_widgets(self):
        self.label = Label(self, text="Application de révision", font=("Helvetica", 40), bg='#5AEBFC', fg='#1749B3')
        self.label.pack()

#ajout d'évenements de clavier et souris
    def creer_bindings(self):
        pass
appli = Interface()
appli.mainloop()