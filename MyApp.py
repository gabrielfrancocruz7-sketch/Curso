from kivymd.uix.boxlayout import MDBoxLayout

class MyApp(MDApp):
    def build(self):
        # Creamos un contenedor vertical con espacio (spacing) entre sus elementos
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            padding="40dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None),
            height="200dp"
        )

        # Campo de texto para ingresar el nombre
        self.campo_nombre = MDTextField(
            hint_text="Escribe tu nombre aquí",
            helper_text="¡No lo dejes vacío!",
            helper_text_mode="on_error"
        )

        # Tu botón original con una acción vinculada (on_release)
        self.boton = MDRectangleFlatButton(
            text="¡Salúdame!",
            pos_hint={"center_x": 0.5},
            on_release=self.saludar_usuario
        )

        # Agregamos los componentes al contenedor
        layout.add_widget(self.campo_nombre)
        layout.add_widget(self.boton)

        return layout

    def saludar_usuario(self, instance):
        # Obtenemos el texto que el usuario escribió
        nombre_ingresado = self.campo_nombre.text.strip()

        # Si el usuario escribió algo, lo saludamos; si no, le pedimos su nombre
        if nombre_ingresado:
            self.boton.text = f"¡Hola, {nombre_ingresado}!"
        else:
            self.campo_nombre.error = True

if __name__ == "__main__":
    MyApp().run()
