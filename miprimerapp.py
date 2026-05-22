import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class DatabaseManager:
    def __init__(self):
        # Conexión y creación de tabla con 3 campos + ID
        self.conn = sqlite3.connect("usuarios_edad.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                edad INTEGER,
                categoria TEXT
            )
        ''')
        self.conn.commit()

    def registrar_persona(self, nombre, edad):
        # Lógica para definir la categoría
        if edad < 13:
            categoria = "Niño/a"
        elif edad < 18:
            categoria = "Adolescente"
        elif edad < 65:
            categoria = "Adulto/a"
        else:
            categoria = "Adulto Mayor"

        # Guardar en la base de datos
        self.cursor.execute(
            "INSERT INTO registros (nombre, edad, categoria) VALUES (?, ?, ?)",
            (nombre, edad, categoria)
        )
        self.conn.commit()
        return categoria

class MiLayout(BoxLayout):
    def guardar_y_mostrar(self):
        nombre = self.ids.input_nombre.text
        edad_texto = self.ids.input_edad.text

        if nombre and edad_texto:
            try:
                edad = int(edad_texto)
                # Llamamos a la lógica de la DB
                cat = app.db.registrar_persona(nombre, edad)
                
                # Actualizamos la interfaz
                self.ids.label_resultado.text = f"Nombre: {nombre}\nCategoría: {cat}"
                
                # Limpiar campos
                self.ids.input_nombre.text = ""
                self.ids.input_edad.text = ""
            except ValueError:
                self.ids.label_resultado.text = "Error: Pon una edad válida"

class RegistroApp(App):
    def build(self):
        self.db = DatabaseManager()
        return MiLayout()

if __name__ == "__main__":
    app = RegistroApp()
    app.run()