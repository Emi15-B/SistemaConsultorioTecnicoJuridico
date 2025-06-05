from .conexion import ConexionDB
from tkinter import messagebox

def editarDatoCliente(persona, idPersona):
    conexion = ConexionDB()
    sql = f"""UPDATE Cliente SET nombre = '{persona.nombre}', apellido ='{persona.apellido}',documId = {persona.documId}, email='{persona.email}', 
    telefono ='{persona.telefono}',nacionalidad = '{persona.nacionalidad}', residencia = '{persona.residencia}', asunto = '{persona.asunto}', 
    estatus = '{persona.estatus}', activo = 1 WHERE idPersona = {idPersona}"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        title = 'Editar Cliente'
        mensaje = 'Cliente editado exitosamente'
        messagebox.showinfo(title, mensaje)

    except Exception as e: # <-- CAMBIA ESTO: atrapa la excepción y la imprime
        print(f"ERROR al editar cliente (SQL: {sql}): {e}") # <-- MUY IMPORTANTE: Imprime el SQL y el error real
        title = 'Editar Cliente'
        mensaje = f' Error al editar cliente: {str(e)}' # Muestra el error en el messagebox
        messagebox.showerror(title, mensaje) # CAMBIA a showerror para que sea más evidente
        # NO llames conexion.cerrarConexion() en el except de edición
        # Si hubo un error, no hay nada que commitear y la conexión podría no haberse abierto bien
        # O incluso estar en un estado inconsistente. Mejor no cerrar si hubo un error de SQL.
        # Puedes considerar un 'finally' si la conexión siempre debe cerrarse.

def guardarDatoCliente(persona):
   conexion =  ConexionDB()
   # Solo los campos que existen en la tabla Cliente
   sql =  f"""INSERT INTO Cliente (nombre, apellido, documId, email, telefono,
          nacionalidad, residencia, asunto, estatus, activo) VALUES
            ('{persona.nombre}','{persona.apellido}',{persona.documId},
            '{persona.email}','{persona.telefono}','{persona.nacionalidad}','{persona.residencia}',
            '{persona.asunto}','{persona.estatus}',1)"""

   try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion()
        title = 'Registrar Cliente'
        mensaje = 'Cliente registrado exitosamente'
        messagebox.showinfo(title, mensaje)
   except Exception as e:
        print("ERROR al ejecutar SQL:", e)
        title = 'Registrar Clientee'
        mensaje = f'Error al registrar cliente: {str(e)}'
        messagebox.showerror(title, mensaje)


def listar ():
    conexion = ConexionDB()

    listaPersona = []   
    sql = 'SELECT idPersona, nombre, apellido, documId, email, telefono, nacionalidad, residencia, asunto, estatus FROM Cliente WHERE activo = 1'
    
    try:
        conexion.cursor.execute(sql)
        listaPersona = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except:
        title = 'Datos'
        mensaje = 'Registros no existen'
        messagebox.showwarning(title, mensaje)
    return listaPersona
 
def listarCondicion(where):
    conexion = ConexionDB()
    listaPersona = []
    sql = f'SELECT idPersona, nombre, apellido, documId, email, telefono, nacionalidad, residencia, asunto, estatus FROM Cliente {where}'
 
    try:
        conexion.cursor.execute(sql,)
        listaPersona = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except:    
        title = 'Datos'
        mensaje = 'Registros no existen'
        messagebox.showwarning(title, mensaje)
    return listaPersona

def eliminarCliente(id):
    conexion = ConexionDB ()
    sql = f"""UPDATE Cliente SET activo = 0 WHERE idPersona = {id}"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrarConexion ()
        title = 'Eliminar Cliente'
        mensaje = 'Cliente eliminado exitosamente'
        messagebox.showwarning(title, mensaje)
    except Exception as e:
        title = 'Eliminar Cliente'
        mensaje = 'Error al eliminar Cliente'
        messagebox.showwarning(title, mensaje)
      
class Persona:
    def __init__(self, nombre,apellido,documId,email,telefono,
                 nacionalidad,residencia,asunto,estatus):
        self.idPersona = None
        self.nombre = nombre
        self.apellido = apellido
        self.documId = documId
        self.email = email
        self.telefono = telefono
        self.nacionalidad = nacionalidad
        self.residencia = residencia
        self.asunto = asunto
        self.estatus = estatus

    def __str__(self):
        return f'Persona[{self.nombre}, {self.apellido},{self.documId}, {self.email}, {self.telefono}, {self.nacionalidad}, {self.residencia}, {self.asunto},{self.estatus}]'    

    __all__ = ['Persona', 'guardarDatoCliente']







