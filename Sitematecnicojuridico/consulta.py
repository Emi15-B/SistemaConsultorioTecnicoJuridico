import tkinter as tk 
import traceback
from clientes.gui import Frame
#interfaz grafica
def main ():
    root = tk.Tk ()
    root.title ('Consulta Tecnico/Juridica')
    root.resizable(1,1)
    
    def show_error(exc_type, exc_value, exc_tb):
        traceback.print_exception(exc_type, exc_value, exc_tb)
    root.report_callback_exception = show_error


    app = Frame(root)
    root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Consulta Tecnico/Juridica')
    root.resizable(1,1)
    app = Frame(root)
    root.mainloop()

