Autor: Javier Navas Martín
Proyecto desarrollado para la universidad de Nebrija - Grado en Ingeniería Informática
📌 Descripción

Este proyecto consiste en el desarrollo de una aplicación móvil inteligente que permite gestionar automáticamente una lista de la compra mediante visión por computador e inteligencia artificial. El sistema reconoce productos en imágenes del interior de una nevera y detecta los alimentos que faltan, todo ello de forma visual y amigable para el usuario.

Este sistema forma parte de un proyecto más ambicioso de domotización del hogar.
🔧 Tecnologías utilizadas

    Frontend: React Native + Expo

    Backend: Python 3.11 + FastAPI

    Visión artificial: Roboflow API + modelo YOLO (Food Image)



📲 Funcionalidades principales

    ✍️ Gestión manual de la lista de la compra

    📸 Simulación de captura de imagen (futuro: conexión con cámara Raspberry Pi)

    🔍 Envío de imagen a Roboflow para análisis

    ✅ Comparación de productos detectados vs lista deseada

    📊 Visualización diferenciada de productos presentes y faltantes

    🔐 Comunicación segura (uso de variables de entorno y HTTPS en producción)
    
📸 Ejemplo de funcionamiento

    El usuario abre la app y consulta su lista.

    Pulsa el botón "Tomar imagen".

    Se envía una imagen predefinida al backend.

    El backend reenvía la imagen a Roboflow.

    Se comparan los productos detectados con la lista.

    La app muestra en verde los productos faltantes y en rojo los detectados.

📈 Resultados

    App funcional probada en dispositivos Android e iOS.

    API completamente integrada con visión artificial.

    Reconocimiento aceptable con imágenes estáticas.

    Preparado para futura integración con sensores físicos y modelos personalizados.

🔮 Líneas futuras

    Integración real con cámara + Raspberry Pi.

    Almacenamiento persistente de listas (MongoDB).

    Sistema de login con autenticación.

    Entrenamiento de modelo propio con dataset doméstico.

    Recomendaciones inteligentes y alertas.

📄 Licencia

Este proyecto es parte de un trabajo académico. No se permite su publicación o distribución sin autorización.
