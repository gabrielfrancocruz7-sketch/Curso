from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

class MyApp(MDApp):
    def build(self):
        # Pantalla principal
        screen = MDScreen()

        # Configuración del Menú Desplegable
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Opción {i}",
                "on_release": lambda x=f"Opción {i}": self.menu_callback(x),
            } for i in range(1, 4)
        ]
        
        self.menu = MDDropdownMenu(
            items=self.menu_items,
            width_mult=4,
        )

        # Barra de herramientas (TopAppBar)
        # Nota: left_action_items recibe [["icono", callback]]
        toolbar = MDTopAppBar(
            title="Mi aplicación",
            elevation=4,
            pos_hint={"top": 1},
            left_action_items=[["menu", lambda x: self.menu.open(x)]],
            right_action_items=[["dots-vertical", lambda x: print("Ajustes")]]
        )

        # Contenido de la pantalla
        label = MDLabel(
            text="Bienvenido a mi aplicación",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # Agregar widgets a la pantalla
        screen.add_widget(toolbar)
        screen.add_widget(label)

        return screen

    def menu_callback(self, text_item):
        print(f"Hiciste clic en: {text_item}")
        self.menu.dismiss()

if __name__ == "__main__":
    MyApp().run()