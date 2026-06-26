# clase animal con metodos y atributos privados
 
class Animal:
    # Constructor de la clase
    def __init__(self, especie, edad):  # Constructor de la clase
        # atributos privados
        self.__especie = especie  # Atributo privado
        self.__edad = edad  # Atributo privado

   # metodos privados
    def __obtener_especie(self):  # Método privado para obtener la especie
        return self.__especie

    def __obtener_edad(self):  # Método privado para obtener la edad
        return self.__edad
    # Métodos públicos para acceder a los métodos privados
    def obtener_informacion(self):  # Método público para obtener toda la información
        especie = self.__obtener_especie()
        edad = self.__obtener_edad()
        return f"Especie: {especie}, Edad: {edad}"
# si  la clase tiene metodos y atribustos privados no se puede acceder a ellos desde fuera de la clase, entonces es necesario que tenga un metodo publico para acceder a ellos
# objeto de la clase Animal
animal = Animal("Perro", 5)
# Accediendo a los atributos privados a través de métodos públicos  
print(animal.obtener_informacion())  # Salida: Especie: Perro, Edad: 5