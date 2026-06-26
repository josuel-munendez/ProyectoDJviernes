#  definicion de atributos protegidos y herencia
# Los atributos protegidos son aquellos que pueden ser accedidos desde la clase y sus subclases. Se definen utilizando un guion bajo al inicio de su nombre.
class Tarea:
    def __init__(self, nombre):
        self._nombre = nombre

    def _validar_duracion(self, duracion):
        if duracion <= 0:
            raise ValueError("La duración debe ser un valor positivo.")
        return duracion
    def _calcular_esfuerzo(self, duracion):
        
        return duracion * 1.5  # Ejemplo de cálculo de esfuerzo
    #metodo publico para acceder a los metodos protegidos
    def programar_tarea(self, duracion):
        duracion_validada = self._validar_duracion(duracion)
        esfuerzo = self._calcular_esfuerzo(duracion_validada)
        return f"Tarea '{self._nombre}' programada por {duracion_validada} horas con un esfuerzo estimado de {esfuerzo} unidades."
# clase que hereda de tarea
class TareaMatematicas(Tarea):
    def __init__(self, nombre):
        super().__init__(nombre)# Llamada al constructor de la clase padre
    #sobreescribir los metodo protegidos de la clase padre
    def _calcular_esfuerzo(self, duracion):
        return duracion * 2.0  # Ejemplo de cálculo de esfuerzo específico para matemáticas
    def crear_ejercicio(self, duracion,tipo):
        #usando metodo protegido de la clase padre
        self._validar_duracion(duracion)# Validar duración usando el método protegido de la clase padre
        esfuerzo = self._calcular_esfuerzo(duracion)# Calcular esfuerzo usando el método sobrescrito
        return f"Ejercicio de Matemáticas '{self._nombre}' creado por {duracion} horas con un esfuerzo estimado de {esfuerzo} unidades." # Salida: Ejercicio de Matemáticas 'Álgebra' creado por 3 horas con un esfuerzo estimado de 6.0 unidades.
# objeto de la clase TareaMatematicas
tareaTrigonometria = TareaMatematicas("Trigonometría")
print(tareaTrigonometria.programar_tarea(4))  # Salida: Tarea 'Trigonometría' programada por 4 horas con un esfuerzo estimado de 6.0 unidades.
print(tareaTrigonometria.crear_ejercicio(3,"Álgebra"))  # Salida: Ejercicio de Matemáticas 'Álgebra' creado por 3 horas con un esfuerzo estimado de 6.0 unidades.
