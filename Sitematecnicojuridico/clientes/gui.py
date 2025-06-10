import tkinter as tk
from tkinter import *
from tkinter import Button, ttk, scrolledtext, Toplevel, messagebox, LabelFrame
from model.conexion import ConexionDB
from model.clienteDao import Persona, guardarDatoCliente, listarCondicion, listar, editarDatoCliente, eliminarCliente
from model.historiaConsultaDao import historiaConsulta, guardarHistoria, listarHistoria, eliminarHistoria   
try:
    from tkcalendar import DateEntry
except ImportError:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkcalendar'])
    from tkcalendar import DateEntry
import datetime

# === PALETA Y FUENTES CORPORATIVAS ===
COLOR_PRIMARIO = '#2A5F8A'  # Azul corporativo
COLOR_SECUNDARIO = '#F5F5F5'  # Gris claro
COLOR_TARJETA = 'white'
COLOR_VERDE = '#4CAF50'  # Guardar
COLOR_ROJO = '#F44336'   # Eliminar
FUENTE_TITULO = ('Segoe UI', 18, 'bold')
FUENTE_TITULO_GRANDE = ('Segoe UI', 28, 'bold')
FUENTE_LABEL = ('Segoe UI', 15, 'bold')
FUENTE_CONTENIDO = ('Segoe UI', 14)
FUENTE_BOTON = ('Segoe UI', 12, 'bold')

