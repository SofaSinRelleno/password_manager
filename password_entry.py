import bcrypt

class PasswordEntry:
    
    #Clase constructora del nombre del servicio, el usuario y la contraseña
    def __init__(self, service_name, username, password):
        self.service_name = service_name
        self.username = username
        self.password = password
        
    @property
    def service_name(self):
        return self._service_name
        
    #Evalua si el nombre del servicio no esta vacio o no es una cadena de texto
    @service_name.setter
    def service_name(self, value):
            
        if not value or not isinstance(value, str):
            raise ValueError("El nombre del servicio no puede estar vacio y debe ser una cadena de texto.")
        self._service_name = value
            
    @property
    def username(self):
        return self._username
    
    #Evalua si el usuario no esta vacio o no es una cadena de texto
    @username.setter
    def username(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("El nombre de usuario no puede estar vacio y debe ser una cadena de texto.")
        self._username = value
            
    @property

    def password(self):
        return self._password
        
    #Evalua si la contraseña no esta vacia o no es una cadena de texto. Ademas verifica longitud, si hay numero o si hay algun caracter
    @password.setter
    def password(self, value):
            
        if not value or not isinstance(value, str):
            raise ValueError("La contraseña no puede estar vacia y debe ser una cadena de texto.")
        if len(value) < 8:
            raise ValueError("La contraseña es demasiado corta.")
        if not any(char.isdigit() for char in value):
            raise ValueError("La contraseña debe tener al menos un numero.")
        if not any(char.isalpha() for char in value):
            raise ValueError("La contraseña debe tener al menos una letra")
    #mediante bcrypt, hashea y agrega un salt a la contraseña
        self._password = bcrypt.hashpw(value.encode(), bcrypt.gensalt())

    #Se chequea si la contraseña ingresada coincide con el hash almacenado
    def check_password(self, password):
        #Verifica si la contraseña coincide con el hash almacenado
        return bcrypt.checkpw(password.encode(), self._password)
    
    
    def __str__(self):
        #Devuelve una representacion amigable del objeto
        return f"PasswordEntry(service_name = '{self._service_name}', username = '{self._username}', password= 'hashed_password')"
    
    def __repr__(self):
        return f"PasswordEntry(service_name = '{self._service_name}', username = '{self._username}', password= 'hashed_password')"
    
