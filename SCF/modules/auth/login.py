import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from database import get_db_connection

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        
        self.title("SCF - Sistema de Control Financiero")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        # Título
        self.label = ctk.CTkLabel(
            self.frame, 
            text="Inicio de Sesión",
            font=("Arial", 20, "bold")
        )
        self.label.pack(pady=12, padx=10)
        
        # Campo de usuario
        self.username_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Usuario",
            width=220
        )
        self.username_entry.pack(pady=6, padx=10)
        
        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(
            self.frame, 
            placeholder_text="Contraseña",
            show="*",
            width=220
        )
        self.password_entry.pack(pady=6, padx=10)
        
        # Botón de login
        self.login_button = ctk.CTkButton(
            self.frame, 
            text="Ingresar", 
            command=self._authenticate,
            width=220
        )
        self.login_button.pack(pady=12, padx=10)
        
        # Configurar tecla Enter para login
        self.bind('<Return>', lambda event: self._authenticate())
        
    def _authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son requeridos")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self.destroy()
                self.on_login_success({
                    "id": user[0],
                    "username": user[1],
                    "role": user[3],
                    "unit": user[4],
                    "specialty": user[5]
                })
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")