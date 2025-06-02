from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from inference_sdk import InferenceHTTPClient
import os
#lock = threading.Lock()  # Lock para sincronizar el acceso
# Configuración de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # CORS global para desarrollo
comparacion = {
    "detectados": ["Sandía", "Uvas", "Limón"],
    "faltantes": ["Lima"]
}

# Middleware adicional para asegurar CORS en todas las respuestas
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,OPTIONS"
    return response

# Conexión a MongoDB
try:
    client = MongoClient("mongodb+srv://javier:javier@cluster0.t5cgbal.mongodb.net/?retryWrites=true&w=majority")
    db = client["ListaCompraDB"]
    productos_collection = db["productos"]
    print("✅ Conexión exitosa a MongoDB")
except Exception as e:
    print(f"❌ Error al conectar con MongoDB: {e}")

# Cliente Roboflow
try:
    ROBOFLOW_CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="QNvyTLvOXub3WhVvABIv"
    )
    print("✅ Conexión exitosa con Roboflow")
except Exception as e:
    print(f"❌ Error en la conexión con Roboflow: {e}")

# Obtener productos
@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        productos = list(productos_collection.find({}, {"_id": 0}))
        print("Resultado de análisis de imagen:")
        print("Detectados:", comparacion["detectados"])
        print("Faltantes:", comparacion["faltantes"])
        return jsonify({"productos": productos}), 200
    except Exception as e:
        return jsonify({"error": f"No se pudieron obtener los productos: {e}"}), 500

# Agregar producto
@app.route('/productos', methods=['POST'])
def add_producto():
    try:
        data = request.json
        if not data or "nombre" not in data:
            return jsonify({"error": "Se requiere un nombre de producto"}), 400

        nombre_normalizado = data["nombre"].strip().lower()
        producto_existente = productos_collection.find_one({
            "nombre": {"$regex": f"^{nombre_normalizado}$", "$options": "i"}
        })

        if producto_existente:
            return jsonify({"error": "El producto ya existe en la lista"}), 409

        productos_collection.insert_one({"nombre": nombre_normalizado})
        return jsonify({"mensaje": "Producto agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": f"No se pudo agregar el producto: {e}"}), 500

# Eliminar producto
@app.route('/productos/<nombre>', methods=['DELETE'])
def delete_producto(nombre):
    try:
        nombre_normalizado = nombre.strip().lower()
        result = productos_collection.delete_one({
            "nombre": {"$regex": f"^{nombre_normalizado}$", "$options": "i"}
        })

        if result.deleted_count > 0:
            return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"No se pudo eliminar el producto: {e}"}), 500

# Tomar foto y detectar alimentos con Roboflow
@app.route('/tomar-foto', methods=['POST'])
def tomar_foto():
    IMAGE_PATH = "variedad.jpg"

    try:
        if not os.path.exists(IMAGE_PATH):
            return jsonify({"error": "No se encontró la imagen"}), 400

        result = ROBOFLOW_CLIENT.infer(IMAGE_PATH, model_id="food-imgae-yolo/2")

        if "predictions" not in result or not result["predictions"]:
            return jsonify({
                "mensaje": "Foto tomada, pero no se detectaron alimentos.",
                "ruta": IMAGE_PATH,
                "alimentos": []
            }), 200

        alimentos_detectados = list(set([
            prediction["class"].lower() for prediction in result["predictions"]
        ]))

        return jsonify({
            "mensaje": "Foto tomada",
            "ruta": IMAGE_PATH,
            "alimentos": alimentos_detectados
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error al procesar la imagen: {e}"}), 500



# Ejecutar servidor Flask: python api.py
if __name__ == '__main__':
    print("🚀 API corriendo en http://localhost:8000 con MongoDB y Roboflow")
    app.run(host='0.0.0.0', port=8000, debug=True)








