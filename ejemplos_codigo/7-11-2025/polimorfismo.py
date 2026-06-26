# polimorfismo rn python  que se estara aplicando en dos clases
#clase padre
""" cuando nada es publico
_ es protegido
__ es privado
¿que es polimorfismo?
    El polimorfismo es un concepto de programación orientada a objetos que permite que diferentes clases puedan ser tratadas como instancias de una clase común. En Python, esto se logra mediante la sobrescritura de métodos en las subclases.
"""
class Usuario:
    # Constructor de la clase
    def __init__(self, nombre,correo):# los atributos de la clase
        self.nombre = nombre # atributos  publicos
        self.correo = correo
    def mostrar_informacion(self):
        return f"Usuario: {self.nombre}, Correo: {self.correo}"

class Administrador(Usuario):
    def __init__(self, nombre, correo, permisos):
        super().__init__(nombre, correo)
        self.permisos = permisos

    def mostrar_informacion(self):
        return f"Administrador: {self.nombre}, Correo: {self.correo}, Permisos: {self.permisos}"
# clase vendedor cuyo metodo mostrar_informacion es diferente al de la clase padre
class Vendedor(Usuario):
    def __init__(self, nombre, correo, region):
        super().__init__(nombre, correo)# Llamada al constructor de la clase padre
        self.region = region

    def mostrar_informacion(self):
        return f"Vendedor: {self.nombre}, Correo: {self.correo}, Región: {self.region}" 
#objetos de las clases 
usuario = Administrador("Ana", "ana@ejemplo.com", ["crear", "editar"])
vendedor = Vendedor("Luis", "luis@ejemplo.com", "Norte")
# Usando polimorfismo para llamar al mismo método en diferentes clases
usuarios = [usuario, vendedor]
for user in usuarios:
    print(user.mostrar_informacion())   
# Salida:
# Administrador: Ana, Correo: ana@ejemplo.com, Permisos: ['crear', 'editar']
# Vendedor: Luis, Correo: luis@ejemplo.com, Región: Norte