from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# Fijamos un tamaño de ventana tipo móvil para el diseño
Window.size = (400, 600)


class BotonRedondeado(Button):
    """Un botón personalizado con bordes redondeados y colores modernos."""

    def __init__(self, color_fondo=(0.92, 0.95, 0.98, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Ocultamos el fondo gris por defecto
        self.color = (0.1, 0.1, 0.1, 1)  # Texto oscuro para buen contraste
        self.bold = True
        self.color_fondo = color_fondo
        self.bind(pos=self.actualizar_canvas, size=self.actualizar_canvas)

    def actualizar_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color_fondo)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])


class PantallaInicio(Screen):
    """Pantalla de bienvenida con el título, imagen e integrantes."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=15)

        # Título de la App
        titulo = Label(
            text="Curso de Español\nInteractivo",
            font_size=26,
            bold=True,
            halign="center",
            color=(0.15, 0.15, 0.2, 1),
            size_hint_y=0.15
        )
        layout_principal.add_widget(titulo)

        # ==========================================
        # ESPACIO PARA TU IMAGEN
        # ==========================================
        # Cambia 'logo_curso.png' por el nombre de tu archivo de imagen.
        # Si aún no tienes la imagen, Kivy mostrará un cuadro blanco/indicador.
        self.imagen_presentacion = Image(
            source='cecytem.jpg',
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=0.25
        )
        layout_principal.add_widget(self.imagen_presentacion)

        # Bloque de Integrantes de Equipo
        bloque_integrantes = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.35)

        subtitulo = Label(
            text="Integrantes del Equipo:",
            font_size=16,
            bold=True,
            color=(0.4, 0.4, 0.4, 1),
            halign="left"
        )
        subtitulo.bind(size=subtitulo.setter('text_size'))
        bloque_integrantes.add_widget(subtitulo)

        integrantes = [
            "FRANCO CRUZ GABRIEL NL.9",
            "FLORES CALZADA MOISES HAZEL NL.8",
            "CARMEN OROPEZA BRAYAN NL.2"
        ]

        for integrante in integrantes:
            lbl = Label(
                text=integrante,
                font_size=14,
                color=(0.2, 0.2, 0.2, 1),
                halign="left"
            )
            lbl.bind(size=lbl.setter('text_size'))
            bloque_integrantes.add_widget(lbl)

        layout_principal.add_widget(bloque_integrantes)

        # Botón para Iniciar
        btn_iniciar = BotonRedondeado(
            text="CAMPAMENTO DE PREGUNTAS",
            font_size=16,
            color_fondo=(0.22, 0.58, 0.93, 1),
            size_hint_y=0.12
        )
        btn_iniciar.color = (1, 1, 1, 1)
        btn_iniciar.bind(on_press=self.ir_a_preguntas)

        layout_principal.add_widget(btn_iniciar)
        self.add_widget(layout_principal)

    def ir_a_preguntas(self, instance):
        self.manager.current = 'juego'


class PantallaJuego(Screen):
    """Pantalla dinámica con 10 preguntas de dificultad progresiva."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Banco de 10 preguntas ordenadas por dificultad creciente
        self.preguntas = [
            # Nivel 1: Vocabulario básico
            {"pregunta": "1. ¿Cómo se dice 'Book' en español?", "opciones": ["Mesa", "Libro", "Lápiz"],
             "correcta": "Libro"},
            # Nivel 2: Identificación de categorías gramaticales básicas
            {"pregunta": "2. Identifica el sustantivo en:\n'El perro corre rápido'",
             "opciones": ["Corre", "Rápido", "Perro"], "correcta": "Perro"},
            # Nivel 3: Acentuación básica
            {"pregunta": "3. ¿Cuál palabra lleva acento ortográfico (tilde)?", "opciones": ["Cancion", "Mesa", "Gato"],
             "correcta": "Cancion"},
            # Nivel 4: Clasificación de palabras por su acentuación
            {"pregunta": "4. La palabra 'árbol' es un ejemplo de palabra:",
             "opciones": ["Aguda", "Grave / Llana", "Esdrújula"], "correcta": "Grave / Llana"},
            # Nivel 5: Ortografía (Uso de grafías b/v)
            {"pregunta": "5. Elige la opción redactada correctamente:",
             "opciones": ["Él iba a cambiar de rumbo", "Él hiba a cambar de rumbo", "Él iba a camviar de rumbo"],
             "correcta": "Él iba a cambiar de rumbo"},
            # Nivel 6: Identificación del Sujeto en oraciones complejas
            {"pregunta": "6. ¿Cuál es el sujeto en:\n'Ayer por la tarde, ellos ganaron el partido'?",
             "opciones": ["Ayer por la tarde", "El partido", "Ellos"], "correcta": "Ellos"},
            # Nivel 7: Nexos y conectores lógicos
            {"pregunta": "7. En 'Estudió mucho, pero no aprobó', el conector 'pero' es:",
             "opciones": ["Adversativo", "Causal", "Copulativo"], "correcta": "Adversativo"},
            # Nivel 8: Vicios del lenguaje
            {"pregunta": "8. ¿Qué vicio se comete en la frase:\n'Sube para arriba'?",
             "opciones": ["Cacofonía", "Pleonasmo / Redundancia", "Solecismo"], "correcta": "Pleonasmo / Redundancia"},
            # Nivel 9: Modificadores del predicado (Objeto Directo)
            {"pregunta": "9. ¿Cuál es el Objeto Directo en:\n'Mariana escribió una carta ayer'?",
             "opciones": ["Una carta", "Mariana", "Ayer"], "correcta": "Una carta"},
            # Nivel 10: Sintaxis avanzada (Oraciones compuestas)
            {"pregunta": "10. 'Cuando llegues, llámame'.\n¿Qué tipo de oración subordinada es?",
             "opciones": ["Sustantiva", "Adjetiva", "Adverbial de tiempo"], "correcta": "Adverbial de tiempo"}
        ]

        self.indice_actual = 0
        self.buenas = 0
        self.malas = 0

        # Layout base
        self.layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=20)

        # Marcador en tiempo real durante el juego
        self.marcador_label = Label(
            text="Correctas: 0 | Incorrectas: 0",
            font_size=14,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.08
        )
        self.layout_principal.add_widget(self.marcador_label)

        # Label de la Pregunta
        self.pregunta_label = Label(
            text="",
            font_size=20,
            bold=True,
            color=(0.15, 0.15, 0.2, 1),
            size_hint_y=0.22,
            halign="center"
        )
        self.pregunta_label.bind(size=self.pregunta_label.setter('text_size'))
        self.layout_principal.add_widget(self.pregunta_label)

        # Contenedor para botones de opciones
        self.layout_opciones = BoxLayout(orientation='vertical', spacing=12, size_hint_y=0.52)
        self.layout_principal.add_widget(self.layout_opciones)

        # Label de Retroalimentación
        self.feedback_label = Label(text="", font_size=18, bold=True, size_hint_y=0.18)
        self.layout_principal.add_widget(self.feedback_label)

        self.add_widget(self.layout_principal)
        self.cargar_pregunta()

    def cargar_pregunta(self):
        self.feedback_label.text = ""
        self.layout_opciones.clear_widgets()

        if self.indice_actual < len(self.preguntas):
            # Actualizamos el marcador superior
            self.marcador_label.text = f"Correctas: {self.buenas} | Incorrectas: {self.malas}"

            datos_pregunta = self.preguntas[self.indice_actual]
            self.pregunta_label.text = datos_pregunta["pregunta"]

            for opcion in datos_pregunta["opciones"]:
                btn = BotonRedondeado(text=opcion, font_size=16)
                btn.bind(on_press=self.verificar_respuesta)
                self.layout_opciones.add_widget(btn)
        else:
            # Fin del juego: Mostramos resultados y el botón para regresar
            self.marcador_label.text = ""
            self.pregunta_label.text = f"¡Campamento Terminado! 🎉\n\nResultados finales:"

            # Label con el desglose de puntos
            lbl_puntos = Label(
                text=f"✅ Buenas: {self.buenas}\n❌ Malas: {self.malas}",
                font_size=22,
                bold=True,
                color=(0.2, 0.2, 0.3, 1),
                halign="center"
            )
            self.layout_opciones.add_widget(lbl_puntos)

            # Botón para regresar al inicio (Reinicia el estado)
            btn_volver = BotonRedondeado(text="Regresar al Inicio", font_size=18, color_fondo=(0.2, 0.2, 0.2, 1))
            btn_volver.color = (1, 1, 1, 1)
            btn_volver.bind(on_press=self.reiniciar_todo)
            self.layout_opciones.add_widget(btn_volver)

    def verificar_respuesta(self, instance):
        correcta = self.preguntas[self.indice_actual]["correcta"]

        if instance.text == correcta:
            self.buenas += 1
            self.feedback_label.text = "¡Correcto! 🎉"
            self.feedback_label.color = (0.15, 0.68, 0.37, 1)  # Verde
            self.layout_opciones.disabled = True
            Clock.schedule_once(self.avanzar_pregunta, 1.2)
        else:
            self.malas += 1
            self.feedback_label.text = f"Inténtalo de nuevo ❌\n(Era: {correcta})"
            self.feedback_label.color = (0.90, 0.30, 0.26, 1)  # Rojo
            self.layout_opciones.disabled = True
            Clock.schedule_once(self.avanzar_pregunta, 1.8)

    def avanzar_pregunta(self, dt):
        self.layout_opciones.disabled = False
        self.indice_actual += 1
        self.cargar_pregunta()

    def reiniciar_todo(self, instance):
        self.indice_actual = 0
        self.buenas = 0
        self.malas = 0
        self.cargar_pregunta()
        self.manager.current = 'inicio'


class CursoEspanolApp(App):
    def build(self):
        Window.clearcolor = (0.98, 0.98, 0.98, 1)

        sm = ScreenManager()
        sm.add_widget(PantallaInicio(name='inicio'))
        sm.add_widget(PantallaJuego(name='juego'))

        return sm


if __name__ == "__main__":
    CursoEspanolApp().run()