class Frame (tk.Frame):
    def __init__(self, root):

        super().__init__(root,width=1280,height=720)
        self.root = root            #modificacion de codigo 
        self.config(bg=COLOR_SECUNDARIO) 
        self.pack()
        self.camposCliente()
        self.deshabilitar()
        self.tablaCliente()
        self.agregar_logo_empresa()  # Mostrar el logo al iniciar
        

    def camposCliente(self):
        self.lblId = tk.Label(self, text='Id: ')
        self.lblId.config (font=('ARIAL',15, 'bold'),bg=COLOR_SECUNDARIO ) 
        self.lblId.grid(column=0,row=0, padx=10, pady=5)

        self.lblNombre = tk.Label(self, text='Nombre: ')
        self.lblNombre.config (font=('ARIAL',15, 'bold'),bg=COLOR_SECUNDARIO ) 
        self.lblNombre.grid(column=0,row=1, padx=10, pady=5)

        self.lblApellido = tk.Label(self, text='Apellido: ')
        self.lblApellido.config (font=('ARIAL',15, 'bold'),bg=COLOR_SECUNDARIO ) 
        self.lblApellido.grid(column=0, row=2, padx=10, pady=5)

        self.lblDocumId= tk.Label(self, text='DocumId: ')
        self.lblDocumId.config (font=('ARIAL',15, 'bold'),bg=COLOR_SECUNDARIO ) 
        self.lblDocumId.grid(column=0, row=3, padx=10, pady=5)

        self.lblEmail = tk.Label(self, text='Email: ')
        self.lblEmail.config (font=('ARIAL',15, 'bold'),bg=COLOR_SECUNDARIO ) 
        self.lblEmail.grid(column=0, row=4, padx=10, pady=5)

        self.lblTelefono = tk.Label(self, text='Telefono: ')
        self.lblTelefono.config(font=FUENTE_LABEL, bg=COLOR_SECUNDARIO)
        self.lblTelefono.grid(column=0, row=5, padx=10, pady=5)

        self.lblNacionalidad = tk.Label(self, text='Nacionalidad: ')
        self.lblNacionalidad.config(font=FUENTE_LABEL, bg=COLOR_SECUNDARIO)
        self.lblNacionalidad.grid(column=0, row=6, padx=10, pady=5)

        self.lblResidencia = tk.Label(self, text='Residencia: ')
        self.lblResidencia.config(font=FUENTE_LABEL, bg=COLOR_SECUNDARIO)
        self.lblResidencia.grid(column=0, row=7, padx=10, pady=5)

        self.svResidencia = tk.StringVar()
        self.entryResidencia = tk.Entry(self, textvariable=self.svResidencia)
        self.entryResidencia.config(width=50, font=FUENTE_CONTENIDO)
        self.entryResidencia.grid(column=1, row=7, padx=10, pady=5, columnspan=2)

        self.lblAsunto = tk.Label(self, text='Asunto: ')
        self.lblAsunto.config(font=FUENTE_LABEL, bg=COLOR_SECUNDARIO)
        self.lblAsunto.grid(column=0, row=8, padx=10, pady=5)

        self.lblEstatus = tk.Label(self, text='Estatus: ')
        self.lblEstatus.config(font=FUENTE_LABEL, bg=COLOR_SECUNDARIO)
        self.lblEstatus.grid(column=0, row=9, padx=10, pady=5)

        #Entradas
        self.svId = tk.StringVar()
        self.entryId = tk.Entry(self, textvariable=self.svId)
        self.entryId.config(width=50, font=FUENTE_CONTENIDO)
        self.entryId.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=50, font=FUENTE_CONTENIDO)
        self.entryNombre.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svApellido = tk.StringVar()
        self.entryApellido = tk.Entry(self, textvariable=self.svApellido)
        self.entryApellido.config(width=50, font=FUENTE_CONTENIDO)
        self.entryApellido.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svDocumId = tk.StringVar()
        self.entryDocumId = tk.Entry(self, textvariable=self.svDocumId)
        self.entryDocumId.config(width=50, font=FUENTE_CONTENIDO)
        self.entryDocumId.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svEmail = tk.StringVar()
        self.entryEmail = tk.Entry(self, textvariable=self.svEmail)
        self.entryEmail.config(width=50, font=FUENTE_CONTENIDO)
        self.entryEmail.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svTelefono = tk.StringVar()
        self.entryTelefono = tk.Entry(self, textvariable=self.svTelefono)
        self.entryTelefono.config(width=50, font=FUENTE_CONTENIDO)
        self.entryTelefono.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        # --- Combobox Nacionalidad ---
        self.svNacionalidad = tk.StringVar()
        self.lista_paises = [
            'Afganistán', 'Albania', 'Alemania', 'Andorra', 'Angola', 'Antigua y Barbuda', 'Arabia Saudita',
            'Argelia', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaiyán', 'Bahamas', 'Bangladés',
            'Barbados', 'Baréin', 'Bélgica', 'Belice', 'Benín', 'Bielorrusia', 'Birmania', 'Bolivia', 'Bosnia y Herzegovina',
            'Botsuana', 'Brasil', 'Brunéi', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Bután', 'Cabo Verde', 'Camboya',
            'Camerún', 'Canadá', 'Catar', 'Chad', 'Chile', 'China', 'Chipre', 'Ciudad del Vaticano', 'Colombia',
            'Comoras', 'Corea del Norte', 'Corea del Sur', 'Costa de Marfil', 'Costa Rica', 'Croacia', 'Cuba',
            'Dinamarca', 'Dominica', 'Ecuador', 'Egipto', 'El Salvador', 'Emiratos Árabes Unidos', 'Eritrea',
            'Eslovaquia', 'Eslovenia', 'España', 'Estados Unidos', 'Estonia', 'Etiopía', 'Filipinas', 'Finlandia',
            'Fiyi', 'Francia', 'Gabón', 'Gambia', 'Georgia', 'Ghana', 'Granada', 'Grecia', 'Guatemala', 'Guyana',
            'Guinea', 'Guinea ecuatorial', 'Guinea-Bisáu', 'Haití', 'Honduras', 'Hungría', 'India', 'Indonesia',
            'Irak', 'Irán', 'Irlanda', 'Islandia', 'Islas Marshall', 'Islas Salomón', 'Israel', 'Italia', 'Jamaica',
            'Japón', 'Jordania', 'Kazajistán', 'Kenia', 'Kirguistán', 'Kiribati', 'Kuwait', 'Laos', 'Lesoto',
            'Letonia', 'Líbano', 'Liberia', 'Libia', 'Liechtenstein', 'Lituania', 'Luxemburgo', 'Macedonia del Norte',
            'Madagascar', 'Malasia', 'Malaui', 'Maldivas', 'Malí', 'Malta', 'Marruecos', 'Mauricio', 'Mauritania',
            'México', 'Micronesia', 'Moldavia', 'Mónaco', 'Mongolia', 'Montenegro', 'Mozambique', 'Namibia',
            'Nauru', 'Nepal', 'Nicaragua', 'Níger', 'Nigeria', 'Noruega', 'Nueva Zelanda', 'Omán', 'Países Bajos',
            'Pakistán', 'Palaos', 'Palestina', 'Panamá', 'Papúa Nueva Guinea', 'Paraguay', 'Perú', 'Polonia',
            'Portugal', 'Reino Unido', 'República Centroafricana', 'República Checa', 'República del Congo',
            'República Democrática del Congo', 'República Dominicana', 'Ruanda', 'Rumanía', 'Rusia', 'Samoa',
            'San Cristóbal y Nieves', 'San Marino', 'San Vicente y las Granadinas', 'Santa Lucía', 'Santo Tomé y Príncipe',
            'Senegal', 'Serbia', 'Seychelles', 'Sierra Leona', 'Singapur', 'Siria', 'Somalia', 'Sri Lanka', 'Suazilandia',
            'Sudáfrica', 'Sudán', 'Sudán del Sur', 'Suecia', 'Suiza', 'Surinam', 'Tailandia', 'Tanzania', 'Tayikistán',
            'Timor Oriental', 'Togo', 'Tonga', 'Trinidad y Tobago', 'Túnez', 'Turkmenistán', 'Turquía', 'Tuvalu',
            'Ucrania', 'Uganda', 'Uruguay', 'Uzbekistán', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Yibuti', 'Zambia', 'Zimbabue'
        ]
        self.comboNacionalidad = ttk.Combobox(self, textvariable=self.svNacionalidad, values=self.lista_paises, width=47, font=('ARIAL', 15))
        self.comboNacionalidad.grid(column=1, row=6, padx=10, pady=5, columnspan=2)
        self.comboNacionalidad.bind('<KeyRelease>', self._filtrar_nacionalidad)

        self.svEstatus = tk.StringVar()
        self.comboEstatus = ttk.Combobox(self, textvariable=self.svEstatus, values=["Activo", "En proceso", "Terminado"], width=47, font=('ARIAL', 15), state="readonly")
        self.comboEstatus.grid(column=1, row=9, padx=10, pady=5, columnspan=2)

        self.svAsunto = tk.StringVar()
        self.lista_asuntos = [
            'Asesoría en Protección de Datos para empresas',
            'Buenas Prácticas Digitales en el Puesto de Trabajo',
            'Seguridad de la Información-Ciberseguridad',
            'Auditorías de Sistemas de Información',
            'Compliance',
            'Adecuación al marco normativo y práctico',
            'Aspectos legales y fiscales',
            'Responsabilidad jurídica de los prestadores de servicios para Internet',
            'Apps: Política de privacidad, términos y condiciones',
            'Consultoría Derecho Digital',
            'Adecuación legal de Proyectos Digitales',
            'Propiedad intelectual (marcas) en entornos  digitales',
            'Nombres de dominio',
            'eCommerce',
            'Reputación Digital',
            'Derechos de la personalidad en entornos digitales',
            'Social media',
            'Gestión jurídica y de comunicación de crisis en entorno digital',
            'Identidad corporativa y publicidad online',
            'Derecho Penal Informático',
            'Estafas (phishing – pharming)',
            'Revelación de secretos empresariales',
            'Vulneración de la intimidad',
            'Amenazas y extorsiones'
        ]
        self.comboAsunto = ttk.Combobox(self, textvariable=self.svAsunto, values=self.lista_asuntos, width=47, font=('ARIAL', 15))
        self.comboAsunto.grid(column=1, row=8, padx=10, pady=5, columnspan=2)

        # --- BOTONES PRINCIPALES (arriba de la tabla) ---
        self.btnNuevo = tk.Button(self, text='Nuevo', command=self.habilitar)
        self.btnNuevo.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, cursor='hand2', activebackground='#3A7DBA')
        self.btnNuevo.grid(row=11, column=0, padx=10, pady=10)

        self.btnGuardar = tk.Button(self, text='Guardar', command=self.guardarCliente)
        self.btnGuardar.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_VERDE, cursor='hand2', activebackground='#388E3C')
        self.btnGuardar.grid(row=11, column=1, padx=10, pady=10)

        self.btnCancelar = tk.Button(self, text='Cancelar', command=self.deshabilitar)
        self.btnCancelar.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, cursor='hand2', activebackground='#3A7DBA')
        self.btnCancelar.grid(row=11, column=2, padx=10, pady=10)

        # --- BUSCADOR ---
        # LABEL BUSCADOR
        self.lblBuscardocumId = tk.Label(self, text='Buscar DocumId: ')
        self.lblBuscardocumId.config(font=('ARIAl',15,'bold'), bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO)
        self.lblBuscardocumId.grid(column=3, row=0, padx=10, pady=5)

        self.lblBuscarApellido = tk.Label(self, text='Buscar Apellido: ')
        self.lblBuscarApellido.config(font=('ARIAl',15,'bold'), bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO)
        self.lblBuscarApellido.grid(column=3, row=1, padx=10, pady=5)

          #ENTRYS BUSCADOR
        self.svBuscardocumId = tk.StringVar()
        self.entryBuscardocumId = tk.Entry(self, textvariable=self.svBuscardocumId)
        self.entryBuscardocumId.config(width=20, font=FUENTE_CONTENIDO)
        self.entryBuscardocumId.grid(column=4, row=0, padx=10, pady=5, columnspan=2)

        self.svBuscarApellido = tk.StringVar()
        self.entryBuscarApellido = tk.Entry(self, textvariable=self.svBuscarApellido)
        self.entryBuscarApellido.config(width=20, font=FUENTE_CONTENIDO)
        self.entryBuscarApellido.grid(column=4, row=1, padx=10, pady=5, columnspan=2)

         #BUTTON BUSCADOR
        self.btnBuscarCondicion = tk.Button(self, text='Buscar', command = self.buscarCondicion)
        self.btnBuscarCondicion.config(width=20, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, cursor='hand2', activebackground='#3A7DBA')
        self.btnBuscarCondicion.grid(column=3,row=2, padx=10, pady=5, columnspan=1)

        self.btnLimpiarBuscador = tk.Button(self, text='Limpiar', command = self.limpiarBuscador)
        self.btnLimpiarBuscador.config(width=20, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, cursor='hand2', activebackground='#3A7DBA')
        self.btnLimpiarBuscador.grid(column=4,row=2, padx=10, pady=5, columnspan=1)
        

    def limpiarBuscador(self):
        self.svBuscarApellido.set('')
        self.svBuscardocumId.set('')
        self.tablaCliente()

    def buscarCondicion(self):
        if len(self.svBuscardocumId.get()) > 0 or len(self.svBuscarApellido.get()) > 0:
            where = "WHERE 1=1"
            if (len(self.svBuscardocumId.get())) > 0:
                where = "WHERE documId = " + self.svBuscardocumId.get() + "" #WHERE documId = 87878787
            if (len(self.svBuscarApellido.get())) > 0:
                where = "WHERE apellido LIKE '" + self.svBuscarApellido.get()+"%' AND activo = 1"
            
            self.tablaCliente(where)
        else:
            self.tablaCliente()


    def guardarCliente(self):
        try:
            # Solo pasar los argumentos que acepta Persona
            persona = Persona(
                self.svNombre.get(), self.svApellido.get(), self.svDocumId.get(), self.svEmail.get(), self.svTelefono.get(),
                self.svNacionalidad.get(), self.svResidencia.get(), self.svAsunto.get(), self.svEstatus.get()
            )
            guardarDatoCliente(persona)
            self.deshabilitar()
            self.tablaCliente()
        except Exception as e:
            print("Error en guardarCliente:", e)
            raise

    def habilitar(self):
        # Habilita los campos de entrada para registrar un nuevo cliente
        self.entryNombre.config(state='normal')
        self.entryApellido.config(state='normal')
        self.entryDocumId.config(state='normal')
        self.entryEmail.config(state='normal')
        self.entryTelefono.config(state='normal')
        self.comboNacionalidad.config(state='normal')
        self.entryResidencia.config(state='normal')
        self.comboAsunto.config(state='normal')
        self.comboEstatus.config(state='normal')
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')
        # Limpia los campos para nuevo registro
        self.svId.set('')
        self.svNombre.set('')
        self.svApellido.set('')
        self.svDocumId.set('')
        self.svEmail.set('')
        self.svTelefono.set('')
        self.svNacionalidad.set('')
        self.svResidencia.set('')
        self.svAsunto.set('')
        self.svEstatus.set('')

    def deshabilitar(self):
        # Deshabilita los campos de entrada y botones de guardar/cancelar
        self.entryNombre.config(state='disabled')
        self.entryApellido.config(state='disabled')
        self.entryDocumId.config(state='disabled')
        self.entryEmail.config(state='disabled')
        self.entryTelefono.config(state='disabled')
        self.comboNacionalidad.config(state='disabled')
        self.entryResidencia.config(state='disabled')
        self.comboAsunto.config(state='disabled')
        self.comboEstatus.config(state='disabled')
        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')

    def _filtrar_nacionalidad(self, event):
        value = self.comboNacionalidad.get().lower()
        if value == '':
            data = self.lista_paises
        else:
            data = [item for item in self.lista_paises if value in item.lower()]
        self.comboNacionalidad['values'] = data
        if data:
            self.comboNacionalidad.event_generate('<Down>')

    def ventanaReportes(self):
        ventana = Toplevel(self)
        ventana.title('Reportes por Estatus y Fecha')
        ventana.geometry('1000x600')
        ventana.config(bg=COLOR_SECUNDARIO)
        notebook = ttk.Notebook(ventana)
        notebook.pack(fill='both', expand=True)

        # Pestañas para cada estatus
        tabs = {}
        for estatus in ["Activo", "En proceso", "Terminado"]:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=estatus)
            tabs[estatus] = tab
            tree = ttk.Treeview(tab, columns=("Id", "Nombre", "Apellido", "DocumId", "Email", "Telefono", "Nacionalidad", "Residencia", "Asunto", "Fecha Historia"), show="headings")
            for col in ("Id", "Nombre", "Apellido", "DocumId", "Email", "Telefono", "Nacionalidad", "Residencia", "Asunto", "Fecha Historia"):
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(fill='both', expand=True)
            # Buscar clientes y su última historia (si existe)
            clientes = listarCondicion(f"WHERE estatus = '{estatus}'")
            from model.historiaConsultaDao import listarHistoria
            for c in clientes:
                historias = listarHistoria(c[0])
                fecha_historia = ''
                if historias:
                    # Tomar la fecha de la última historia (por id más alto)
                    historia_ordenada = sorted(historias, key=lambda h: h[0], reverse=True)
                    fecha_historia = historia_ordenada[0][5] if len(historia_ordenada[0]) > 5 else ''
                tree.insert('', 'end', values=(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], fecha_historia))

        # --- Nueva pestaña: Reporte por Fecha de Historia ---
        tab_fecha = ttk.Frame(notebook)
        notebook.add(tab_fecha, text='Por Fecha Registrado')
        frame_filtros = tk.Frame(tab_fecha, bg=COLOR_TARJETA)
        frame_filtros.pack(fill='x', pady=10)
        Label(frame_filtros, text='Fecha Registrado (YYYY-MM-DD):', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(side='left', padx=5)
        entry_fecha = Entry(frame_filtros, font=FUENTE_CONTENIDO, width=15)
        entry_fecha.pack(side='left', padx=5)
        btn_buscar = Button(frame_filtros, text='Buscar', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', activebackground='#3A7DBA')
        btn_buscar.pack(side='left', padx=5)
        tree_fecha = ttk.Treeview(tab_fecha, columns=("Id", "Nombre", "Apellido", "DocumId", "Email", "Telefono", "Nacionalidad", "Residencia", "Asunto", "Fecha Historia"), show="headings")
        for col in ("Id", "Nombre", "Apellido", "DocumId", "Email", "Telefono", "Nacionalidad", "Residencia", "Asunto", "Fecha Historia"):
            tree_fecha.heading(col, text=col)
            tree_fecha.column(col, width=100)
        tree_fecha.pack(fill='both', expand=True)
        def buscar_por_fecha():
            fecha = entry_fecha.get().strip()
            for item in tree_fecha.get_children():
                tree_fecha.delete(item)
            if fecha:
                clientes = listar()
                from model.historiaConsultaDao import listarHistoria
                for c in clientes:
                    historias = listarHistoria(c[0])
                    for h in historias:
                        fecha_historia = h[5] if len(h) > 5 else ''
                        if fecha_historia == fecha:
                            tree_fecha.insert('', 'end', values=(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], fecha_historia))
        btn_buscar.config(command=buscar_por_fecha)

        # --- BOTÓN DE DESCARGA CON OPCIONES DE FORMATO ---
        frame_export = tk.Frame(ventana, bg=COLOR_SECUNDARIO)
        frame_export.pack(fill='x', pady=5)
        btn_descargar = Button(frame_export, text='Descargar Reporte', bg=COLOR_PRIMARIO, fg='white', font=FUENTE_BOTON, command=lambda: mostrar_opciones_descarga())
        btn_descargar.pack(side='left', padx=5)

        def mostrar_opciones_descarga():
            top = Toplevel(ventana)
            top.title('Selecciona el formato de descarga')
            top.geometry('300x150')
            top.config(bg=COLOR_TARJETA)
            Label(top, text='Elige el formato:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=10)
            Button(top, text='PNG', width=15, font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', command=lambda: [exportar_png(ventana), top.destroy()]).pack(pady=5)
            Button(top, text='CSV', width=15, font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', command=lambda: [exportar_csv(), top.destroy()]).pack(pady=5)
            Button(top, text='Excel', width=15, font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', command=lambda: [exportar_excel(), top.destroy()]).pack(pady=5)

        def generar_nombre_archivo(base, ext):
            fecha = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            return f"{base}_{fecha}.{ext}"

        def exportar_png(win):
            try:
                from PIL import ImageGrab
                x = win.winfo_rootx()
                y = win.winfo_rooty()
                w = win.winfo_width()
                h = win.winfo_height()
                img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
                nombre = generar_nombre_archivo("reporte", "png")
                img.save(nombre)
                messagebox.showinfo("Exportar PNG", f"Reporte guardado como {nombre}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar PNG: {e}")

        def exportar_csv():
            try:
                import pandas as pd
                tab = notebook.nametowidget(notebook.select())
                tree = next((w for w in tab.winfo_children() if isinstance(w, ttk.Treeview)), None)
                if not tree:
                    messagebox.showerror("Error", "No se encontró la tabla para exportar.")
                    return
                data = [tree.item(item)['values'] for item in tree.get_children()]
                cols = [tree.heading(col)["text"] for col in tree["columns"]]
                df = pd.DataFrame(data, columns=cols)
                nombre = generar_nombre_archivo("reporte", "csv")
                df.to_csv(nombre, index=False)
                messagebox.showinfo("Exportar CSV", f"Reporte guardado como {nombre}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar CSV: {e}")

        def exportar_excel():
            try:
                import pandas as pd
                tab = notebook.nametowidget(notebook.select())
                tree = next((w for w in tab.winfo_children() if isinstance(w, ttk.Treeview)), None)
                if not tree:
                    messagebox.showerror("Error", "No se encontró la tabla para exportar.")
                    return
                data = [tree.item(item)['values'] for item in tree.get_children()]
                cols = [tree.heading(col)["text"] for col in tree["columns"]]
                df = pd.DataFrame(data, columns=cols)
                nombre = generar_nombre_archivo("reporte", "xlsx")
                df.to_excel(nombre, index=False)
                messagebox.showinfo("Exportar Excel", f"Reporte guardado como {nombre}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar Excel: {e}")

    def editarCliente(self):
        # Permite editar el cliente seleccionado in la tabla
        seleccionado = self.treeClientes.focus()
        print(f"DEBUG editarCliente: seleccionado={seleccionado}")
        if not seleccionado:
            messagebox.showwarning('Editar Cliente', 'Seleccione un cliente de la tabla.')
            return
        valores = self.treeClientes.item(seleccionado, 'values')
        print(f"DEBUG editarCliente: valores={valores}")
        if not valores or len(valores) < 10:
            messagebox.showerror('Editar Cliente', 'No se pudieron obtener los datos del cliente seleccionado.')
            return
        self.habilitar()  # Habilitar primero
        self.svId.set(valores[0])
        self.svNombre.set(valores[1])
        self.svApellido.set(valores[2])
        self.svDocumId.set(valores[3])
        self.svEmail.set(valores[4])
        self.svTelefono.set(valores[5])
        self.svNacionalidad.set(valores[6])
        self.svResidencia.set(valores[7])
        self.svAsunto.set(valores[8])
        self.svEstatus.set(valores[9])
        self.btnGuardar.config(command=self.actualizarCliente)

    def actualizarCliente(self):
        # Actualiza el cliente editado
        # Validar que ningún campo esté vacío y que el ID sea válido
        if not self.svId.get() or not self.svNombre.get() or not self.svApellido.get() or not self.svDocumId.get():
            messagebox.showwarning('Actualizar Cliente', 'Debe seleccionar un cliente y completar todos los campos obligatorios.')
            return
        try:
            persona = Persona(
                self.svNombre.get(), self.svApellido.get(), self.svDocumId.get(), self.svEmail.get(), self.svTelefono.get(),
                self.svNacionalidad.get(), self.svResidencia.get(), self.svAsunto.get(), self.svEstatus.get()
            )
            editarDatoCliente(persona, self.svId.get())
            self.deshabilitar()
            self.tablaCliente()
            self.btnGuardar.config(command=self.guardarCliente)
        except Exception as e:
            messagebox.showerror('Error', f'Error al actualizar cliente: {e}')

    def eliminarCliente(self):
        # Elimina el cliente seleccionado
        seleccionado = self.treeClientes.focus()
        if not seleccionado:
            messagebox.showwarning('Eliminar Cliente', 'Seleccione un cliente de la tabla.')
            return
        valores = self.treeClientes.item(seleccionado, 'values')
        respuesta = messagebox.askyesno('Eliminar Cliente', f'¿Está seguro de eliminar al cliente {valores[1]} {valores[2]}?')
        if respuesta:
            eliminarCliente(valores[0])
            self.tablaCliente()

    def abrirHistoriaCliente(self):
        # Muestra la historia del cliente seleccionado
        seleccionado = self.treeClientes.focus()
        if not seleccionado:
            messagebox.showwarning('Historia Cliente', 'Seleccione un cliente de la tabla.')
            return
        valores = self.treeClientes.item(seleccionado, 'values')
        id_cliente = valores[0]
        ventana = Toplevel(self)
        ventana.title(f'Historia de {valores[1]} {valores[2]}')
        ventana.geometry('900x500')
        ventana.config(bg=COLOR_SECUNDARIO)
        # Actualizar columnas: Id, Nombre y Apellido, Atendido por, Observaciones, Fecha
        tree = ttk.Treeview(ventana, columns=("Id", "Nombre y Apellido", "Atendido por", "Observaciones", "Fecha"), show="headings")
        tree.heading("Id", text="Id")
        tree.heading("Nombre y Apellido", text="Nombre y Apellido")
        tree.heading("Atendido por", text="Atendido por")
        tree.heading("Observaciones", text="Observaciones")
        tree.heading("Fecha", text="Fecha de registro")
        tree.column("Id", width=60)
        tree.column("Nombre y Apellido", width=180)
        tree.column("Atendido por", width=180)
        tree.column("Observaciones", width=400)
        tree.column("Fecha", width=120)
        tree.pack(fill='both', expand=True)
        # --- BOTONES DE HISTORIAL ---
        frame_botones = tk.Frame(ventana, bg=COLOR_SECUNDARIO)
        frame_botones.pack(fill='x', pady=10)
        btn_agregar = tk.Button(frame_botones, text='Agregar Historia', width=18, font=FUENTE_BOTON, fg='white', bg=COLOR_VERDE, activebackground='#388E3C', cursor='hand2', command=lambda: self.agregarHistoria(id_cliente, tree, ventana))
        btn_agregar.pack(side='left', padx=10)
        btn_editar = tk.Button(frame_botones, text='Editar Historia', width=18, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, activebackground='#3A7DBA', cursor='hand2', command=lambda: self.editarHistoria(tree, ventana))
        btn_editar.pack(side='left', padx=10)
        btn_eliminar = tk.Button(frame_botones, text='Eliminar Historia', width=18, font=FUENTE_BOTON, fg='white', bg=COLOR_ROJO, activebackground='#B71C1C', cursor='hand2', command=lambda: self.eliminarHistoria(tree, ventana))
        btn_eliminar.pack(side='left', padx=10)
        btn_salir = tk.Button(frame_botones, text='Salir', width=18, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, activebackground='#3A7DBA', cursor='hand2', command=ventana.destroy)
        btn_salir.pack(side='right', padx=10)
        # --- LLENAR TABLA DESPUÉS DE LOS BOTONES ---
        historias = listarHistoria(id_cliente)
        for h in historias:
            # h: (idHistoriaConsulta, NombreCompleto, atendidoPor, observaciones, fecha)
            if len(h) > 4:
                tree.insert('', 'end', values=(h[0], h[1], h[2], h[3], h[4]))
            else:
                tree.insert('', 'end', values=(h[0], h[1], h[2], h[3], h[4] if len(h) > 3 else ''))

    def agregarHistoria(self, id_cliente, tree, ventana):
        def guardar():
            btn_guardar.config(state='disabled')  # Deshabilita el botón para evitar doble click
            atendido_por = entry_atendido_por.get()
            observaciones = entry_observaciones.get("1.0", "end").strip()
            fecha = entry_fecha.get() if hasattr(entry_fecha, 'get') else ''
            if not atendido_por or not observaciones or not fecha:
                from tkinter import messagebox
                messagebox.showwarning('Campos requeridos', 'Debe completar todos los campos.')
                btn_guardar.config(state='normal')  # Rehabilita si hay error
                return
            from model.historiaConsultaDao import guardarHistoria
            guardarHistoria(id_cliente, atendido_por, observaciones, fecha)
            top.destroy()
            self.refrescar_historial(tree, id_cliente)
        from tkinter import Toplevel, Label, Entry, Text, Button
        try:
            from tkcalendar import DateEntry
        except ImportError:
            DateEntry = None
        top = Toplevel(ventana)
        top.title('Agregar Historia')
        top.geometry('500x400')
        top.config(bg=COLOR_TARJETA)
        # --- CAMPO NOMBRE Y APELLIDO (deshabilitado) ---
        Label(top, text='Nombre y Apellido:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        entry_nombre_apellido = Entry(top, font=FUENTE_CONTENIDO, state='normal')
        # Buscar nombre y apellido del cliente
        persona = None
        for c in self.treeClientes.get_children():
            if str(self.treeClientes.item(c, 'values')[0]) == str(id_cliente):
                persona = self.treeClientes.item(c, 'values')
                break
        if persona:
            entry_nombre_apellido.insert(0, f"{persona[1]} {persona[2]}")
            entry_nombre_apellido.config(state='readonly', disabledbackground='#f0f0f0', disabledforeground='#000000')
        entry_nombre_apellido.pack(pady=5, fill='x', padx=20)
        # --- CAMPO ATENDIDO POR ---
        Label(top, text='Atendido por:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        entry_atendido_por = Entry(top, font=FUENTE_CONTENIDO)
        entry_atendido_por.pack(pady=5, fill='x', padx=20)
        entry_atendido_por.delete(0, END)  # Asegura que siempre esté vacío
        # --- CAMPO OBSERVACIONES ---
        Label(top, text='Observaciones:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        entry_observaciones = Text(top, font=FUENTE_CONTENIDO, height=5)
        entry_observaciones.pack(pady=5, fill='x', padx=20)
        # --- CAMPO FECHA DE REGISTRO ---
        Label(top, text='Fecha de registro:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        if DateEntry:
            entry_fecha = DateEntry(top, font=FUENTE_CONTENIDO, date_pattern='yyyy-mm-dd')
        else:
            entry_fecha = Entry(top, font=FUENTE_CONTENIDO)
        entry_fecha.pack(pady=5, fill='x', padx=20)
        # --- BOTONES GUARDAR Y CANCELAR ---
        frame_botones = tk.Frame(top, bg=COLOR_TARJETA)
        frame_botones.pack(side='bottom', pady=20)
        btn_guardar = Button(frame_botones, text='Guardar', command=guardar, bg=COLOR_VERDE, fg='white', font=FUENTE_BOTON, activebackground='#388E3C', width=12)
        btn_guardar.pack(side='left', padx=10)
        btn_cancelar = Button(frame_botones, text='Cancelar', command=top.destroy, bg=COLOR_PRIMARIO, fg='white', font=FUENTE_BOTON, width=12)
        btn_cancelar.pack(side='left', padx=10)

    def editarHistoria(self, tree, ventana):
        seleccionado = tree.focus()
        if not seleccionado:
            from tkinter import messagebox
            messagebox.showwarning('Editar Historia', 'Seleccione una historia de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        id_historia = valores[0]
        atendido_actual = valores[2] if len(valores) > 2 else ''
        observaciones_actual = valores[3] if len(valores) > 3 else ''
        fecha_actual = valores[4] if len(valores) > 4 else ''
        def guardar():
            atendido_por = entry_atendido_por.get()
            observaciones = entry_observaciones.get("1.0", "end").strip()
            fecha = entry_fecha.get() if hasattr(entry_fecha, 'get') else ''
            if not atendido_por or not observaciones or not fecha:
                from tkinter import messagebox
                messagebox.showwarning('Campos requeridos', 'Debe completar todos los campos.')
                return
            from model.historiaConsultaDao import editarHistoria
            editarHistoria(atendido_por, observaciones, fecha, id_historia)
            top.destroy()
            self.refrescar_historial(tree, self.id_cliente_historial(tree, id_historia))
        from tkinter import Toplevel, Label, Entry, Text, Button, Frame
        import tkinter as tk
        try:
            from tkcalendar import DateEntry
        except ImportError:
            DateEntry = None
        top = Toplevel(ventana)
        top.title('Editar Historia')
        top.geometry('500x400')
        top.config(bg=COLOR_TARJETA)
        # --- CAMPO NOMBRE Y APELLIDO (habilitado pero no editable) ---
        Label(top, text='Nombre y Apellido:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        entry_nombre_apellido = Entry(top, font=FUENTE_CONTENIDO, state='normal')
        # Obtener nombre y apellido del cliente seleccionado en la tabla principal
        persona = None
        for c in self.treeClientes.get_children():
            if str(self.treeClientes.item(c, 'values')[0]) == str(self.id_cliente_historial(tree, id_historia)):
                persona = self.treeClientes.item(c, 'values')
                break
        if persona:
            entry_nombre_apellido.insert(0, f"{persona[1]} {persona[2]}")
            entry_nombre_apellido.config(state='readonly', disabledbackground='#f0f0f0', disabledforeground='#000000')
        entry_nombre_apellido.pack(pady=5, fill='x', padx=20)
        # --- CAMPO ATENDIDO POR (dejar vacío) ---
        Label(top, text='Atendido por:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        entry_atendido_por = Entry(top, font=FUENTE_CONTENIDO)
        entry_atendido_por.pack(pady=5, fill='x', padx=20)
        entry_atendido_por.delete(0, END)  # Siempre vacío al abrir
        # --- CAMPO OBSERVACIONES ---
        Label(top, text='Observaciones:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        entry_observaciones = Text(top, font=FUENTE_CONTENIDO, height=5)
        entry_observaciones.insert('1.0', observaciones_actual)
        entry_observaciones.pack(pady=5, fill='x', padx=20)
        # --- CAMPO FECHA DE REGISTRO ---
        Label(top, text='Fecha de registro:', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA).pack(pady=5)
        if DateEntry:
            entry_fecha = DateEntry(top, font=FUENTE_CONTENIDO, date_pattern='yyyy-mm-dd')
            if fecha_actual:
                try:
                    entry_fecha.set_date(fecha_actual)
                except Exception:
                    import datetime
                    entry_fecha.set_date(datetime.date.today())
        else:
            entry_fecha = Entry(top, font=FUENTE_CONTENIDO)
            entry_fecha.insert(0, fecha_actual)
        entry_fecha.pack(pady=5, fill='x', padx=20)
        # --- BOTONES GUARDAR Y CANCELAR ---
        frame_botones = tk.Frame(top, bg=COLOR_TARJETA)
        frame_botones.pack(side='bottom', pady=20)
        btn_guardar = Button(frame_botones, text='Guardar', command=guardar, bg=COLOR_VERDE, fg='white', font=FUENTE_BOTON, activebackground='#388E3C', width=12)
        btn_guardar.pack(side='left', padx=10)
        btn_cancelar = Button(frame_botones, text='Cancelar', command=top.destroy, bg=COLOR_PRIMARIO, fg='white', font=FUENTE_BOTON, width=12)
        btn_cancelar.pack(side='left', padx=10)

    def id_cliente_historial(self, tree, id_historia):
        # Busca el id_cliente a partir del id_historia
        from model.conexion import ConexionDB
        conexion = ConexionDB()
        sql = 'SELECT idPersona FROM historiaConsulta WHERE idHistoriaConsulta = ?'
        conexion.cursor.execute(sql, (id_historia,))
        row = conexion.cursor.fetchone()
        conexion.cerrarConexion()
        return row[0] if row else None

    def eliminarHistoria(self, tree, ventana):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning('Eliminar Historia', 'Seleccione una historia de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        id_historia = valores[0]
        if messagebox.askyesno('Eliminar Historia', '¿Está seguro de eliminar esta historia?'):
            eliminarHistoria(id_historia)
            # Buscar el id_cliente del historial mostrado
            id_cliente = self.id_cliente_historial(tree, id_historia)
            self.refrescar_historial(tree, id_cliente)

    def refrescar_historial(self, tree, id_cliente):
        # Refresca la tabla de historial tras agregar/editar/eliminar
        for item in tree.get_children():
            tree.delete(item)
        historias = listarHistoria(id_cliente)
        for h in historias:
            # h: (idHistoriaConsulta, NombreCompleto, atendidoPor, observaciones, fecha)
            # Tabla espera: Id, Nombre y Apellido, Atendido por, Observaciones, Fecha
            if len(h) > 4:
                tree.insert('', 'end', values=(h[0], h[1], h[2], h[3], h[4]))
            else:
                tree.insert('', 'end', values=(h[0], h[1], h[2], h[3], h[4] if len(h) > 3 else ''))

    def obtener_id_cliente_de_historial(self, tree):
        # Busca el id_cliente a partir del primer registro mostrado (asume que todos son del mismo cliente)
        items = tree.get_children()
        if items:
            id_historia = tree.item(items[0], 'values')[0]
            from model.historiaConsultaDao import listarHistoria
            # Buscar el id_cliente a partir de la historia (opcional: podrías guardar el id_cliente en la ventana)
            # Aquí simplemente retornamos el id_historia usado en la última consulta
            # Si no hay historias, retorna None
            historias = listarHistoria(id_historia)
            if historias:
                return id_historia  # O ajusta según tu modelo
        return None

    def agregar_logo_empresa(self):
        # Cargar y mostrar el logo in la parte vacía inferior derecha de la ventana principal
        try:
            from PIL import Image, ImageTk
            logo_path = 'logo_empresa.png'  # Cambia el nombre si tu logo tiene otro nombre
            img = Image.open(logo_path)
            img = img.resize((300, 300), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            # Coloca el logo en la parte inferior derecha, ajusta x/y según tu layout
            self.lblLogo = tk.Label(self, image=self.logo_img, bg=COLOR_SECUNDARIO)
            self.lblLogo.image = self.logo_img
            self.lblLogo.place(x=850, y=140)  # Ajusta estos valores para mover el logo
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

    def salir(self):
        self.root.destroy()

    def tablaCliente(self, where=None):
        # Muestra la tabla de clientes con datos reales desde la base de datos
        if hasattr(self, 'treeClientes'):
            self.treeClientes.destroy()
        columnas = ("Id", "Nombre", "Apellido", "DocumId", "Email", "Telefono", "Nacionalidad", "Residencia", "Asunto", "Estatus")
        self.treeClientes = ttk.Treeview(self, columns=columnas, show="headings")
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', font=FUENTE_CONTENIDO, rowheight=28, background=COLOR_TARJETA, fieldbackground=COLOR_TARJETA)
        style.configure('Treeview.Heading', font=FUENTE_LABEL, background=COLOR_PRIMARIO, foreground='white')
        self.treeClientes.tag_configure('activo', background=COLOR_SECUNDARIO)
        self.treeClientes.tag_configure('inactivo', background=COLOR_TARJETA)
        self.treeClientes.grid(row=13, column=0, columnspan=6, padx=10, pady=10)

        # --- LLENAR TABLA CON DATOS ---
        from model.clienteDao import listar, listarCondicion
        if where:
            clientes = listarCondicion(where)
        else:
            clientes = listar()
        for c in clientes:
            estado_tag = 'activo' if c[9] == 'Activo' else 'inactivo'
            self.treeClientes.insert('', 'end', values=(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]), tags=(estado_tag,))

        # --- BOTONES SECUNDARIOS (debajo de la tabla) ---
        self.btnEditar = tk.Button(self, text='Editar Cliente', command=self.editarCliente)
        self.btnEditar.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, cursor='hand2', activebackground='#3A7DBA')
        self.btnEditar.grid(row=15, column=0, padx=10, pady=15)

        self.btnEliminar = tk.Button(self, text='Eliminar Cliente', command=self.eliminarCliente)
        self.btnEliminar.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_ROJO, cursor='hand2', activebackground='#B71C1C')
        self.btnEliminar.grid(row=15, column=1, padx=10, pady=15)

        self.btnHistoria = tk.Button(self, text='Historia Cliente', command=self.abrirHistoriaCliente)
        self.btnHistoria.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, cursor='hand2', activebackground='#3A7DBA')
        self.btnHistoria.grid(row=15, column=2, padx=10, pady=15)

        self.btnReportes = tk.Button(self, text='Reportes', command=self.ventanaReportes)
        self.btnReportes.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, activebackground='#3A7DBA', cursor='hand2')
        self.btnReportes.grid(row=15, column=3, padx=10, pady=15)

        self.btnSalir = tk.Button(self, text='Salir', command=self.salir)
        self.btnSalir.config(width=15, font=FUENTE_BOTON, fg='white', bg=COLOR_PRIMARIO, activebackground='#3A7DBA', cursor='hand2')
        self.btnSalir.grid(row=15, column=4, padx=10, pady=15)

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Menú Principal - Consultorio Técnico/Jurídico')
        self.geometry('1100x700')
        self.config(bg=COLOR_SECUNDARIO)
        self._crear_widgets()

    def _crear_widgets(self):
        import os
        # --- Barra lateral compacta con íconos + texto y efecto hover ---
        self.sidebar = tk.Frame(self, bg=COLOR_PRIMARIO, width=80)
        self.sidebar.pack(side='left', fill='y')
        # Cargar íconos (usar emojis si no hay imágenes)
        icon_size = (28, 28)
        try:
            from PIL import Image, ImageTk
            def load_icon(filename):
                path = os.path.join(os.path.dirname(__file__), '..', filename)
                img = Image.open(path)
                img = img.resize(icon_size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            self.icon_nuevo = load_icon('icon_nuevo.png')
            self.icon_lista = load_icon('icon_lista.png')
            self.icon_reportes = load_icon('icon_reportes.png')
            self.icon_salir = load_icon('icon_salir.png')
        except Exception:
            self.icon_nuevo = None
            self.icon_lista = None
            self.icon_reportes = None
            self.icon_salir = None
        # --- Botón helper con hover ---
        def crear_boton_menu(parent, icon, texto, comando):
            btn = tk.Frame(parent, bg=COLOR_PRIMARIO, cursor='hand2')
            btn.pack(fill='x', pady=2)
            def on_enter(e):
                btn.config(bg='#3A7DBA')
                lbl_icon.config(bg='#3A7DBA')
                lbl_texto.config(bg='#3A7DBA')
            def on_leave(e):
                btn.config(bg=COLOR_PRIMARIO)
                lbl_icon.config(bg=COLOR_PRIMARIO)
                lbl_texto.config(bg=COLOR_PRIMARIO)
            if icon:
                lbl_icon = tk.Label(btn, image=icon, bg=COLOR_PRIMARIO)
            else:
                # Usa emoji si no hay icono
                emoji = {
                    'Ingresar Nuevo Cliente': '📝',
                    'Lista de Clientes': '📋',
                    'Reportes': '📊',
                    'Salir': '🚪',
                }.get(texto, '🔹')
                lbl_icon = tk.Label(btn, text=emoji, font=('Segoe UI', 18), bg=COLOR_PRIMARIO, fg='white')
            lbl_icon.pack(side='left', padx=10, pady=8)
            lbl_texto = tk.Label(btn, text=texto, font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white')
            lbl_texto.pack(side='left', padx=6)
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            lbl_icon.bind('<Enter>', on_enter)
            lbl_icon.bind('<Leave>', on_leave)
            lbl_texto.bind('<Enter>', on_enter)
            lbl_texto.bind('<Leave>', on_leave)
            btn.bind('<Button-1>', lambda e: comando())
            lbl_icon.bind('<Button-1>', lambda e: comando())
            lbl_texto.bind('<Button-1>', lambda e: comando())
            return btn
        # --- Menú lateral ---
        crear_boton_menu(self.sidebar, self.icon_nuevo, 'Ingresar Nuevo Cliente', self.mostrar_nuevo_cliente)
        crear_boton_menu(self.sidebar, self.icon_lista, 'Lista de Clientes', self.mostrar_lista_clientes)
        crear_boton_menu(self.sidebar, self.icon_reportes, 'Reportes', self.mostrar_reportes)
        crear_boton_menu(self.sidebar, self.icon_salir, 'Salir', self.destroy)
        # --- Panel central ---
        self.central_frame = tk.Frame(self, bg=COLOR_SECUNDARIO)
        self.central_frame.pack(side='left', fill='both', expand=True)
        self.mostrar_info_institucional()

    def limpiar_central(self):
        for widget in self.central_frame.winfo_children():
            widget.destroy()

    def mostrar_info_institucional(self):
        self.limpiar_central()
        # --- Hero institucional ---
        hero = tk.Frame(self.central_frame, bg=COLOR_TARJETA, bd=0, highlightthickness=0)
        hero.place(relx=0.5, rely=0.25, anchor='center', relwidth=0.7, relheight=0.32)
        # Sombra simulada
        sombra = tk.Frame(self.central_frame, bg='#e0e0e0')
        sombra.place(relx=0.5, rely=0.25+0.03, anchor='center', relwidth=0.7, relheight=0.32)
        hero.lift()
        # Hero visual
        tk.Label(hero, text='OFICINA TÉCNICO - JURÍDICA', font=FUENTE_TITULO_GRANDE, bg=COLOR_TARJETA, fg=COLOR_PRIMARIO).pack(pady=(30, 10))
        tk.Label(hero, text='Consultoría y asesoría en derecho digital, ciberseguridad y tecnología', font=FUENTE_CONTENIDO, bg=COLOR_TARJETA, fg='#444', wraplength=700, justify='center').pack(pady=(0, 18))
        # --- Info institucional debajo del hero ---
        info = tk.Frame(self.central_frame, bg=COLOR_SECUNDARIO)
        info.place(relx=0.5, rely=0.60, anchor='center', relwidth=0.8)
        def seccion(titulo, texto):
            tk.Label(info, text=titulo, font=FUENTE_TITULO, bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO).pack(anchor='w', pady=(10, 0))
            tk.Label(info, text=texto, font=FUENTE_CONTENIDO, bg=COLOR_SECUNDARIO, fg='#222', wraplength=800, justify='left').pack(anchor='w', pady=(0, 8))
        seccion('¿Qué es?', 'La Oficina Técnico-Jurídica es un espacio de atención y asesoría en temas legales y tecnológicos.')
        seccion('¿Para qué funciona?', 'Brindamos orientación, consultoría y acompañamiento en protección de datos, derecho digital, ciberseguridad, y más.')
        seccion('¿A quiénes está dirigido?', 'Empresas, emprendedores, profesionales, estudiantes y cualquier persona interesada en el ámbito legal y tecnológico.')

    def mostrar_nuevo_cliente(self):
        self.limpiar_central()
        from tkinter import ttk
        labels = [
            ('Nombre', True), ('Apellido', True), ('DocumId', True), ('Email', True), ('Telefono', True),
            ('Nacionalidad', True), ('Residencia', False), ('Asunto', True), ('Estatus', True)
        ]
        entries = {}
        # --- Tarjeta blanca con sombra ---
        sombra = tk.Frame(self.central_frame, bg='#e0e0e0')
        sombra.place(relx=0.5, rely=0.5+0.025, anchor='center', relwidth=0.52, relheight=0.68)
        card = tk.Frame(self.central_frame, bg=COLOR_TARJETA, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.52, relheight=0.68)
        card.lift()
        # --- Título ---
        tk.Label(card, text='Nuevo Cliente', font=FUENTE_TITULO, bg=COLOR_TARJETA, fg=COLOR_PRIMARIO).grid(row=0, column=0, columnspan=2, pady=(24, 10))
        # --- Campos ---
        for idx, (label, obligatorio) in enumerate(labels):
            label_text = label + (" *" if obligatorio else "")
            tk.Label(card, text=label_text, font=FUENTE_LABEL, bg=COLOR_TARJETA, fg=COLOR_PRIMARIO if obligatorio else '#444').grid(row=idx+1, column=0, padx=20, pady=10, sticky='e')
            style = ttk.Style()
            style.theme_use('default')
            style.configure('Modern.TCombobox', relief='flat', borderwidth=1, padding=8, font=FUENTE_CONTENIDO, foreground='#222', background='white', fieldbackground='white')
            style.map('Modern.TCombobox', fieldbackground=[('readonly', 'white')])
            if label in ['Nacionalidad', 'Asunto', 'Estatus']:
                if label == 'Nacionalidad':
                    nacionalidades = [
                        'Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Ecuador', 'Paraguay', 'Perú', 'Uruguay', 'Venezuela',
                        'México', 'España', 'Estados Unidos', 'Otro'
                    ]
                    entry = ttk.Combobox(card, values=nacionalidades, font=FUENTE_CONTENIDO, width=32, style='Modern.TCombobox')
                elif label == 'Asunto':
                    asuntos = [
                        'Asesoría en Protección de Datos para empresas',
                        'Buenas Prácticas Digitales en el Puesto de Trabajo',
                        'Seguridad de la Información-Ciberseguridad',
                        'Auditorías de Sistemas de Información',
                        'Compliance',
                        'Adecuación al marco normativo y práctico',
                        'Aspectos legales y fiscales',
                        'Responsabilidad jurídica de los prestadores de servicios para Internet',
                        'Apps: Política de privacidad, términos y condiciones',
                        'Consultoría Derecho Digital',
                        'Adecuación legal de Proyectos Digitales',
                        'Propiedad intelectual (marcas) en entornos  digitales',
                        'Nombres de dominio',
                        'eCommerce',
                        'Reputación Digital',
                        'Derechos de la personalidad en entornos digitales',
                        'Social media',
                        'Gestión jurídica y de comunicación de crisis en entorno digital',
                        'Identidad corporativa y publicidad online',
                        'Derecho Penal Informático',
                        'Estafas (phishing – pharming)',
                        'Revelación de secretos empresariales',
                        'Vulneración de la intimidad',
                        'Amenazas y extorsiones'
                    ]
                    entry = ttk.Combobox(card, values=asuntos, font=FUENTE_CONTENIDO, width=32, style='Modern.TCombobox')
                else:
                    estatuses = ['Activo', 'En proceso', 'Terminado']
                    entry = ttk.Combobox(card, values=estatuses, font=FUENTE_CONTENIDO, width=32, state='readonly', style='Modern.TCombobox')
            else:
                entry = tk.Entry(card, font=FUENTE_CONTENIDO, width=34, relief='flat', highlightthickness=1, highlightbackground='#bbb')
            entry.grid(row=idx+1, column=1, padx=10, pady=10, sticky='w')
            entries[label] = (entry, obligatorio)
        # --- Botones Guardar y Cancelar centrados en la tarjeta ---
        btns_frame = tk.Frame(card, bg=COLOR_TARJETA)
        btns_frame.grid(row=len(labels)+2, column=0, columnspan=2, pady=24)
        btn_guardar = tk.Button(btns_frame, text='Guardar', font=FUENTE_BOTON, bg=COLOR_VERDE, fg='white', width=14, activebackground='#388E3C', command=lambda: guardar())
        btn_guardar.pack(side='left', padx=30)
        btn_cancelar = tk.Button(btns_frame, text='Cancelar', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', width=14, activebackground='#3A7DBA', command=self.mostrar_info_institucional)
        btn_cancelar.pack(side='left', padx=30)
        # --- Botones clásicos debajo de la tarjeta (restaurados) ---
        btns_frame2 = tk.Frame(self.central_frame, bg=COLOR_SECUNDARIO)
        btns_frame2.place(relx=0.5, rely=0.5+0.38, anchor='center')
        btn_guardar2 = tk.Button(btns_frame2, text='Guardar', font=FUENTE_BOTON, bg=COLOR_VERDE, fg='white', width=14, activebackground='#388E3C', command=lambda: guardar())
        btn_guardar2.pack(side='left', padx=30)
        btn_cancelar2 = tk.Button(btns_frame2, text='Cancelar', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', width=14, activebackground='#3A7DBA', command=self.mostrar_info_institucional)
        btn_cancelar2.pack(side='left', padx=30)
        # --- Toast notification helper ---
        def show_toast(msg, color):
            toast = tk.Toplevel(self)
            toast.overrideredirect(True)
            toast.config(bg=color)
            toast.attributes('-topmost', True)
            x = self.winfo_x() + self.winfo_width() - 340
            y = self.winfo_y() + self.winfo_height() - 100
            toast.geometry(f"+{x}+{y}")
            label = tk.Label(toast, text=msg, bg=color, fg='white', font=FUENTE_CONTENIDO)
            label.pack(padx=10, pady=5)
            toast.after(3000, toast.destroy)
        # --- Guardar cliente ---
        def guardar():
            # Validar campos obligatorios
            for key, (entry, obligatorio) in entries.items():
                if obligatorio and not entry.get():
                    entry.focus()
                    messagebox.showwarning('Campo obligatorio', f'El campo "{key}" es obligatorio.')
                    return
            try:
                persona = Persona(
                    entries['Nombre'][0].get(),
                    entries['Apellido'][0].get(),
                    entries['DocumId'][0].get(),
                    entries['Email'][0].get(),
                    entries['Telefono'][0].get(),
                    entries['Nacionalidad'][0].get(),
                    entries['Residencia'][0].get(),
                    entries['Asunto'][0].get(),
                    entries['Estatus'][0].get()
                )
                guardarDatoCliente(persona)
                show_toast('Cliente guardado con éxito.', COLOR_VERDE)
                self.mostrar_info_institucional()
            except Exception as e:
                messagebox.showerror('Error al guardar', str(e))

    def mostrar_lista_clientes(self):
        self.limpiar_central()
        from tkinter import ttk
        card = tk.Frame(self.central_frame, bg=COLOR_TARJETA, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.92, relheight=0.82)
        card.lift()
        # Título
        tk.Label(card, text='Lista de Clientes', font=FUENTE_TITULO, bg=COLOR_TARJETA, fg=COLOR_PRIMARIO).pack(pady=(18, 8))
        # Tabla
        columnas = ("Id", "Nombre", "Apellido", "DocumId", "Email", "Telefono", "Nacionalidad", "Residencia", "Asunto", "Estatus")
        tree = ttk.Treeview(card, columns=columnas, show="headings")
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', font=FUENTE_CONTENIDO, rowheight=28, background=COLOR_TARJETA, fieldbackground=COLOR_TARJETA)
        style.configure('Treeview.Heading', font=FUENTE_LABEL, background=COLOR_PRIMARIO, foreground='white')
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill='both', expand=True, padx=18, pady=10)
        # Llenar datos
        from model.clienteDao import listar
        for c in listar():
            estado_tag = 'activo' if c[9] == 'Activo' else 'inactivo'
            tree.insert('', 'end', values=(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]), tags=(estado_tag,))
        # --- Botones clásicos debajo de la tabla ---
        btns_frame = tk.Frame(card, bg=COLOR_TARJETA)
        btns_frame.pack(pady=10)
        btn_editar = tk.Button(btns_frame, text='Editar Cliente', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', width=15, activebackground='#3A7DBA', command=lambda: self._editar_cliente_tabla(tree))
        btn_editar.pack(side='left', padx=10)
        btn_eliminar = tk.Button(btns_frame, text='Eliminar Cliente', font=FUENTE_BOTON, bg=COLOR_ROJO, fg='white', width=15, activebackground='#B71C1C', command=lambda: self._eliminar_cliente_tabla(tree))
        btn_eliminar.pack(side='left', padx=10)
        btn_historial = tk.Button(btns_frame, text='Historia Cliente', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', width=15, activebackground='#3A7DBA', command=lambda: self._historial_cliente_tabla(tree))
        btn_historial.pack(side='left', padx=10)
        btn_volver = tk.Button(btns_frame, text='Volver', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', width=15, activebackground='#3A7DBA', command=self.mostrar_info_institucional)
        btn_volver.pack(side='left', padx=10)

    def _editar_cliente_tabla(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning('Editar Cliente', 'Seleccione un cliente de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        if not valores or len(valores) < 10:
            messagebox.showerror('Editar Cliente', 'No se pudieron obtener los datos del cliente seleccionado.')
            return
        # Lógica: cargar datos en el formulario de edición
        self.mostrar_nuevo_cliente()
        # Rellenar los campos del formulario con los valores seleccionados
        # ...existing code for rellenar campos si es necesario...

    def _eliminar_cliente_tabla(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning('Eliminar Cliente', 'Seleccione un cliente de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        respuesta = messagebox.askyesno('Eliminar Cliente', f'¿Está seguro de eliminar al cliente {valores[1]} {valores[2]}?')
        if respuesta:
            from model.clienteDao import eliminarCliente
            eliminarCliente(valores[0])
            self.mostrar_lista_clientes()

    def _historial_cliente_tabla(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning('Historia Cliente', 'Seleccione un cliente de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        id_cliente = valores[0]
        # Reutilizar la ventana de historial clásica
        self.abrirHistoriaCliente_tabla(id_cliente, valores)

    def abrirHistoriaCliente_tabla(self, id_cliente, valores):
        ventana = Toplevel(self)
        ventana.title(f'Historia de {valores[1]} {valores[2]}')
        ventana.geometry('900x500')
        ventana.config(bg=COLOR_SECUNDARIO)
        from model.historiaConsultaDao import listarHistoria
        tree = ttk.Treeview(ventana, columns=("Id", "Nombre y Apellido", "Atendido por", "Observaciones", "Fecha"), show="headings")
        tree.heading("Id", text="Id")
        tree.heading("Nombre y Apellido", text="Nombre y Apellido")
        tree.heading("Atendido por", text="Atendido por")
        tree.heading("Observaciones", text="Observaciones")
        tree.heading("Fecha", text="Fecha de registro")
        tree.column("Id", width=60)
        tree.column("Nombre y Apellido", width=180)
        tree.column("Atendido por", width=180)
        tree.column("Observaciones", width=400)
        tree.column("Fecha", width=120)
        tree.pack(fill='both', expand=True)
        # Botón salir
        btn_salir = tk.Button(ventana, text='Salir', font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg='white', width=12, activebackground='#3A7DBA', command=ventana.destroy)
        btn_salir.pack(pady=10)
        # Llenar tabla
        historias = listarHistoria(id_cliente)
        for h in historias:
            if len(h) > 4:
                tree.insert('', 'end', values=(h[0], h[1], h[2], h[3], h[4]))
            else:
                tree.insert('', 'end', values=(h[0], h[1], h[2], h[3], h[4] if len(h) > 3 else ''))

    def mostrar_reportes(self):
        self.limpiar_central()
        # Crear un frame temporal para alojar la ventana de reportes
        frame_reportes = tk.Frame(self.central_frame, bg=COLOR_SECUNDARIO)
        frame_reportes.pack(fill='both', expand=True)
        # Instanciar el Frame de reportes clásico y mostrarlo en el panel central
        # Reutiliza la lógica de ventanaReportes de Frame
        try:
            frame_temp = Frame(frame_reportes)
            frame_temp.pack(fill='both', expand=True)
            frame_temp.ventanaReportes()
        except Exception as e:
            tk.Label(frame_reportes, text=f'Error al mostrar reportes: {e}', fg='red', bg=COLOR_SECUNDARIO).pack(pady=30)