"""
    definicion de atributos privados
    Los atributos privados son aquellos que no pueden ser accedidos directamente desde fuera de la clase. Se definen utilizando un guion bajo al inicio de su nombre.
"""
class Persona:
    def __init__(self, nombre, edad):# Constructor de la clase
        # atributos privados
        self.__nombre = nombre# Atributo privado
        self.__edad = edad# Atributo privado
    # Métodos públicos para acceder a los atributos privados
    def obtener_nombre(self):# Método para obtener el nombre
        return self.__nombre

    def obtener_edad(self):# Método para obtener la edad
        return self.__edad
    def obtener_informacion(self):# Método para obtener toda la información
        return f"Nombre: {self.__nombre}, Edad: {self.__edad}"
# objeto de la clase Persona
persona = Persona("Melisa", 17)
# Accediendo a los atributos privados a través de métodos públicos
 # Salida: 17
print(persona.obtener_informacion())  # Salida: Nombre: Melisa, Edad: 17