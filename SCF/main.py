import customtkinter as ctk
ctk.set_appearance_mode("System")
from modules.auth.login import LoginWindow
from modules.auth.users import create_default_admin

class SCFApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SCF - Sistema de Control Financiero")
        self.geometry("1024x768")
        self.minsize(800, 600)
        
        # Configuración de tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Crear admin por defecto si no existe
        create_default_admin()
        
        # Mostrar ventana de login
        self.show_login()
        
    def show_login(self):
        LoginWindow(self, self.on_login_success)
        
    def on_login_success(self, user_data):
        self.user_data = user_data
        self._setup_main_ui()
        
    def _setup_main_ui(self):
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()
            
        # Configurar grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Panel lateral (menú)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Logo o título
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="SCF 1.00", 
            font=("Arial", 20, "bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Información de usuario
        self.user_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=f"Usuario: {self.user_data['username']}\nUnidad: {self.user_data.get('unit', 'N/A')}",
            font=("Arial", 12)
        )
        self.user_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Botones del menú principal
        self.processes_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Procesos", 
            command=self.show_processes_menu
        )
        self.processes_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.config_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Configuración", 
            command=self.show_config_menu
        )
        self.config_btn.grid(row=3, column=0, padx=20, pady=10)
        
        # Botón de cerrar sesión
        self.logout_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Cerrar Sesión", 
            command=self.logout,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE")
        )
        self.logout_btn.grid(row=5, column=0, padx=20, pady=20)
        
        # Frame principal para contenido
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Mostrar dashboard inicial
        self.show_dashboard()
        
    def show_dashboard(self):
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Contenido del dashboard
        label = ctk.CTkLabel(
            self.main_frame, 
            text="Bienvenido al Sistema de Control Financiero\n\nSeleccione una opción del menú lateral",
            font=("Arial", 16)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
        
    def show_processes_menu(self):
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Menú de Procesos",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Botones de procesos
        buttons = [
            ("Gestionar Presupuesto", self.show_budget_menu),
            ("Gestionar Recursos Financieros", self.show_finances_menu),
            ("Gestionar Informes", self.show_reports_menu),
            ("Gestionar Cierre Contable", self.show_accounting_menu),
            ("Gestionar Contratos Económicos", self.show_contracts_menu)
        ]
        
        for i, (text, command) in enumerate(buttons, start=1):
            btn = ctk.CTkButton(
                self.main_frame,
                text=text,
                command=command,
                width=300,
                height=40,
                corner_radius=6
            )
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="w")
            
    def show_config_menu(self):
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Menú de Configuración",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Botones de configuración
        buttons = [
            ("Parámetros", self.show_parameters),
            ("Seguridad", self.show_security)
        ]
        
        for i, (text, command) in enumerate(buttons, start=1):
            btn = ctk.CTkButton(
                self.main_frame,
                text=text,
                command=command,
                width=300,
                height=40,
                corner_radius=6
            )
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="w")
            
    def show_budget_menu(self):
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Gestión de Presupuesto",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Botón de regreso
        back_btn = ctk.CTkButton(
            self.main_frame,
            text="← Volver",
            command=self.show_processes_menu,
            width=100,
            height=30,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE")
        )
        back_btn.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        
        # Botones de gestión de presupuesto
        buttons = [
            ("Presupuesto Aprobado (SCF-72)", self.show_scf72_form),
            ("Presupuesto Desagregado y Ejecutado (SCF-73)", self.show_scf73_form)
        ]
        
        for i, (text, command) in enumerate(buttons, start=1):
            btn = ctk.CTkButton(
                self.main_frame,
                text=text,
                command=command,
                width=400,
                height=45,
                corner_radius=6
            )
            btn.grid(row=i, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
    
    def show_scf72_form(self):
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Presupuesto Aprobado (SCF-72)",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Botón de regreso
        back_btn = ctk.CTkButton(
            self.main_frame,
            text="← Volver",
            command=self.show_budget_menu,
            width=100,
            height=30,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE")
        )
        back_btn.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        
        # Configurar grid del formulario
        for i in range(6):
            form_frame.grid_rowconfigure(i, weight=1)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)
        
        # Campos del formulario SCF-72
        fields = [
            ("Unidad Militar:", self.user_data.get('unit', '')),
            ("Especialidad:", self.user_data.get('specialty', '')),
            ("Fecha (D M A):", ""),
            ("Detalles:", ""),
            ("Presupuesto Aprobado:", ""),
            ("Partida Directiva 110101:", ""),
            ("Partida Directiva 110406:", ""),
            ("Partida Directiva 800000:", "")
        ]
        
        # Crear etiquetas y campos de entrada
        self.scf72_entries = {}
        for i, (label, default_value) in enumerate(fields):
            # Etiqueta
            lbl = ctk.CTkLabel(form_frame, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            # Campo de entrada
            if label == "Detalles:":
                entry = ctk.CTkTextbox(form_frame, height=60)
                entry.insert("1.0", default_value)
            else:
                entry = ctk.CTkEntry(form_frame)
                entry.insert(0, default_value)
            
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.scf72_entries[label.replace(":", "").strip().lower().replace(" ", "_")] = entry
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        
        buttons = [
            ("Guardar", self.save_scf72),
            ("Exportar PDF", self.export_scf72_pdf),
            ("Limpiar", self.clear_scf72_form)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=command
            )
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            
    def show_scf72_records(self, filters=None):
        """Muestra una ventana con los registros existentes de SCF-72"""
        from modules.processes.budget import get_approved_budgets
        from modules.processes.filter_dialog import FilterDialog
        
        try:
            # Configuración de filtros
            filter_fields = {
                'text_fields': [
                    {'name': 'military_unit', 'label': 'Unidad Militar'},
                    {'name': 'specialty', 'label': 'Especialidad'}
                ],
                'date_fields': [
                    {'name': 'date_from', 'label': 'Fecha desde'},
                    {'name': 'date_to', 'label': 'Fecha hasta'}
                ],
                'range_fields': [
                    {'name': 'amount', 'label': 'Monto Presupuesto'}
                ],
                'checkboxes': [
                    {'name': '110101', 'label': '110101'},
                    {'name': '110406', 'label': '110406'},
                    {'name': '800000', 'label': '800000'}
                ],
                'sort_fields': [
                    {'value': 'date', 'label': 'Fecha'},
                    {'value': 'approved_budget', 'label': 'Monto'},
                    {'value': 'military_unit', 'label': 'Unidad'}
                ]
            }
            
            # Crear ventana principal de registros
            records_window = ctk.CTkToplevel(self)
            records_window.title("Registros de Presupuesto Aprobado (SCF-72)")
            records_window.geometry("1200x700")
            
            # Barra de herramientas
            toolbar = ctk.CTkFrame(records_window)
            toolbar.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkButton(
                toolbar, 
                text="Filtrar", 
                command=lambda: self._open_filter_dialog(
                    records_window, filter_fields, filters, 
                    lambda f: self.show_scf72_records(f)
                ),
                width=100
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                toolbar, 
                text="Exportar a Excel", 
                command=self._export_to_excel,
                width=120
            ).pack(side="left", padx=5)
            
            # Treeview para mostrar los registros
            tree_frame = ctk.CTkFrame(records_window)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Configurar el Treeview
            tree = ttk.Treeview(tree_frame)
            tree["columns"] = ("id", "date", "unit", "specialty", "details", 
                             "approved", "110101", "110406", "800000", "user", "created")
            
            # Configurar columnas
            columns = [
                ("id", "ID", 50),
                ("date", "Fecha", 100),
                ("unit", "Unidad", 120),
                ("specialty", "Especialidad", 100),
                ("details", "Detalles", 250),
                ("approved", "Presupuesto", 100),
                ("110101", "110101", 80),
                ("110406", "110406", 80),
                ("800000", "800000", 80),
                ("user", "Usuario", 100),
                ("created", "Creado", 120)
            ]
            
            for col_id, col_text, col_width in columns:
                tree.column(col_id, width=col_width, anchor="center" if col_id != "details" else "w")
                tree.heading(col_id, text=col_text)
            
            # Scrollbars
            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Grid layout
            tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")
            
            # Configurar el grid para expandirse
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            # Obtener y mostrar registros
            records = get_approved_budgets(filters)
            for record in records:
                tree.insert("", "end", values=(
                    record['id'],
                    record['date'],
                    record['military_unit'],
                    record['specialty'],
                    record['details'],
                    f"{record['approved_budget']:,.2f}",
                    f"{record['item_110101']:,.2f}",
                    f"{record['item_110406']:,.2f}",
                    f"{record['item_800000']:,.2f}",
                    record['created_by'],
                    record['created_at']
                ))
            
            # Mostrar contador de registros
            count_label = ctk.CTkLabel(
                records_window, 
                text=f"Total de registros: {len(records)}"
            )
            count_label.pack(side="left", padx=10, pady=5, anchor="w")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los registros: {str(e)}")
    
    def _open_filter_dialog(self, parent, filter_fields, current_filters, callback):
        def on_dialog_close():
            filters = dialog.result
            parent.destroy()
            if filters is not None:
                callback(filters)
        
        dialog = FilterDialog(parent, filter_fields, current_filters)
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        dialog.wait_window()
            
    def save_scf72(self):
        try:
            from modules.processes.budget import save_approved_budget
            
            data = {
                'unidad_militar': self.scf72_entries['unidad_militar'].get(),
                'especialidad': self.scf72_entries['especialidad'].get(),
                'fecha_d_m_a': self.scf72_entries['fecha_d_m_a'].get(),
                'detalles': self.scf72_entries['detalles'].get("1.0", "end-1c"),
                'presupuesto_aprobado': self.scf72_entries['presupuesto_aprobado'].get(),
                'partida_directiva_110101': self.scf72_entries['partida_directiva_110101'].get(),
                'partida_directiva_110406': self.scf72_entries['partida_directiva_110406'].get(),
                'partida_directiva_800000': self.scf72_entries['partida_directiva_800000'].get()
            }
            
            # Validar campos numéricos
            try:
                float(data['presupuesto_aprobado'])
                float(data['partida_directiva_110101'])
                float(data['partida_directiva_110406'])
                float(data['partida_directiva_800000'])
            except ValueError:
                messagebox.showerror("Error", "Los valores de presupuesto deben ser numéricos")
                return
                
            record_id = save_approved_budget(data, self.user_data['username'])
            messagebox.showinfo("Éxito", f"Registro guardado con ID: {record_id}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def export_scf72_pdf(self):
        from templates.SCF_72 import SCF72PDF
        
        data = {key: entry.get("1.0", "end-1c") if isinstance(entry, ctk.CTkTextbox) else entry.get() 
               for key, entry in self.scf72_entries.items()}
        
        # Validar datos
        if not all(data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios para exportar")
            return
            
        try:
            pdf = SCF72PDF()
            pdf = pdf.create_pdf(data)
            
            # Guardar el PDF
            filename = f"SCF-72_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            
            messagebox.showinfo("Éxito", f"PDF exportado como {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    def clear_scf72_form(self):
        for entry in self.scf72_entries.values():
            if isinstance(entry, ctk.CTkTextbox):
                entry.delete("1.0", "end")
            else:
                entry.delete(0, "end")
                
    def show_scf73_form(self):
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Presupuesto Desagregado y Ejecutado (SCF-73)",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Botón de regreso
        back_btn = ctk.CTkButton(
            self.main_frame,
            text="← Volver",
            command=self.show_budget_menu,
            width=100,
            height=30,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE")
        )
        back_btn.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        
        # Configurar grid del formulario (6 filas, 2 columnas)
        for i in range(8):
            form_frame.grid_rowconfigure(i, weight=1)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)
        
        # Campos del formulario SCF-73
        fields = [
            ("Unidad Militar:", self.user_data.get('unit', '')),
            ("Especialidad:", self.user_data.get('specialty', '')),
            ("Partida Directiva:", "800000"),  # Valor por defecto como ejemplo
            ("Fecha (D M A):", ""),
            ("Detalles:", ""),
            ("Presupuesto Aprobado:", ""),
            ("Ejecución Partida 800440:", ""),
            ("Ejecución Partida 890441:", ""),
            ("Concepto de Gastos:", "corriente")  # Valor por defecto
        ]
        
        # Crear etiquetas y campos de entrada
        self.scf73_entries = {}
        for i, (label, default_value) in enumerate(fields):
            # Etiqueta
            lbl = ctk.CTkLabel(form_frame, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            # Campo de entrada
            if label == "Detalles:":
                entry = ctk.CTkTextbox(form_frame, height=60)
                entry.insert("1.0", default_value)
            elif label == "Concepto de Gastos:":
                entry = ctk.CTkComboBox(form_frame, values=["corriente", "capital"])
                entry.set(default_value)
            else:
                entry = ctk.CTkEntry(form_frame)
                entry.insert(0, default_value)
            
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            field_name = label.replace(":", "").strip().lower().replace(" ", "_")
            self.scf73_entries[field_name] = entry
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        
        buttons = [
            ("Guardar", self.save_scf73),
            ("Exportar PDF", self.export_scf73_pdf),
            ("Calcular", self.calculate_scf73),
            ("Limpiar", self.clear_scf73_form)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=command
            )
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
    
    def save_scf73(self):
        try:
            from modules.processes.budget import save_budget_execution
            
            data = {
                'unidad_militar': self.scf73_entries['unidad_militar'].get(),
                'especialidad': self.scf73_entries['especialidad'].get(),
                'partida_directiva': self.scf73_entries['partida_directiva'].get(),
                'fecha_d_m_a': self.scf73_entries['fecha_d_m_a'].get(),
                'detalles': self.scf73_entries['detalles'].get("1.0", "end-1c"),
                'presupuesto_aprobado': self.scf73_entries['presupuesto_aprobado'].get(),
                'ejecución_partida_800440': self.scf73_entries['ejecución_partida_800440'].get() or "0",
                'ejecución_partida_890441': self.scf73_entries['ejecución_partida_890441'].get() or "0",
                'concepto_de_gastos': self.scf73_entries['concepto_de_gastos'].get()
            }
            
            # Validar campos numéricos
            try:
                float(data['presupuesto_aprobado'])
                float(data['ejecución_partida_800440'])
                float(data['ejecución_partida_890441'])
            except ValueError:
                messagebox.showerror("Error", "Los valores de presupuesto deben ser numéricos")
                return
                
            record_id = save_budget_execution(data, self.user_data['username'])
            messagebox.showinfo("Éxito", f"Registro guardado con ID: {record_id}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def calculate_scf73(self, silent=False):
        try:
            # Obtener valores numéricos
            presupuesto = float(self.scf73_entries['presupuesto_aprobado'].get())
            ejecucion_800440 = float(self.scf73_entries['ejecución_partida_800440'].get() or 0)
            ejecucion_890441 = float(self.scf73_entries['ejecución_partida_890441'].get() or 0)
            
            # Calcular valores
            saldo = presupuesto - (ejecucion_800440 + ejecucion_890441)
            porcentaje = ((ejecucion_800440 + ejecucion_890441) / presupuesto) * 100 if presupuesto != 0 else 0
            
            # Mostrar resultados (podríamos añadir campos de solo lectura para mostrar estos valores)
            messagebox.showinfo("Cálculo", 
                f"Saldo: {saldo:.2f}\n% Ejecutado: {porcentaje:.2f}%")
                
            return saldo, porcentaje
        except ValueError as e:
            if not silent:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos")
            return None, None
    
    def export_scf73_pdf(self):
        from templates.SCF_73 import SCF73PDF
        
        data = {key: entry.get("1.0", "end-1c") if isinstance(entry, ctk.CTkTextbox) else entry.get() 
               for key, entry in self.scf73_entries.items()}
        
        # Calcular saldo y porcentaje
        saldo, porcentaje = self.calculate_scf73(silent=True)
        data['saldo'] = f"{saldo:.2f}" if saldo is not None else "0.00"
        data['porcentaje_ejecutado'] = f"{porcentaje:.2f}%" if porcentaje is not None else "0.00%"
        
        # Validar datos
        required_fields = ['unidad_militar', 'especialidad', 'partida_directiva', 
                          'fecha_d_m_a', 'detalles', 'presupuesto_aprobado']
        
        if not all(data[field] for field in required_fields):
            messagebox.showerror("Error", "Los campos marcados con * son obligatorios para exportar")
            return
            
        try:
            pdf = SCF73PDF()
            pdf = pdf.create_pdf(data)
            
            # Guardar el PDF
            filename = f"SCF-73_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            
            messagebox.showinfo("Éxito", f"PDF exportado como {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    def clear_scf73_form(self):
        for entry in self.scf73_entries.values():
            if isinstance(entry, ctk.CTkTextbox):
                entry.delete("1.0", "end")
            elif isinstance(entry, ctk.CTkComboBox):
                entry.set("corriente")
            else:
                entry.delete(0, "end")    
    def show_finances_menu(self):
        # Implementar submenú de recursos financieros
        pass
        
    def show_reports_menu(self):
        # Implementar submenú de informes
        pass
        
    def show_accounting_menu(self):
        # Implementar submenú de cierre contable
        pass
        
    def show_contracts_menu(self):
        # Implementar submenú de contratos
        pass
        
    def show_parameters(self):
        # Implementar configuración de parámetros
        pass
        
    def show_security(self):
        # Implementar configuración de seguridad
        pass
        
    def logout(self):
        # Limpiar datos de usuario y volver a login
        self.user_data = None
        for widget in self.winfo_children():
            widget.destroy()
        self.show_login()
    
    def _export_to_excel(self, records):
        try:
            from pandas import DataFrame
            import os
            
            # Convertir registros a DataFrame
            df = DataFrame([dict(record) for record in records])
            
            # Seleccionar y ordenar columnas
            columns = ['date', 'military_unit', 'specialty', 'approved_budget',
                     'item_110101', 'item_110406', 'item_800000', 'created_by']
            df = df[columns]
            
            # Renombrar columnas
            df.columns = ['Fecha', 'Unidad Militar', 'Especialidad', 'Presupuesto Aprobado',
                        'Partida 110101', 'Partida 110406', 'Partida 800000', 'Usuario']
            
            # Generar nombre de archivo
            filename = f"SCF72_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Guardar como Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            
            # Abrir el archivo
            os.startfile(filename)
            messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
if __name__ == "__main__":
    app = SCFApp()
    app.mainloop()