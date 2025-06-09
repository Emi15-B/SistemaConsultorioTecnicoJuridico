import tkinter as tk
from clientes.gui import MenuPrincipal

def main():
    menu = MenuPrincipal()
    menu.state('zoomed')  # Abrir en pantalla completa (Windows)
    menu.mainloop()

if __name__ == '__main__':
    main()

