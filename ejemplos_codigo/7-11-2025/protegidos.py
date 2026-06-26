# este es un ejemplo de una clase que tiene metodos y atributos protegidos
# con el fin de que solo puedan ser accedidos desde la clase y sus subclases
# una clase tarea, que le hereda a matematicas y el objeto es tareaTrigonometria
class Tarea:# clase tarea padre
    # Constructor de la clase
    def __init__(self, nombre, descripcion):  # Constructor de la clase
        # atributos protegidos
        self._nombre = nombre  # Atributo protegido _nombre
        self._descripcion = descripcion  # Atributo protegido _descripcion

    # Métodos protegidos para acceder a los atributos protegidos
    def _obtener_nombre(self):  # Método protegido para obtener el nombre _
        return self._nombre

    def _obtener_descripcion(self):  # Método protegido para obtener la descripción
        return self._descripcion
    # Método público para obtener toda la información
    def obtener_informacion(self):  # Método público para obtener toda la información
        nombre = self._obtener_nombre()
        descripcion = self._obtener_descripcion()
        return f"Tarea: {nombre}, Descripción: {descripcion}"
# objeto de la clase Tarea
tarea = Tarea("Trigonometría", "Resolver problemas de triángulos")
print(tarea.obtener_informacion())  # Salida: Tarea: Trigonometría, Descripción: Resolver problemas de triángulos