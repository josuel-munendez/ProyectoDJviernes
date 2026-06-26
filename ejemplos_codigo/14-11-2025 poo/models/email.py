class Email:
    """ asociaciones : esta clase esta asoiada a persona"""
    def __init__(self, direccion:str, persona_id: int =None):
        self.id= None # por que en la base de datos lo tengo  auto incrementado
        self.direccion= direccion # debe recibir direccion 
        self.persona_id = persona_id # debe recibir direccion
         
    def __str__(self):
        return f"Email({self.id}, {self.direccion})"