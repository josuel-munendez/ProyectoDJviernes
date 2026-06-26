class Telefono:
    """asociacion : por que esta asociado  con la clase persona"""
    def  __init__(self, numero: str, persona_id: int):
        self.id =None# por que esta en db con autoincrementado 
        # It looks like there is a typo in the code snippet you provided. The line `self` is
        # incomplete and does not serve any purpose in its current form. It seems like there might
        # have been an intention to write some code after `self`, but it is missing.
        self.numero = numero
        self.persona_id= persona_id
    def __str__(self):
        return f" telefono ({self.id}, {self.numero})"
        