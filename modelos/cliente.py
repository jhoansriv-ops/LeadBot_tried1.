class Cliente:
    """Entidad que representa a un cliente en el sistema LeadBot."""
    def __init__(self, id_cliente=None, tipo_documento="CC", num_documento="", 
                 nombre="", telefono="", correo="", direccion="", ciudad="", estado="ACTIVO"):
        self.id_cliente = id_cliente
        self.tipo_documento = tipo_documento
        self.num_documento = num_documento
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.ciudad = ciudad
        self.estado = estado