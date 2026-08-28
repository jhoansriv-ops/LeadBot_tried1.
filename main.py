from database.conexion import Conexion

if __name__ == "__main__":
    print("Iniciando prueba de conexión de LeadBot...")
    try:
        with Conexion() as cn:
            if cn.is_connected():
                print("¡Conexión exitosa a la base de datos MySQL!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")