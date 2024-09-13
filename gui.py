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
        
        if not self.manager.master_password_exist():
            self.create_new_master_password_window()
        else:
            self.create_master_password_window()
            
    def create_new_master_password_window(self):
        #Ventana para crear una contraseña maestra
        self.new_master_password_window = tk.Toplevel(self.root)
        self.new_master_password_window.title("Crear clave maestra")
        self.new_master_password_window.geometry("300x200")
        
        tk.Label(self.new_master_password_window, text="Ingrese su nueva clave maestra: ").pack(pady=10)
        self.new_password_entry = tk.Entry(self.new_master_password_window, show="*")
        self.new_password_entry.pack(pady=10)
        
        tk.Label(self.new_master_password_window, text="Confirme su clave maestra: ").pack(pady=10)
        self.confirm_password_entry = tk.Entry(self.new_master_password_window, show="*")
        self.confirm_password_entry.pack(pady=10)
        
        tk.Button(self.new_master_password_window, text="Guardar", command=self.save_new_master_password).pack(pady=10)
        
    def save_new_master_password(self):
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if new_password and confirm_password:
            if new_password == confirm_password:
                self.manager.create_master_password(new_password)
                messagebox.showinfo("Exito", "Clave maestra creada correctamente.")
                self.new_master_password_window.destroy()
                self.create_master_password_window()
            else:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
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
        tk.Button(self.root, text="Editar contraseñas", command=self.edit_password_window).pack(pady=5)
        tk.Button(self.root, text="Ver contraseñas", command=self.view_passwords).pack(pady=5)
        tk.Button(self.root, text="Eliminar contraseñas", command=self.delete_password_window).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)
            
    def add_password_window(self):
        #Creamos una ventana para agregar contraseñas
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar contraseña")
        add_window.geometry("400x300")
            
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
            
    def edit_password_window(self):
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Editar contraseña")
        
        tk.Label(self.edit_window, text="Servicio").pack(pady=5)
        self.service_entry = tk.Entry(self.edit_window)
        self.service_entry.pack(pady=5)
        
        tk.Label(self.edit_window, text="Nuevo usuario").pack(pady=5)
        self.new_username_entry = tk.Entry(self.edit_window)
        self.new_username_entry.pack(padx=5)
        
        tk.Label(self.edit_window, text="Nueva contraseña").pack(pady=5)
        self.new_password_entry = tk.Entry(self.edit_window, show="*")
        self.new_password_entry.pack(pady=5)
        
        tk.Button(self.edit_window, text="Guardar cambios", command=self.save_edited_password).pack(pady=5)
        
    def save_edited_password(self):
        service_name = self.service_entry.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        
        #Verifica si el servicio existe
        if service_name not in self.manager.dict_password:
            tk.messagebox.showerror("Error", "El servicio no existe.")
            return
        
        #Llama a la funcion para actualizar la contraseña en PasswordManager
        self.manager.edit_password(service_name, new_username, new_password)
        tk.messagebox.showinfo("Exito", "Servicio actualizado correctamente")
        self.edit_window.destroy()
        
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
                
                #Codigo para crear boton de mostrar/ocultar contraseña
                password_label = tk.Label(view_window, text="Contraseña: **********")
                password_label.pack()
                
                def toggle_password_visibility(entry, label):
                    if label.cget('text').startswith('Contraseña: **********'):
                        label.config(text=f"Contraseña: {entry['password']}")
                    else:
                        label.config(text='Contraseña: **********')
                tk.Button(view_window, text="Mostrar/Ocultar",
                        command=lambda entry= entry, 
                        label=password_label: toggle_password_visibility(entry, label)).pack()
                
                tk.Label(view_window, text="-"*40).pack()
    
    def delete_password_window(self):
        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Eliminar contraseñas")
        
        tk.Label(self.delete_window, text="Servicio").pack(pady=5)
        self.service_entry = tk.Entry(self.delete_window)
        self.service_entry.pack(pady=5)
        
        tk.Button(self.delete_window, text="Buscar servicio", command=self.confirm_delete_password).pack(pady=5)
        
    def confirm_delete_password(self):
        service_name = self.service_entry.get()
        if service_name not in self.manager.dict_password:
            tk.messagebox.showerror("Error", "El servicio no existe.")
            return
        #Cuadro de confirmacion
        confirm = messagebox.askyesno("Confirmacion", f"¿Estas seguro de eliminar la contraseña para el servicio:{service_name}?")
        if confirm:
            self.manager.delete_password(service_name)
            messagebox.showinfo("Exito", "Servicio eliminado correctamente")
            self.delete_window.destroy()
        else:
            messagebox.showinfo("Cancelado", "Eliminacion cancelada")
            self.delete_window.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()