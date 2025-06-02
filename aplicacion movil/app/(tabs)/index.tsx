import React, { useEffect, useState } from "react";
import { View, Text, FlatList, TextInput, TouchableOpacity, ImageBackground, StyleSheet } from "react-native";

const API_URL = "http://192.168.1.61:8000"; // Cambia por tu IP si usas un móvil físico

export default function App() {
  const [productos, setProductos] = useState([]);
  const [nuevoProducto, setNuevoProducto] = useState("");
  const [alimentosDetectados, setAlimentosDetectados] = useState([]);
  const [fotoTomada, setFotoTomada] = useState(false); // Controla si la foto fue tomada

  // Cargar productos desde la API
  const cargarProductos = async () => {
    try {
      const response = await fetch(`${API_URL}/productos`);
      const data = await response.json();
      setProductos(data.productos);
    } catch (error) {
      console.error("Error al cargar productos:", error);
    }
  };

  // Agregar un producto
  const agregarProducto = async () => {
    if (!nuevoProducto.trim()) return;
    try {
      await fetch(`${API_URL}/productos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre: nuevoProducto }),
      });
      setNuevoProducto("");
      cargarProductos();
      setFotoTomada(false); // 🔹 Restablecer para que los nuevos productos aparezcan en blanco
    } catch (error) {
      console.error("Error al agregar producto:", error);
    }
  };

  // Eliminar un producto
  const eliminarProducto = async (nombre) => {
    try {
      await fetch(`${API_URL}/productos/${nombre}`, { method: "DELETE" });
      cargarProductos();
    } catch (error) {
      console.error("Error al eliminar producto:", error);
    }
  };

  // Tomar Foto y detectar alimentos (Sin mostrar alertas)
  const tomarFoto = async () => {
    try {
      const response = await fetch(`${API_URL}/tomar-foto`, { method: "POST" });
      const data = await response.json();

      if (data.alimentos.length > 0) {
        setAlimentosDetectados(data.alimentos);
        setFotoTomada(true); // 🔹 Solo marcamos los productos con colores después de tomar la foto
      } else {
        setFotoTomada(false); // 🔹 Si no detecta alimentos, mantenemos los productos en blanco
      }
    } catch (error) {
      console.error("Error al tomar foto:", error);
    }
  };

  useEffect(() => {
    cargarProductos();
  }, []);

  return (
    <ImageBackground source={{ uri: "https://source.unsplash.com/800x600/?food" }} style={styles.background}>
      <View style={styles.container}>
        <Text style={styles.title}>Lista de la Compra 🛒</Text>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Añadir producto..."
            placeholderTextColor="#fff"
            value={nuevoProducto}
            onChangeText={setNuevoProducto}
          />
          <TouchableOpacity style={styles.botonAgregar} onPress={agregarProducto}>
            <Text style={styles.botonTexto}>➕</Text>
          </TouchableOpacity>
        </View>

        <FlatList
          data={productos}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => {
            const estaEnImagen = alimentosDetectados.includes(item.nombre.toLowerCase());
            const backgroundColor = fotoTomada
              ? (estaEnImagen ? "#ff6b6b" : "#4caf50") // 🔴 Rojo si está en la imagen, 🟢 Verde si no
              : "#ffffff"; // ⚪ Blanco antes de tomar la foto o al agregar un producto nuevo

            return (
              <View style={[styles.productoContainer, { backgroundColor }]}>
                <Text style={styles.producto}>{item.nombre}</Text>
                <TouchableOpacity onPress={() => eliminarProducto(item.nombre)} style={styles.botonEliminar}>
                  <Text style={styles.eliminarTexto}>❌</Text>
                </TouchableOpacity>
              </View>
            );
          }}
        />

        <TouchableOpacity style={styles.botonFoto} onPress={tomarFoto}>
          <Text style={styles.botonTexto}>📷 Tomar Foto</Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: { flex: 1, resizeMode: "cover" },
  container: { flex: 1, padding: 20, backgroundColor: "rgba(0, 0, 0, 0.6)" },
  title: { fontSize: 28, fontWeight: "bold", color: "#fff", textAlign: "center", marginBottom: 20 },
  inputContainer: { flexDirection: "row", marginBottom: 20, alignItems: "center" },
  input: { flex: 1, borderWidth: 1, borderColor: "#fff", padding: 10, borderRadius: 5, marginRight: 10, color: "#fff" },
  botonAgregar: { backgroundColor: "#28a745", padding: 10, borderRadius: 5 },
  botonTexto: { fontSize: 18, color: "#fff", fontWeight: "bold" },
  productoContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    padding: 15,
    borderRadius: 5,
    marginBottom: 5,
    alignItems: "center",
  },
  producto: { fontSize: 18, color: "#000" },
  botonEliminar: { backgroundColor: "red", padding: 5, borderRadius: 5 },
  eliminarTexto: { color: "white", fontWeight: "bold" },
  botonFoto: { backgroundColor: "#007bff", padding: 15, borderRadius: 10, alignItems: "center", marginTop: 20 },
});
