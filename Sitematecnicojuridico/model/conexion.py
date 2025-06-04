import sqlite3 

class ConexionDB:
    def __init__(self):
        self.baseDatos = 'Basededatos/dbSistema.db'
        self.conexion = None
        self.cursor = None
        self.abrirConexion()

    def abrirConexion(self):
        if self.conexion is None:
            self.conexion = sqlite3.connect(self.baseDatos, timeout=10)  # Le damos un timeout de 10 seg.
            self.cursor = self.conexion.cursor()

    def cerrarConexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.commit()
            self.conexion.close()
            self.conexion = None
            self.cursor = None
