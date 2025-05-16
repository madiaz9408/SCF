import customtkinter as ctk
from tkinter import ttk
from datetime import datetime

class FilterDialog(ctk.CTkToplevel):
    def __init__(self, parent, filter_fields, current_filters=None):
        super().__init__(parent)
        self.title("Filtros Avanzados")
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.filter_fields = filter_fields
        self.result = None
        self.current_filters = current_filters or {}
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Campos de filtro
        self.entries = {}
        row = 0
        
        # Filtros por texto
        if 'text_fields' in self.filter_fields:
            for field in self.filter_fields['text_fields']:
                lbl = ctk.CTkLabel(self.frame, text=field['label'])
                lbl.grid(row=row, column=0, padx=5, pady=5, sticky="w")
                
                entry = ctk.CTkEntry(self.frame)
                entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
                
                if field['name'] in self.current_filters:
                    entry.insert(0, self.current_filters[field['name'])
                
                self.entries[field['name']] = entry
                row += 1
        
        # Filtros por fechas
        if 'date_fields' in self.filter_fields:
            for field in self.filter_fields['date_fields']:
                lbl = ctk.CTkLabel(self.frame, text=field['label'])
                lbl.grid(row=row, column=0, padx=5, pady=5, sticky="w")
                
                entry = ctk.CTkEntry(self.frame, placeholder_text="DD-MM-AAAA")
                entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
                
                if field['name'] in self.current_filters:
                    entry.insert(0, self.current_filters[field['name']])
                
                self.entries[field['name']] = entry
                row += 1
        
        # Filtros por rango numérico
        if 'range_fields' in self.filter_fields:
            for field in self.filter_fields['range_fields']:
                lbl = ctk.CTkLabel(self.frame, text=field['label'])
                lbl.grid(row=row, column=0, padx=5, pady=5, sticky="w")
                
                min_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
                min_frame.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
                
                ctk.CTkLabel(min_frame, text="Mín:").pack(side="left")
                min_entry = ctk.CTkEntry(min_frame, width=80)
                min_entry.pack(side="left", padx=5)
                
                ctk.CTkLabel(min_frame, text="Máx:").pack(side="left")
                max_entry = ctk.CTkEntry(min_frame, width=80)
                max_entry.pack(side="left", padx=5)
                
                if f"min_{field['name']}" in self.current_filters:
                    min_entry.insert(0, self.current_filters[f"min_{field['name']}"])
                if f"max_{field['name']}" in self.current_filters:
                    max_entry.insert(0, self.current_filters[f"max_{field['name']}"])
                
                self.entries[f"min_{field['name']}"] = min_entry
                self.entries[f"max_{field['name']}"] = max_entry
                row += 1
        
        # Filtros por checkboxes (partidas)
        if 'checkboxes' in self.filter_fields:
            ctk.CTkLabel(self.frame, text="Filtrar por partidas:").grid(
                row=row, column=0, padx=5, pady=10, sticky="w")
            row += 1
            
            checks_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
            checks_frame.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            
            self.check_vars = {}
            for i, item in enumerate(self.filter_fields['checkboxes']):
                var = ctk.BooleanVar(value=item['name'] in self.current_filters.get('items', {}))
                cb = ctk.CTkCheckBox(checks_frame, text=item['label'], variable=var)
                cb.pack(side="left", padx=10)
                self.check_vars[item['name']] = var
            row += 1
        
        # Ordenamiento
        ctk.CTkLabel(self.frame, text="Ordenar por:").grid(
            row=row, column=0, padx=5, pady=10, sticky="w")
        row += 1
        
        sort_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        sort_frame.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Campo para ordenar
        self.sort_field = ctk.CTkComboBox(
            sort_frame, 
            values=[f['value'] for f in self.filter_fields['sort_fields']],
            width=120
        )
        self.sort_field.pack(side="left", padx=5)
        self.sort_field.set(self.current_filters.get('sort_field', 'date'))
        
        # Dirección del orden
        self.sort_order = ctk.CTkComboBox(
            sort_frame, 
            values=["ASC", "DESC"],
            width=80
        )
        self.sort_order.pack(side="left", padx=5)
        self.sort_order.set(self.current_filters.get('sort_order', 'DESC'))
        row += 1
        
        # Botones
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(
            btn_frame, 
            text="Aplicar Filtros", 
            command=self._apply_filters,
            width=120
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="Limpiar Filtros", 
            command=self._clear_filters,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE"),
            width=120
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cancelar", 
            command=self._cancel,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE"),
            width=120
        ).pack(side="left", padx=10)
    
    def _apply_filters(self):
        filters = {}
        
        # Text fields
        for field in self.filter_fields.get('text_fields', []):
            value = self.entries[field['name']].get()
            if value:
                filters[field['name']] = value
        
        # Date fields
        for field in self.filter_fields.get('date_fields', []):
            value = self.entries[field['name']].get()
            if value:
                try:
                    datetime.strptime(value, "%d-%m-%Y")
                    filters[field['name']] = value
                except ValueError:
                    pass
        
        # Range fields
        for field in self.filter_fields.get('range_fields', []):
            min_val = self.entries[f"min_{field['name']}"].get()
            max_val = self.entries[f"max_{field['name']}"].get()
            
            if min_val:
                try:
                    filters[f"min_{field['name']}"] = float(min_val)
                except ValueError:
                    pass
            if max_val:
                try:
                    filters[f"max_{field['name']}"] = float(max_val)
                except ValueError:
                    pass
        
        # Checkboxes
        if 'checkboxes' in self.filter_fields:
            items = {}
            for item in self.filter_fields['checkboxes']:
                if self.check_vars[item['name']].get():
                    items[item['name']] = True
            if items:
                filters['items'] = items
        
        # Sorting
        filters['sort_field'] = self.sort_field.get()
        filters['sort_order'] = self.sort_order.get()
        
        self.result = filters
        self.destroy()
    
    def _clear_filters(self):
        self.result = {}
        self.destroy()
    
    def _cancel(self):
        self.destroy()