from tkinter import *

#Interface graphique    chatgpt
class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.config_fenetre()
    def config_fenetre(self):
        self.title("Appli de révision")
        self.geometry("1080x720")
        self.minsize(480, 360)
        self.config(background='#5AEBFC')

appli = Interface()
appli.mainloop()