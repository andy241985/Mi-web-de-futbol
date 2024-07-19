from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Clase para manejar el catálogo de fútbol argentino
class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

        # Crear las tablas si no existen
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            posicion VARCHAR(100),
            club VARCHAR(100),
            edad INT
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS partidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE,
            rival VARCHAR(100),
            resultado VARCHAR(50)
        )''')

        self.conn.commit()

    def agregar_jugador(self, nombre, posicion, club, edad):
        sql = "INSERT INTO jugadores (nombre, posicion, club, edad) VALUES (%s, %s, %s, %s)"
        valores = (nombre, posicion, club, edad)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def listar_jugadores(self):
        self.cursor.execute("SELECT * FROM jugadores")
        jugadores = self.cursor.fetchall()
        return jugadores

    def agregar_partido(self, fecha, rival, resultado):
        sql = "INSERT INTO partidos (fecha, rival, resultado) VALUES (%s, %s, %s)"
        valores = (fecha, rival, resultado)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def listar_partidos(self):
        self.cursor.execute("SELECT * FROM partidos")
        partidos = self.cursor.fetchall()
        return partidos

# Configurar la instancia de Catalogo para la aplicación de fútbol argentino
catalogo = Catalogo(host='localhost', user='root', password='', database='futbol_argentino')

# Rutas para manejar jugadores y partidos
@app.route('/jugadores', methods=['GET', 'POST'])
def jugadores():
    if request.method == 'GET':
        jugadores = catalogo.listar_jugadores()
        return jsonify(jugadores)
    elif request.method == 'POST':
        datos = request.get_json()
        nombre = datos['nombre']
        posicion = datos['posicion']
        club = datos['club']
        edad = datos['edad']
        catalogo.agregar_jugador(nombre, posicion, club, edad)
        return 'Jugador agregado correctamente'

@app.route('/partidos', methods=['GET', 'POST'])
def partidos():
    if request.method == 'GET':
        partidos = catalogo.listar_partidos()
        return jsonify(partidos)
    elif request.method == 'POST':
        datos = request.get_json()
        fecha = datos['fecha']
        rival = datos['rival']
        resultado = datos['resultado']
        catalogo.agregar_partido(fecha, rival, resultado)
        return 'Partido agregado correctamente'

if __name__ == '__main__':
    app.run(debug=True)
