import sqlite3

# Ajusta el nombre si tu base de datos se llama diferente
DB_NAME = 'abarrotes_don_chuy.db'

print(f"Conectando a {DB_NAME}...")
conexion = sqlite3.connect(DB_NAME)
cursor = conexion.cursor()

try:
    # Agrega la columna 'palabra_clave' a la tabla 'usuario'
    cursor.execute("ALTER TABLE usuario ADD COLUMN palabra_clave VARCHAR(100) DEFAULT 'sin_clave'")
    conexion.commit()
    print("¡Éxito! La columna 'palabra_clave' ha sido agregada.")
except sqlite3.OperationalError as e:
    print(f"Aviso: {e}")
    print("Probablemente la columna ya existía. No se hicieron cambios.")
finally:
    conexion.close()