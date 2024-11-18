from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS", "DELETE"])

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='tienda_futbol',  
        user='root',
        password=''
    )
    if connection.is_connected():
        return connection
    else:
        return None

# Lista de productos ahora son artículos de fútbol
products = [
    {'id': 1, 'name': 'Balón de Fútbol', 'description': 'Balón oficial para partidos profesionales', 'price': 120000, 'image': 'img/ball.jpg', 'category': 'Balones'},
    {'id': 2, 'name': 'Zapatos de Fútbol', 'description': 'Zapatos de fútbol para césped natural', 'price': 250000, 'image': 'img/cleats.jpeg', 'category': 'Calzado'},
    {'id': 3, 'name': 'Camiseta del Equipo Nacional', 'description': 'Camiseta oficial del equipo nacional', 'price': 100000, 'image': 'img/jersey.jpg', 'category': 'Ropa'},
    {'id': 4, 'name': 'Espinilleras', 'description': 'Espinilleras ligeras y resistentes', 'price': 50000, 'image': 'img/shin-guards.jpg', 'category': 'Protección'},
    {'id': 5, 'name': 'Red para Portería', 'description': 'Red resistente para porterías de entrenamiento', 'price': 80000, 'image': 'img/net.jpg', 'category': 'Accesorios'},
]

cart = []

@app.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.get_json()

    if not all(k in new_product for k in ('id', 'name', 'description', 'price', 'image', 'category')):
        return jsonify({"error": "Faltan datos para el producto"}), 400

    products.append(new_product)
    return jsonify({"message": "Producto agregado exitosamente"}), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/api/cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('id')
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        cart.append(product)
        return jsonify({"message": "Producto agregado al carrito"}), 201
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/api/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item['id'] != product_id]
    return jsonify({"message": "Producto eliminado del carrito"}), 200

@app.route('/api/change-password', methods=['POST'])
def change_password():
    data = request.get_json()

    email = data.get('email')
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
      
        query = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and user['contraseña'] == old_password:

            update_query = "UPDATE usuarios SET contraseña = %s WHERE email = %s"
            cursor.execute(update_query, (new_password, email))
            connection.commit()
            return jsonify({"message": "Contraseña cambiada exitosamente"}), 200
        else:
            return jsonify({"error": "Contraseña actual incorrecta"}), 400
    else:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('username')  
    password = data.get('password')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and user['contraseña'] == password:  
            return jsonify({'user': user, 'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401
    else:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)

        query = "INSERT INTO usuarios (email, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (email, password))
        connection.commit()

        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    else:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)
