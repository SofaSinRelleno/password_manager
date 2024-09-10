import tkinter as tk
from tkinter import messagebox
from password_manager import PasswordManager


class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de contraseñas")
        self.root.geometry("400x300")

        #Instanciamos PasswordManager
        self.manager = PasswordManager()
        
        #Variable de clave maestra.
        self.master_password_var = tk.StringVar()
        
        #Ventana para ingresar la contraseña maestra
        
        self.create_master_password_window()
        
        
    def create_master_password_window(self):
        self.master_password_window = tk.Toplevel(self.root)
        self.master_password_window.title("Clave maestra")
        self.master_password_window.geometry("300x150")
        
        tk.Label(self.master_password_window, text="Ingrese su clave maestra: ").pack(pady=10)
        tk.Entry(self.master_password_window, textvariable=self.master_password_var, show="*").pack(pady=10)
        tk.Button(self.master_password_window, text="Verificar", command=self.verify_master_password).pack(pady=10)
        
        self.attempts = 0
        
    def verify_master_password(self):
        password = self.master_password_var.get()
            
        if self.manager.verifyPassword(password):
            messagebox.showinfo("Exito", "Contraseña correcta. Acceso concedido.")
            self.master_password_window.destroy()
            self.create_main_window()
        else:
            self.attempts += 1
            messagebox.showerror("Error", f"Contraseña incorrecta. Intento {self.attempts}/5.")
            if self.attempts >= 5:
                messagebox.showerror("Error", "Numero maximo de intentos alcanzados. Cerrando programa.")
                self.root.quit()
                    
    def create_main_window(self):
        #Creamos el menu principal con todas las opciones del gestor de contraseñas.
        tk.Label(self.root, text="Bienvenido al gestor de contraseñas").pack(pady=10)
            
        tk.Button(self.root, text="Agregar contraseña", command=self.add_password_window).pack(pady=5)
        tk.Button(self.root, text="Ver contraseñas", command=self.view_passwords).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)
            
    def add_password_window(self):
        #Creamos una ventana para agregar contraseñas
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar contraseña")
        add_window.geometry("300x200")
            
        service_var = tk.StringVar()
        username_var = tk.StringVar()
        password_var = tk.StringVar()
            
        tk.Label(add_window, text="Servicio: ").pack(pady=5)
        tk.Entry(add_window, textvariable=service_var).pack(pady=5)
            
        tk.Label(add_window, text="Nombre de usuario: ").pack(pady=5)
        tk.Entry(add_window, textvariable=username_var).pack(pady=5)
            
        tk.Label(add_window, text="Contraseña: ").pack(pady=5)
        tk.Entry(add_window, textvariable=password_var, show="*").pack(pady=5)
            
        tk.Button(add_window, text= "Guardar", command=lambda: self.save_password(service_var, username_var, password_var, add_window)).pack(pady=10)
            
    def save_password(self, service_var, username_var, password_var, window):
        service = service_var.get()
        username = username_var.get()
        password = password_var.get()
            
        if service and username and password:
            self.manager.add_password(service, username, password)
            messagebox.showinfo("Exito", "Contraseña guardada correctamente.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
                
        
    def view_passwords(self):
        #Ventana para ver las contraseñas guardadas
        view_window = tk.Toplevel(self.root)
        view_window.title("Ver contraseñas")
        view_window.geometry("400x300")
            
        passwords = self.manager.view_passwords()
        if not passwords:
            tk.Label(view_window, text="No hay contraseñas guardadas.").pack(pady=10)
        else:
            for service, entry in passwords.items():
                tk.Label(view_window, text=f"Servicio: {service}").pack()
                tk.Label(view_window, text=f"Nombre de usuario: {entry['username']}").pack()
                tk.Label(view_window, text=f"Contraseña: {entry['password']}").pack()
                tk.Label(view_window, text="-"*40).pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()