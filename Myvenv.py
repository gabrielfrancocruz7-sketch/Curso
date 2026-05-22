from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar  # MDToolbar ahora se llama MDTopAppBar
from kivymd.uix.label import MDLabel

class MyApp(MDApp):
    def build(self):
        screen = Screen()

        # Menú
        menu = MDDropdownMenu()
        menu.items = [
            {"viewclass": "OneLineListItem", "text": "Opción 1"},
            {"viewclass": "OneLineListItem", "text": "Opción 2"},
            {"viewclass": "OneLineListItem", "text": "Opción 3"},
        ]

        # Barra de herramientas (MDTopAppBar)
        toolbar = MDTopAppBar(
            title="Mi aplicación",
            elevation=10,
            pos_hint={"top": 1},
        )
        toolbar.left_action_items = [["menu", lambda x: None]]

        # Pantalla de inicio
        home_screen = Screen()
        home_screen.add_widget(
            MDLabel(
                text="Bienvenido a mi aplicación",
                halign="center",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )

        # Agregar widgets a la pantalla principal
        screen.add_widget(home_screen)
        screen.add_widget(toolbar)

        return screen

if __name__ == "__main__":
    MyApp().run()