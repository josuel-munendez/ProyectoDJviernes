# patron sigliton
import os # manejo de consoloa y sus recursos 
import mysql
from mysql.connector import Error #  importar los servicios de mysql para conectar a la base de datos
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] # este esta ayudando a conectar con el archivo .env

load_dotenv() # cargando los datos que llamamos  env

# clase database para la conexio de  la base de datos de la agenda 
class Database:
    _instance = None
    # todo esto va con las intacias que desea generar para cargar la informacion de la db
    def __new__(cls):#  __new__ metodo especial de python  que llama cuando se crea un nuevo objeto
        #cls  es una referencia  a la clase que se esta creanado , en esta caso la database
        if cls.instance is None:# esla verificacion  si la variables de clase que se utiliza para almacencar la instancia unica de la clase db
            cls._instance = super(Database, cls).__new__(cls)# se crea una instancia de la clase db  utiliza metodo  __new__ de la clase parder 
            cls._instance.__connection =None
        return cls._instance # se devuekve  la instancia  unica de la se  database  que naco que sistista , conclucion conecto la base de datos
    
    # esta es una forma de patro  de desarollo que se llama sigliton , para la calse de base de datos, lo que significa  que solo puede crear una instancia de la clase  db  en todo el programa. Si se desea crear otra instancia, se devuelve a la instancia ya instanciada.
    def get_connection(self):
        if self._connection is None or not self.__connection.is_connected():
            try:
                self._connection = mysql.connector.connect(host=os.getenv('DB_HOST'),user=os.getenv('DB_USER'),password=os.getenv('DB_PASSWORD'),database=os.getenv('DB_NAME'),Charset='utf8mb4')
                print("✅ conexion super buena de Mysql")
            except Error as e:
                print(f"❌ error de la conexion de la base de datos: {e}")
        return self._connection
    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("🔌 conexion cerrada")

