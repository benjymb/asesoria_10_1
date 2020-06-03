from conexion import ConexionPG
from atributos_conexion import ATRIBUTOS

class Modelo:

    _conexion = None

    @classmethod
    def inicializar_conexion(cls):
        if cls._conexion is None:
            cls._conexion = ConexionPG(
                **ATRIBUTOS
            )


class Editorial(Modelo):


    def __init__(self, nombre, editorial_id=None):
        self.nombre = nombre
        self.editorial_id = editorial_id

    def guardar(self):
        self.__class__._conexion._ejecutar_sql(
            "INSERT INTO Editorial (nombre) VALUES (%s)",
            (self.nombre,)
        )
        self.__class__._conexion._ejecutar_sql(
            "SELECT editorial_id FROM Editorial WHERE nombre=%s ORDER BY editorial_id DESC LIMIT 1",
            (self.nombre, )
        )
        nueva_editorial = self.__class__._conexion._leer_desde_sql()
        self.editorial_id = nueva_editorial[0][0]

    def actualizar(self):
        self.__class__._conexion._ejecutar_sql(
            "UPDATE Editorial SET nombre = %s WHERE editorial_id = %s",
            (self.nombre, self.editorial_id)
        )
        

    @classmethod
    def buscar_por_nombre(cls, nombre):
        cls._conexion._ejecutar_sql(
            "SELECT nombre, editorial_id FROM Editorial WHERE nombre=%s ORDER BY editorial_id DESC LIMIT 1",
            (nombre, )
        )
        editorial_buscada = cls._conexion._leer_desde_sql()
        return Editorial(
            editorial_buscada[0][0],
            editorial_buscada[0][1]
        )
    

class Libro(Modelo):

    def __init__(
        self, titulo, autor, esta_disponible, 
        editorial_id=None, libro_id=None 
    ):
        self.titulo = titulo
        self.autor = autor
        self.esta_disponible = esta_disponible
        self.editorial_id = editorial_id
        self.libro_id = libro_id

    def guardar(self):
        self.__class__._conexion._ejecutar_sql(
            "INSERT INTO Libro (titulo, autor, esta_disponible, editorial_id) VALUES"
            "(%s, %s, %s, %s)",
            (self.titulo, self.autor, self.esta_disponible, self.editorial_id)
        )
        self.__class__._conexion._ejecutar_sql(
            "SELECT libro_id FROM Libro WHERE titulo=%s ORDER BY libro_id DESC LIMIT 1",
            (self.titulo, )
        )
        nuevo_libro = self.__class__._conexion._leer_desde_sql()
        self.libro_id = nuevo_libro[0][0]
    

Libro.inicializar_conexion() 
Editorial.inicializar_conexion()   
"""
mi_libro = Libro("Cien Anios de Soledad", "Gabriel Garcia Marquez", False, Editorial.buscar_por_nombre("Alfaguara").editorial_id)
mi_libro.guardar()
print(mi_libro.libro_id)
"""
editorial = Editorial.buscar_por_nombre("Alfaguara")
editorial.nombre = "Santillana"
editorial.actualizar()