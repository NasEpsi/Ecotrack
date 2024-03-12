import tkinter as tk

class EcotrackAppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Ecotrack App")
        
        # Ajoutez les éléments de l'interface Tkinter ici

if __name__ == "__main__":
    root = tk.Tk()
    app = EcotrackAppTkinter(root)
    root.mainloop()