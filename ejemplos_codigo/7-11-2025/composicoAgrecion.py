"""
# vamos  acrear una clase universidad, esa calse tiene una composicion con la clase Departamento y una agregacion con la clase profesor.

#La composicion  se indica con la lista departamento enla clase universidad,  que es responsable  de la creacion  y destruccion de los departamentos.

# la agregacion  se indica  con la list de profesores en la clase  universidad , que no es responsable  de la creacion y destruccion de los profesores.
clase profesor tiene atributos nombre y edad, y la clase departamento tiene atributos nombre y cursos tipo listas, y la clase universidad tiene atributos nombre, departamentos y profesores.
"""
class Profesor:
    def __init__(self, nombre, edad):# Constructor de la clase
        self.nombre = nombre # Atributo publico
        self.edad = edad# Atributo publico
    def mostrar_profesor(self): # Método para mostrar información del profesor
        return f"Profesor: {self.nombre}, Edad: {self.edad}" # Salida: Profesor: Juan, Edad: 40
class Departamento:
    def __init__(self,nombre):# Constructor de la clase
        self.nombre = nombre # Atributo publico
        self.cursos = [] # Atributo publico, lista de cursos
    def agregar_curso(self, curso): # Método para agregar un curso
        self.cursos.append(curso)
    def mostrar_departamento(self): # Método para mostrar información del departamento
        return f"Departamento: {self.nombre}, Cursos: {', '.join(self.cursos)}" # Salida: Departamento: Matemáticas, Cursos: Álgebra, Cálculo
class Universidad:
    def __init__(self, nombre):# Constructor de la clase
        self.nombre = nombre # Atributo publico
        self.departamentos = [] # Atributo publico, lista de departamentos (composición)
        self.profesores = [] # Atributo publico, lista de profesores (agregación)
    def agregar_departamento(self, departamento): # Método para agregar un departamento
        self.departamentos.append(departamento)
    def agregar_profesor(self, profesor): # Método para agregar un profesor
        self.profesores.append(profesor)
    def mostrar_universidad(self): # Método para mostrar información de la universidad
        # Mostrar información de la universidad, departamentos y profesores
        deptos_info = [dept.mostrar_departamento() for dept in self.departamentos]
        # Mostrar información de los departamentos
        profes_info = [prof.mostrar_profesor() for prof in self.profesores]
        # Mostrar información de los profesores
        return f"Universidad: {self.nombre}\nDepartamentos:\n" + "\n".join(deptos_info) + "\nProfesores:\n" + "\n".join(profes_info)
    #join(profes_info) este lo que hace es llamar la informacion y unirla en una sola cadena de texto
#objetos de las clases
#prosor
profesor1 = Profesor("Juan", 40)
profesor2 = Profesor("María", 35)
#departamento
departamento1 = Departamento("Matemáticas")
departamento1.agregar_curso("Álgebra")
departamento1.agregar_curso("Cálculo")
#universidad
universidad = Universidad("Universidad Nacional")
universidad.agregar_profesor(profesor1)
universidad.agregar_profesor(profesor2)
universidad.agregar_departamento(departamento1)
print(universidad.mostrar_universidad())