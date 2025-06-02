from inference_sdk import InferenceHTTPClient

# Configuración del cliente de Roboflow
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",  # URL base de la API
    api_key="QNvyTLvOXub3WhVvABIv"         # Tu clave API
)

# Imagen de prueba (local o remota)
IMAGE_PATH = "variedad.jpg"  # Reemplaza con la ruta de tu imagen

# Modelo que deseas usar
MODEL_ID = "food-imgae-yolo/2"  # ID del modelo y versión

# Realizar la inferencia
result = CLIENT.infer(IMAGE_PATH, model_id=MODEL_ID)

# Mostrar resultados
print("\n🔍 Resultados de la inferencia:")
for prediction in result["predictions"]:
    print(f"- {prediction['class']} ")
