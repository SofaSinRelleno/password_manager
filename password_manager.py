import password_entry
import json
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64

class PasswordManager:
    def __init__(self, json_file='passwords.json', master_password_file='master_password.json', key_file='cipher_key.key'):
        #Inicializa el diccionario para almacenar contraseñas
        self.json_file = json_file
        self.master_password_file = master_password_file
        self.key_file = key_file
        self.key = self.load_cipher_key()
        self.cipher = Fernet(self.key)
        self.dict_password = self.load_passwords()
        self._master_password_hash = self.load_master_password()
        
    
    def save_passwords(self):
        #Convierte cada entrada a un diccionario antes de guardarla
        with open(self.json_file, 'w') as file:
            password_dict = {}
            for service, entry in self.dict_password.items():
                try:
                    #Cifra la contraseña antes de guardarlas
                    encrypted_password = self.cipher.encrypt(entry['password'].encode())
                    password_dict[service] = {
                        'username': entry['username'],
                        'password': base64.b64encode(encrypted_password).decode()
                    }
                except Exception as e:
                    print(f"Error al cifrar la contraseña para {service}: {e}")
            json.dump(password_dict, file, indent=4)
            
    def load_passwords(self):
        #Cargamos las contraseñas guardadas en el archivo JSON
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                for service, entry in data.items():
                    #Decodifica la contraeña de base64 y luego descifra
                    encrypted_password = base64.b64decode(entry['password'])
                    entry['password'] = self.cipher.decrypt(encrypted_password).decode()
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            #Si el archivo no existe, creamos un diccionario vacio
            return {}
        
    def load_master_password(self):
        #Carga la contraseña hash si existe
        try:
            with open(self.master_password_file, 'r') as file:
                data = json.load(file)
                #Decodificamos el hash almacenado en base64
                return base64.b64decode(data.get('master_password_hash', ''))
        except FileNotFoundError:
            return b''
        
    def save_master_password(self, master_password_hash):
        #Convertimos el hash a una representacion de base64 para poder guardarlo en el JSON
        with open(self.master_password_file, 'w') as file:
            base64_hash = base64.b64encode(master_password_hash).decode('utf-8')
            json.dump({'master_password_hash': base64_hash}, file)
            
    def generate_cipher_key(self):
        #Genera una nueva clave de cifrado
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as file:
            file.write(key)
        return key
    
    def load_cipher_key(self):
        #Carga la clave de cifrado si existe
        try:
            with open(self.key_file, 'rb') as file:
                key = file.read()
                return key
        except FileNotFoundError:
            #Si no hay clave, genera una.
            return self.generate_cipher_key()
        
    def create_master_password(self):
        #Solicita al usuario que cree una contraseña maestra nueva
        while True:
            master_password = input("Cree una contraseña maestra: ")
            if len(master_password) < 8:
                print("La contraseña debe tener al menos 8 caracteres")
                continue
            if not any(char.isdigit() for char in master_password):
                print("La contraseña maestra debe tener al menos un numero")
                continue
            if not any(char.isalpha() for char in master_password):
                print("La contraseña maestra debe tener al menos una letra")
                continue
            break
        
        master_password_hash = hashlib.sha256(master_password.encode()).digest()
        self._master_password_hash = master_password_hash
        self.save_master_password(master_password_hash)
        print("Contraseña maestra creada y guardada exitosamente")
            

    def verifyPassword(self, password):
        #Verifica si la contraseña ingresada coincide con el hash almacenado
        return hashlib.sha256(password.encode()).digest() == self._master_password_hash
    
    def prompt_master_password(self):
        #Solicita la contraseña maestra al usuario y verifica
        max_attempts = 5
        attempt = 0
        while attempt < max_attempts:
            input_password = input("Por favor, ingrese su clave maestra: ")
            if self.verifyPassword(input_password):
                print("Contraseña correcta. Acceso concedido.")
                return True
            else:
                attempt +=1
                print(f"Contraseña incorrecta. Intento {attempt}/{max_attempts}.")
        print("Numero maximo de intentos alcanzados. Saliendo del sistema.")
        exit()
        
    def add_password(self, service_name, username, password):
        if not service_name or not username or not password:
            print("Todos los campos son obligatorios.")
            return
                
        if service_name in self.dict_password:
            print(f"La entrada para el servicio '{service_name}' ya existe. ¿Desea sobreescribirla?")
            confirm = input().strip().lower()
            if confirm != 'si':
                print("Operacion cancelada.")
                return
            
        try:
            #Ciframos la contraseña
            encrypted_password = self.cipher.encrypt(password.encode())
            #Guardamos la contraseña cifrada
            self.dict_password[service_name] = {
                'username': username,
                'password': encrypted_password.decode('utf-8')
            }
            self.save_passwords()
            print("Contraseña ingresada exitosamente.")
        except ValueError as ve:
            print(f"Error al agregar la contraseña: {ve}")
        
        
    def edit_password(self):
        service_name =  input("Ingrese el nombre del servicio para editar: ")
        
        if service_name not in self.dict_password:
            print(f"No se encontro ninguna entrada para el servicio solicitado: '{service_name}'.")
            return
        
        #Obtenemos la entrada actual
        entry = self.dict_password[service_name]
        print(f"Username actual: {entry['username']}")
        new_username = input("Ingrese el nuevo username/email (dejar en blanco para no cambiar): ")
        new_password = input("Ingrese la nueva contraseña (dejar en blanco para no cambiar): ")
        
        if not new_username and not new_password:
            print("No se realizaron cambios.")
            return
        
        #Actualizamos los atributos en PasswordEntry
        try:
            if new_username:
                entry['username'] = new_username
            if new_password:
                encrypted_password = self.cipher.encrypt(new_password.encode()).decode()
                entry['password'] = encrypted_password
                
            self.save_passwords()
            print(f"La contraseña para el servicio '{service_name}' ha sido actualizada correctamente.")
            
        except ValueError as ve:
            print(f"Error al editar la contraseña: {ve}")
        
    def delete_password(self):
        service_name = input("Ingrese el nombre del servicio para eliminarlo: ")
        
        if service_name not in self.dict_password:
            print(f"No se encontro ninguna entrada para el servicio solicitado: '{service_name}'.")
            return
        #Se requiere confirmacion.
        confirm = input(f"¿Esta seguro de que desea eliminar la entrada para '{service_name}'? (si/no)")
        
        if confirm.lower() == "si":
            del self.dict_password[service_name]
            self.save_passwords()
            print(f"La entrada para el servicio '{service_name}' ha sido correctamente eliminada.")
        else:
            print("Operacion cancelada.")
            
    def view_passwords(self):
        if not self.dict_password:
            print("No hay contraseñas guardadas.")
            return
        
        print("\nContraseñas guardadas: ")
        passwords = {}
        for service, entry in self.dict_password.items():
            try:
                #Decodificamos la contraseña cifrada
                encrypted_password = entry['password'].encode('utf-8') #Convertimos el string a bytes
                decrypted_password = self.cipher.decrypt(encrypted_password).decode('utf-8') #Desencriptamos
            except Exception as e:
                print(f"Error al descifrar la contraseña para {service} : {e}")
                decrypted_password = "[Error al descrifrar]"
                
            passwords[service] = {
                'username': entry['username'],
                'password': decrypted_password
            }
        return passwords
    
    def selec_option(self):
        print("¡Buenos dias! ¿Que desea realizar? (Escribir solo el numero): ")
        print("1: Agregar contraseña")
        print("2: Editar contraseña")
        print("3: Eliminar contraseña")
        print("4: Mirar contraseñas")
        print("5: Salir")
        
        try:
            seleccion = int(input("Ingrese su opcion: "))
        except ValueError:
            print("Seleccion invalida. Por favor ingrese un numero valido.")
            return
        
        if seleccion == 1:
            self.add_password()
        elif seleccion == 2:
            self.edit_password()
        elif seleccion == 3:
            self.delete_password()
        elif seleccion == 4:
            self.view_passwords()
        elif seleccion == 5:
            print("Saliendo del gestor de contraseñas.")
            exit()
        else:
            print("Opcion no valida. Por favor, ingrese 1, 2 o 3")
            
def main():
    print("Bienvenido al gestor de contraseñas: ")
        
    #Creamos una instancia de PasswordManager       
    manager = PasswordManager()
        
    while True:
        manager.selec_option()
            
if __name__ == '__main__':
    main()
            
'''
Tareas pendientes:
- Pensar en la interfaz grafica. Tkinter es una buena opcion.
    + Falta edit password y delete password
    + Arreglar errores de visualizacion
    + Agregar una interfaz mas bonita
    
- Posible migracion a servidor personal en netbook
'''