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
class Frame (tk.Frame):
    def __init__(self, root):

        super().__init__(root,width=1280,height=720)
        self.root = root            #modificacion de codigo 
        self.config(bg='#CDD8FF') 
        self.pack()
        self.camposCliente()
        self.deshabilitar()
        self.tablaCliente()
        self.agregar_logo_empresa()  # Mostrar el logo al iniciar
        

    def camposCliente(self):
        self.lblId = tk.Label(self, text='Id: ')
        self.lblId.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblId.grid(column=0,row=0, padx=10, pady=5)

        self.lblNombre = tk.Label(self, text='Nombre: ')
        self.lblNombre.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblNombre.grid(column=0,row=1, padx=10, pady=5)

        self.lblApellido = tk.Label(self, text='Apellido: ')
        self.lblApellido.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblApellido.grid(column=0, row=2, padx=10, pady=5)

        self.lblDocumId= tk.Label(self, text='DocumId: ')
        self.lblDocumId.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblDocumId.grid(column=0, row=3, padx=10, pady=5)

        self.lblEmail = tk.Label(self, text='Email: ')
        self.lblEmail.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblEmail.grid(column=0, row=4, padx=10, pady=5)

        self.lblTelefono = tk.Label(self, text='Telefono: ')
        self.lblTelefono.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblTelefono.grid(column=0, row=5, padx=10, pady=5)

        self.lblNacionalidad = tk.Label(self, text='Nacionalidad: ')
        self.lblNacionalidad.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblNacionalidad.grid(column=0, row=6, padx=10, pady=5)

        self.lblResidencia = tk.Label(self, text='Residencia: ')
        self.lblResidencia.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblResidencia.grid(column=0, row=7, padx=10, pady=5)

        self.svResidencia = tk.StringVar()
        self.entryResidencia = tk.Entry(self, textvariable=self.svResidencia)
        self.entryResidencia.config(width=50, font=('ARIAL',15))
        self.entryResidencia.grid(column=1, row=7, padx=10, pady=5, columnspan=2)

        self.lblAsunto = tk.Label(self, text='Asunto: ')
        self.lblAsunto.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblAsunto.grid(column=0, row=8, padx=10, pady=5)

        self.lblEstatus = tk.Label(self, text='Estatus: ')
        self.lblEstatus.config (font=('ARIAL',15, 'bold'),bg='#CDD8FF' ) 
        self.lblEstatus.grid(column=0, row=9, padx=10, pady=5)

        #Entradas
        self.svId = tk.StringVar()
        self.entryId = tk.Entry(self, textvariable=self.svId)
        self.entryId.config(width=50, font=('ARIAL',15))
        self.entryId.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=50, font=('ARIAL',15))
        self.entryNombre.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svApellido = tk.StringVar()
        self.entryApellido = tk.Entry(self, textvariable=self.svApellido)
        self.entryApellido.config(width=50, font=('ARIAL',15))
        self.entryApellido.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svDocumId = tk.StringVar()
        self.entryDocumId = tk.Entry(self, textvariable=self.svDocumId)
        self.entryDocumId.config(width=50, font=('ARIAL',15))
        self.entryDocumId.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svEmail = tk.StringVar()
        self.entryEmail = tk.Entry(self, textvariable=self.svEmail)
        self.entryEmail.config(width=50, font=('ARIAL',15))
        self.entryEmail.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svTelefono = tk.StringVar()
        self.entryTelefono = tk.Entry(self, textvariable=self.svTelefono)
        self.entryTelefono.config(width=50, font=('ARIAL',15))
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
        self.btnNuevo.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', cursor='hand2', activebackground='#5B8DBD')
        self.btnNuevo.grid(row=11, column=0, padx=10, pady=10)

        self.btnGuardar = tk.Button(self, text='Guardar', command=self.guardarCliente)
        self.btnGuardar.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', cursor='hand2', activebackground='#5B8DBD')
        self.btnGuardar.grid(row=11, column=1, padx=10, pady=10)

        self.btnCancelar = tk.Button(self, text='Cancelar', command=self.deshabilitar)
        self.btnCancelar.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', cursor='hand2', activebackground='#5B8DBD')
        self.btnCancelar.grid(row=11, column=2, padx=10, pady=10)

        # --- BUSCADOR ---
        # LABEL BUSCADOR
        self.lblBuscardocumId = tk.Label(self, text='Buscar DocumId: ')
        self.lblBuscardocumId.config(font=('ARIAl',15,'bold'), bg='#CDD8FF')
        self.lblBuscardocumId.grid(column=3, row=0, padx=10, pady=5)

        self.lblBuscarApellido = tk.Label(self, text='Buscar Apellido: ')
        self.lblBuscarApellido.config(font=('ARIAl',15,'bold'), bg='#CDD8FF')
        self.lblBuscarApellido.grid(column=3, row=1, padx=10, pady=5)

          #ENTRYS BUSCADOR
        self.svBuscardocumId = tk.StringVar()
        self.entryBuscardocumId = tk.Entry(self, textvariable=self.svBuscardocumId)
        self.entryBuscardocumId.config(width=20, font=('ARIAL',15))
        self.entryBuscardocumId.grid(column=4, row=0, padx=10, pady=5, columnspan=2)

        self.svBuscarApellido = tk.StringVar()
        self.entryBuscarApellido = tk.Entry(self, textvariable=self.svBuscarApellido)
        self.entryBuscarApellido.config(width=20, font=('ARIAL',15))
        self.entryBuscarApellido.grid(column=4, row=1, padx=10, pady=5, columnspan=2)

         #BUTTON BUSCADOR
        self.btnBuscarCondicion = tk.Button(self, text='Buscar', command = self.buscarCondicion)
        self.btnBuscarCondicion.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', 
                                bg='#00396F', cursor='hand2',activebackground='#5B8DBD')
        self.btnBuscarCondicion.grid(column=3,row=2, padx=10, pady=5, columnspan=1)

        self.btnLimpiarBuscador = tk.Button(self, text='Limpiar', command = self.limpiarBuscador)
        self.btnLimpiarBuscador.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', 
                                bg="#00396F", cursor='hand2',activebackground='#5B8DBD')
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
        frame_filtros = tk.Frame(tab_fecha)
        frame_filtros.pack(fill='x', pady=10)
        Label(frame_filtros, text='Fecha Registrado (YYYY-MM-DD):', font=('Arial', 12)).pack(side='left', padx=5)
        entry_fecha = Entry(frame_filtros, font=('Arial', 12), width=15)
        entry_fecha.pack(side='left', padx=5)
        btn_buscar = Button(frame_filtros, text='Buscar', font=('Arial', 12), bg='#00396F', fg='#C5EAFE', activebackground='#5B8DBD')
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
        frame_export = tk.Frame(ventana)
        frame_export.pack(fill='x', pady=5)
        btn_descargar = Button(frame_export, text='Descargar Reporte', bg='#00396F', fg='#C5EAFE', command=lambda: mostrar_opciones_descarga())
        btn_descargar.pack(side='left', padx=5)

        def mostrar_opciones_descarga():
            top = Toplevel(ventana)
            top.title('Selecciona el formato de descarga')
            top.geometry('300x150')
            Label(top, text='Elige el formato:', font=('Arial', 12)).pack(pady=10)
            Button(top, text='PNG', width=15, command=lambda: [exportar_png(ventana), top.destroy()]).pack(pady=5)
            Button(top, text='CSV', width=15, command=lambda: [exportar_csv(), top.destroy()]).pack(pady=5)
            Button(top, text='Excel', width=15, command=lambda: [exportar_excel(), top.destroy()]).pack(pady=5)

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
        # Actualizar columnas: Id, Motivo, Tipo de Consulta, Detalle, Fecha
        tree = ttk.Treeview(ventana, columns=("Id", "Motivo", "Tipo de Consulta", "Detalle", "Fecha"), show="headings")
        tree.heading("Id", text="Id")
        tree.heading("Motivo", text="Motivo")
        tree.heading("Tipo de Consulta", text="Tipo de Consulta")
        tree.heading("Detalle", text="Detalle")
        tree.heading("Fecha", text="Fecha")
        tree.column("Id", width=60)
        tree.column("Motivo", width=150)
        tree.column("Tipo de Consulta", width=150)
        tree.column("Detalle", width=350)
        tree.column("Fecha", width=120)
        tree.pack(fill='both', expand=True)
        # --- BOTONES DE HISTORIAL ---
        frame_botones = tk.Frame(ventana, bg='#CDD8FF')
        frame_botones.pack(fill='x', pady=10)
        btn_agregar = tk.Button(frame_botones, text='Agregar Historia', width=18, font=('ARIAL',12,'bold'), fg='#C5EAFE', bg='#00396F', activebackground='#5B8DBD', cursor='hand2', command=lambda: self.agregarHistoria(id_cliente, tree, ventana))
        btn_agregar.pack(side='left', padx=10)
        btn_editar = tk.Button(frame_botones, text='Editar Historia', width=18, font=('ARIAL',12,'bold'), fg='#C5EAFE', bg='#00396F', activebackground='#5B8DBD', cursor='hand2', command=lambda: self.editarHistoria(tree, ventana))
        btn_editar.pack(side='left', padx=10)
        btn_eliminar = tk.Button(frame_botones, text='Eliminar Historia', width=18, font=('ARIAL',12,'bold'), fg='#C5EAFE', bg='#00396F', activebackground='#5B8DBD', cursor='hand2', command=lambda: self.eliminarHistoria(tree, ventana))
        btn_eliminar.pack(side='left', padx=10)
        btn_salir = tk.Button(frame_botones, text='Salir', width=18, font=('ARIAL',12,'bold'), fg='#C5EAFE', bg='#00396F', activebackground='#5B8DBD', cursor='hand2', command=ventana.destroy)
        btn_salir.pack(side='right', padx=10)
        # --- LLENAR TABLA DESPUÉS DE LOS BOTONES ---
        historias = listarHistoria(id_cliente)
        for h in historias:
            # h: (id, motivo, tipoConsulta, detalle, fecha)
            if len(h) > 5:
                tree.insert('', 'end', values=(h[0], h[2], h[3], h[4], h[5]))
            else:
                tree.insert('', 'end', values=(h[0], h[2], h[3], h[4], ''))

    def agregarHistoria(self, id_cliente, tree, ventana):
        def guardar():
            motivo = entry_motivo.get()
            tipo = entry_tipo.get()
            detalle = entry_detalle.get("1.0", "end").strip()
            fecha = entry_fecha.get() if hasattr(entry_fecha, 'get') else ''
            if not motivo or not tipo or not detalle or not fecha:
                from tkinter import messagebox
                messagebox.showwarning('Campos requeridos', 'Debe completar todos los campos.')
                return
            from model.historiaConsultaDao import guardarHistoria
            guardarHistoria(id_cliente, motivo, tipo, detalle, fecha)
            top.destroy()
            self.refrescar_historial(tree, id_cliente)
        from tkinter import Toplevel, Label, Entry, Text, Button
        try:
            from tkcalendar import DateEntry
        except ImportError:
            DateEntry = None
        top = Toplevel(ventana)
        top.title('Agregar Historia')
        top.geometry('500x420')
        Label(top, text='Motivo:', font=('Arial', 12)).pack(pady=5)
        entry_motivo = Entry(top, font=('Arial', 12))
        entry_motivo.pack(pady=5, fill='x', padx=20)
        Label(top, text='Tipo de Consulta:', font=('Arial', 12)).pack(pady=5)
        entry_tipo = Entry(top, font=('Arial', 12))
        entry_tipo.pack(pady=5, fill='x', padx=20)
        Label(top, text='Detalle:', font=('Arial', 12)).pack(pady=5)
        entry_detalle = Text(top, font=('Arial', 12), height=5)
        entry_detalle.pack(pady=5, fill='x', padx=20)
        Label(top, text='Fecha:', font=('Arial', 12)).pack(pady=5)
        if DateEntry:
            entry_fecha = DateEntry(top, font=('Arial', 12), date_pattern='yyyy-mm-dd')
        else:
            entry_fecha = Entry(top, font=('Arial', 12))
        entry_fecha.pack(pady=5, fill='x', padx=20)
        Button(top, text='Guardar', command=guardar, bg='#00396F', fg='#C5EAFE', activebackground='#5B8DBD').pack(pady=15)

    def editarHistoria(self, tree, ventana):
        seleccionado = tree.focus()
        if not seleccionado:
            from tkinter import messagebox
            messagebox.showwarning('Editar Historia', 'Seleccione una historia de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        id_historia = valores[0]
        # Usar los valores directamente de la fila seleccionada
        motivo_actual = valores[1] if len(valores) > 1 else ''
        tipo_actual = valores[2] if len(valores) > 2 else ''
        detalle_actual = valores[3] if len(valores) > 3 else ''
        fecha_actual = valores[4] if len(valores) > 4 else ''
        def guardar():
            motivo = entry_motivo.get()
            tipo = entry_tipo.get()
            detalle = entry_detalle.get("1.0", "end").strip()
            fecha = entry_fecha.get() if hasattr(entry_fecha, 'get') else ''
            if not motivo or not tipo or not detalle or not fecha:
                from tkinter import messagebox
                messagebox.showwarning('Campos requeridos', 'Debe completar todos los campos.')
                return
            from model.historiaConsultaDao import editarHistoria
            editarHistoria(motivo, tipo, detalle, fecha, id_historia)
            top.destroy()
            id_cliente = self.obtener_id_cliente_de_historial(tree)
            self.refrescar_historial(tree, id_cliente)
        from tkinter import Toplevel, Label, Entry, Text, Button
        try:
            from tkcalendar import DateEntry
        except ImportError:
            DateEntry = None
        top = Toplevel(ventana)
        top.title('Editar Historia')
        top.geometry('500x420')
        Label(top, text='Motivo:', font=('Arial', 12)).pack(pady=5)
        entry_motivo = Entry(top, font=('Arial', 12))
        entry_motivo.insert(0, motivo_actual)
        entry_motivo.pack(pady=5, fill='x', padx=20)
        Label(top, text='Tipo de Consulta:', font=('Arial', 12)).pack(pady=5)
        entry_tipo = Entry(top, font=('Arial', 12))
        entry_tipo.insert(0, tipo_actual)
        entry_tipo.pack(pady=5, fill='x', padx=20)
        Label(top, text='Detalle:', font=('Arial', 12)).pack(pady=5)
        entry_detalle = Text(top, font=('Arial', 12), height=5)
        entry_detalle.insert('1.0', detalle_actual)
        entry_detalle.pack(pady=5, fill='x', padx=20)
        Label(top, text='Fecha:', font=('Arial', 12)).pack(pady=5)
        if DateEntry:
            entry_fecha = DateEntry(top, font=('Arial', 12), date_pattern='yyyy-mm-dd')
            if fecha_actual:
                try:
                    entry_fecha.set_date(fecha_actual)
                except Exception:
                    entry_fecha.set_date('today')
        else:
            entry_fecha = Entry(top, font=('Arial', 12))
            entry_fecha.insert(0, fecha_actual)
        entry_fecha.pack(pady=5, fill='x', padx=20)
        Button(top, text='Guardar', command=guardar, bg='#00396F', fg='#C5EAFE', activebackground='#5B8DBD').pack(pady=15)

    def eliminarHistoria(self, tree, ventana):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning('Eliminar Historia', 'Seleccione una historia de la tabla.')
            return
        valores = tree.item(seleccionado, 'values')
        id_historia = valores[0]
        if messagebox.askyesno('Eliminar Historia', '¿Está seguro de eliminar esta historia?'):
            from model.historiaConsultaDao import eliminarHistoria
            eliminarHistoria(id_historia)
            # Buscar el id_cliente del historial mostrado
            id_cliente = self.obtener_id_cliente_de_historial(tree)
            self.refrescar_historial(tree, id_cliente)

    def refrescar_historial(self, tree, id_cliente):
        # Refresca la tabla de historial tras agregar/editar/eliminar
        for item in tree.get_children():
            tree.delete(item)
        historias = listarHistoria(id_cliente)
        for h in historias:
            # h: (id, motivo, tipoConsulta, detalle, fecha)
            if len(h) > 5:
                tree.insert('', 'end', values=(h[0], h[2], h[3], h[4], h[5]))
            else:
                tree.insert('', 'end', values=(h[0], h[2], h[3], h[4], ''))

    def obtener_id_cliente_de_historial(self, tree):
        # Busca el id_cliente a partir del primer registro mostrado (asume que todos son del mismo cliente)
        items = tree.get_children()
        if items:
            id_historia = tree.item(items[0], 'values')[0]
            from model.historiaConsultaDao import listarHistoria
            # Buscar el id_cliente a partir de la historia (opcional: podrías guardar el id_cliente en la ventana)
            # Aquí simplemente retornamos el id_cliente usado en la última consulta
            # Si no hay historias, retorna None
            historias = listarHistoria(id_historia)
            if historias:
                return id_historia  # O ajusta según tu modelo
        return None

    def agregar_logo_empresa(self):
        # Cargar y mostrar el logo en la parte vacía inferior derecha de la ventana principal
        try:
            from PIL import Image, ImageTk
            logo_path = 'logo_empresa.png'  # Cambia el nombre si tu logo tiene otro nombre
            img = Image.open(logo_path)
            img = img.resize((300, 300), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            # Coloca el logo en la parte inferior derecha, ajusta x/y según tu layout
            self.lblLogo = tk.Label(self, image=self.logo_img, bg='#CDD8FF')
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
        for col in columnas:
            self.treeClientes.heading(col, text=col)
            self.treeClientes.column(col, width=120)
        self.treeClientes.grid(row=13, column=0, columnspan=6, padx=10, pady=10)

        # --- LLENAR TABLA CON DATOS ---
        from model.clienteDao import listar, listarCondicion
        if where:
            clientes = listarCondicion(where)
        else:
            clientes = listar()
        for c in clientes:
            self.treeClientes.insert('', 'end', values=(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]))

        # --- BOTONES SECUNDARIOS (debajo de la tabla) ---
        self.btnEditar = tk.Button(self, text='Editar Cliente', command=self.editarCliente)
        self.btnEditar.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', cursor='hand2', activebackground='#5B8DBD')
        self.btnEditar.grid(row=15, column=0, padx=10, pady=15)

        self.btnEliminar = tk.Button(self, text='Eliminar Cliente', command=self.eliminarCliente)
        self.btnEliminar.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', cursor='hand2', activebackground='#5B8DBD')
        self.btnEliminar.grid(row=15, column=1, padx=10, pady=15)

        self.btnHistoria = tk.Button(self, text='Historia Cliente', command=self.abrirHistoriaCliente)
        self.btnHistoria.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', cursor='hand2', activebackground='#5B8DBD')
        self.btnHistoria.grid(row=15, column=2, padx=10, pady=15)

        self.btnReportes = tk.Button(self, text='Reportes', command=self.ventanaReportes)
        self.btnReportes.config(width=15, font=('ARIAL',12,'bold'), fg='#C5EAFE', bg='#00396F', activebackground='#5B8DBD', cursor='hand2')
        self.btnReportes.grid(row=15, column=3, padx=10, pady=15)

        self.btnSalir = tk.Button(self, text='Salir', command=self.salir)
        self.btnSalir.config(width=15, font=('ARIAL',12, 'bold'), fg='#C5EAFE', bg='#00396F', activebackground='#5B8DBD', cursor='hand2')
        self.btnSalir.grid(row=15, column=4, padx=10, pady=15)
