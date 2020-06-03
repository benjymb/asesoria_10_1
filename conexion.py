from psycopg2 import connect, Error
from logger import escribir_al_log


class ConexionPG:

    db = None
    cursor = None
    tabla = None

    def __init__(self, **parametros):
        try:
            self.db = connect(
                host=parametros['direccion_servidor'],
                user=parametros['usuario'],
                password=parametros['contrasena'],
                database=parametros['base_datos']
            )
            self.cursor = self.db.cursor()
            self.tabla = parametros['tabla']
        except Error as e:
            escribir_al_log(e, "Ocurrio un error al conectar a la base de datos")

    def __del__(self):
        self.db.close()

    def _ejecutar_sql(
        self, sentencia_sql, parametros=None, 
        escribir_en_bd=True
    ):
        try:
            self.cursor.execute(sentencia_sql, parametros) # execute corre las sentencias sql
            if escribir_en_bd:
                self.db.commit()
        except Exception as e:
            escribir_al_log(e, f"Ocurrio un error al ejecutar la sentencia SQL:\n\n{sentencia_sql}\n")
            if escribir_en_bd:
                self.db.rollback()

    def _leer_desde_sql(self):
        registros = []
        try:
            registros = self.cursor.fetchall()
        except Exception as e:
            escribir_al_log(e, f'Un error ocurrió al momento de leer desde la BD')
        return registros
            
    def crear_tabla(self, sentencia_sql=None):
        if sentencia_sql is None:
            sentencia_sql = """
            CREATE TABLE mitabla1(
                id SERIAL,
                nombre VARCHAR(50) NOT NULL,
                PRIMARY KEY (id)
            )
            """
        self._ejecutar_sql(sentencia_sql)
        
    def insertar_datos(self, nombre):
        self._ejecutar_sql(
            sentencia_sql="INSERT INTO " + self.tabla + " (nombre) VALUES (%s)",
            parametros=(nombre,)
        )

    def leer_datos(self):
        # Ejecutar SELECTs
        self._ejecutar_sql(
            "SELECT * FROM " + self.tabla + " ",
            escribir_en_bd=False
        )
        return self._leer_desde_sql()    

    def obtener_registro(self, registro_id):
        self._ejecutar_sql(
            "SELECT * FROM " + self.tabla + " WHERE id=%s",
            (registro_id,),
            escribir_en_bd=False
        )
        return self._leer_desde_sql()

    def buscar_por_nombre(self, nombre, registro_id):
        self._ejecutar_sql(
            "SELECT * FROM " + self.tabla + " WHERE id=%s AND nombre=%s",
            (registro_id, nombre),
            escribir_en_bd=False
        )
        return self._leer_desde_sql()

    def eliminar_registro(self, registro_id):
        self._ejecutar_sql(
            "DELETE FROM " + self.tabla + " WHERE id=%s",
            (registro_id,)
        )

    def cambiar_tabla(self, tabla):
        self.tabla = tabla