import sqlite3
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder

class MainScreen(MDScreen):
    def process_data(self):
        # Obtener textos de los inputs
        name = self.ids.name_input.text.strip()
        age_text = self.ids.age_input.text.strip()
        
        # Validación de campos vacíos
        if not name or not age_text:
            self.show_error("Todos los campos son obligatorios")
            return
        
        try:
            # Convertir edad y obtener categoría
            age = int(age_text)
            category = self.get_category(age)

            # --- PARTE CLAVE: Almacenamiento en DB ---
            self.save_to_db(name, age, category)
            
            # Cambiar a la pantalla de resultados y mostrar datos
            app = MDApp.get_running_app()
            result_screen = app.root.get_screen("result")
            result_screen.ids.result_label.text = (
                f"¡Registro Exitoso!\n\n"
                f"Nombre: {name}\n"
                f"Edad: {age}\n"
                f"Categoría: {category}"
            )
            
            app.root.current = "result"
            
            # Limpiar los campos después de guardar
            self.ids.name_input.text = ""
            self.ids.age_input.text = ""
            
        except ValueError:
            self.show_error("La edad debe ser un número válido")

    def get_category(self, age):
        if age < 13: return "Niño"
        elif age < 18: return "Adolescente"
        elif age < 60: return "Adulto"
        else: return "Adulto Mayor"

    def save_to_db(self, name, age, category):
        try:
            # Conectar a la base de datos (se crea si no existe)
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()
            
            # Insertar los datos
            cursor.execute(
                "INSERT INTO usuarios (nombre, edad, categoria) VALUES (?, ?, ?)",
                (name, age, category)
            )
            
            conn.commit()
            conn.close()
            print(f"Datos guardados: {name}, {age}, {category}") # Log en consola
        except Exception as e:
            self.show_error(f"Error de base de datos: {e}")

    def show_error(self, message):
        dialog = MDDialog(
            text=message, 
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class ResultScreen(MDScreen):
    pass

KV_DESIGN = '''
MDScreenManager:
    MainScreen:
    ResultScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"
        
        MDLabel:
            text: "Registro en Base de Datos"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Primary"
            
        MDTextField:
            id: name_input
            hint_text: "Nombre completo"
            mode: "rectangle"
            icon_right: "account"
            
        MDTextField:
            id: age_input
            hint_text: "Edad"
            input_filter: "int"
            mode: "rectangle"
            icon_right: "numeric"
            
        MDRaisedButton:
            text: "GUARDAR EN SQLITE"
            pos_hint: {"center_x": .5}
            size_hint_x: .8
            on_release: root.process_data()

<ResultScreen>:
    name: "result"
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"
        
        MDLabel:
            id: result_label
            halign: "center"
            font_style: "H5"
            
        MDRaisedButton:
            text: "VOLVER AL REGISTRO"
            pos_hint: {"center_x": .5}
            on_release: app.root.current = "main"
'''

class UserApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.init_db() # Crear la tabla al iniciar
        return Builder.load_string(KV_DESIGN)

    def init_db(self):
        # Esta función asegura que la tabla exista antes de usar la App
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                categoria TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

if __name__ == "__main__":
    UserApp().run()