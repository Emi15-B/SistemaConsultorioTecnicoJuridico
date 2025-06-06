from .conexion import ConexionDB
from tkinter import messagebox
import sqlite3

def ensure_fecha_column():
    conexion = ConexionDB()
    try:
        conexion.cursor.execute("PRAGMA table_info(historiaConsulta)")
        columns = [col[1] for col in conexion.cursor.fetchall()]
        if 'fecha' not in columns:
            conexion.cursor.execute("ALTER TABLE historiaConsulta ADD COLUMN fecha TEXT")
            conexion.conexion.commit()
    except Exception as e:
        print(f"[MIGRATION] Error ensuring 'fecha' column: {e}")
    finally:
        conexion.cerrarConexion()

# Ensure the column exists on import
ensure_fecha_column()

def listarHistoria(idPersona):
    idpersona = int(idPersona)
    conexion = ConexionDB()
    listaHistoria = []
    sql = '''
    SELECT h.idHistoriaConsulta,
           c.nombre || " " || c.apellido AS NombreCompleto,
           h.atendidoPor,
           h.observaciones,
           h.fecha
    FROM historiaConsulta h
    INNER JOIN Cliente c ON c.idPersona = h.idPersona
    WHERE c.idPersona = ?
    '''
    try:
        conexion.cursor.execute(sql, (idPersona,))  # 👈 parámetro seguro
        listaHistoria = conexion.cursor.fetchall()
        print(f"[DEBUG] Resultados consulta historia: {listaHistoria}")
        conexion.cerrarConexion()

    except Exception as e:
        print(f'Error en listarHistoria: {str(e)}')
        title = 'LISTAR HISTORIA'
        mensaje =f'Error al listar historia consulta:\n{str(e)}'
        messagebox.showerror(title, mensaje)

    return listaHistoria


def guardarHistoria(idPersona, atendidoPor, observaciones, fecha):
    conexion = ConexionDB()
    sql = f"""INSERT INTO historiaConsulta (idPersona, atendidoPor, observaciones, fecha) VALUES
            (?, ?, ?, ?)"""
    try:
        conexion.cursor.execute(sql, (idPersona, atendidoPor, observaciones, fecha))
        conexion.cerrarConexion()
        title = 'Registro Historia Consulta'
        mensaje = 'Historia registrada exitosamente'
        messagebox.showinfo(title, mensaje)

    except Exception as e:
        title = 'Registro Historia Consulta'
        mensaje = f'Error al registrar historia:\n{str(e)}'
        messagebox.showerror(title, mensaje)


def eliminarHistoria(idHistoriaConsulta):
    conexion = ConexionDB()
    sql = f'DELETE FROM historiaConsulta WHERE idHistoriaConsulta = {idHistoriaConsulta}'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        title = 'Eliminar Historia '
        mensaje = 'Historia eliminada exitosamente'
        messagebox.showinfo(title, mensaje)
    except Exception as e:
        title = 'Eliminar Historia'
        mensaje = f'Error al eliminar historia:\n{str(e)}'
        messagebox.showerror(title, mensaje)

def editarHistoria(atendidoPor, observaciones, fecha, idHistoriaConsulta):
    conexion = ConexionDB()
    sql = f"""UPDATE historiaConsulta SET atendidoPor = ?, observaciones = ?, fecha = ? 
              WHERE idHistoriaConsulta = ?"""
    try:
        conexion.cursor.execute(sql, (atendidoPor, observaciones, fecha, idHistoriaConsulta))
        conexion.cerrarConexion()
        title = 'Editar Historia'
        mensaje = 'Historia editada exitosamente'
        messagebox.showinfo(title, mensaje)

    except Exception as e:
        title = 'Editar Historia'
        mensaje = f'Error al editar historia:\n{str(e)}'
        messagebox.showerror(title, mensaje)   
        
        
        
class historiaConsulta:
    def __init__(self, idPersona, motivo, detalle, fecha=None):
        self.idHistoriaConsulta = None
        self.idPersona= idPersona
        self.motivo = motivo
        self.detalle = detalle
        self.fecha = fecha

    def __str__(self):
        return f'historiaConsulta[{self.idPersona},{self.motivo}, {self.detalle}, {self.fecha}]'