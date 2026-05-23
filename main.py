from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

Window.size = (400, 700)

# Fondo pastel bonito
Window.clearcolor = (0.90, 0.96, 0.95, 1)


# =====================================================
# BOTÓN PERSONALIZADO
# =====================================================

class BotonBonito(Button):

    def __init__(self, color_fondo=(0.65, 0.85, 0.80, 1), **kwargs):
        super().__init__(**kwargs)

        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.font_size = 17
        self.color_fondo = color_fondo

        self.bind(pos=self.actualizar_canvas)
        self.bind(size=self.actualizar_canvas)

    def actualizar_canvas(self, *args):

        self.canvas.before.clear()

        with self.canvas.before:

            Color(*self.color_fondo)

            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[35]
            )


# =====================================================
# PANTALLA DE INICIO
# =====================================================

class PantallaInicio(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        # TÍTULO
        titulo = Label(
            text="🏕️ CAMPAMENTO\nDEL SABER 📚",
            font_size=30,
            bold=True,
            halign="center",
            color=(0.15, 0.30, 0.35, 1),
            size_hint_y=0.18
        )

        layout.add_widget(titulo)

        # IMAGEN
        imagen = Image(
            source='cecytem.jpg',
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=0.30
        )

        layout.add_widget(imagen)

        # SUBTÍTULO
        subtitulo = Label(
            text="✨ Integrantes del equipo ✨",
            font_size=18,
            bold=True,
            color=(0.25, 0.25, 0.25, 1),
            size_hint_y=0.08
        )

        layout.add_widget(subtitulo)

        integrantes = [

            "👤 Franco Cruz Gabriel NL.9",
            "👤 Flores Calzada Moises Hazel NL.8",
            "👤 Carmen Oropeza Brayan NL.2",
            "👤 Jiménez Hernández Lizette Gabriela NL.18",
            "👤 Hernández González Lizbeth NL.16"

        ]

        for integrante in integrantes:

            lbl = Label(
                text=integrante,
                font_size=14,
                color=(0.20, 0.20, 0.20, 1),
                size_hint_y=0.05
            )

            layout.add_widget(lbl)

        # BOTÓN
        btn_iniciar = BotonBonito(
            text="🚀 INICIAR AVENTURA",
            color_fondo=(0.25, 0.60, 0.90, 1),
            size_hint_y=0.12
        )

        btn_iniciar.bind(on_press=self.ir_juego)

        layout.add_widget(btn_iniciar)

        self.add_widget(layout)

    def ir_juego(self, instance):

        self.manager.current = "juego"


# =====================================================
# PANTALLA DEL JUEGO
# =====================================================

class PantallaJuego(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.indice_actual = 0
        self.correctas = 0
        self.incorrectas = 0

        # =================================================
        # PREGUNTAS
        # =================================================

        self.preguntas = [

            {
                "pregunta": "📚 1. ¿Cómo se dice 'Book' en español?",
                "opciones": ["Mesa", "Libro", "Lápiz"],
                "correcta": "Libro"
            },

            {
                "pregunta": "🐶 2. ¿Cuál es el sustantivo?\n'El perro corre rápido'",
                "opciones": ["Corre", "Perro", "Rápido"],
                "correcta": "Perro"
            },

            {
                "pregunta": "✏️ 3. ¿Cuál palabra lleva tilde?",
                "opciones": ["Canción", "Mesa", "Gato"],
                "correcta": "Canción"
            },

            {
                "pregunta": "⚡ 4. ¿Cuál es un sinónimo de feliz?",
                "opciones": ["Triste", "Contento", "Malo"],
                "correcta": "Contento"
            },

            {
                "pregunta": "🚗 5. ¿Cuál es el antónimo de rápido?",
                "opciones": ["Lento", "Grande", "Bonito"],
                "correcta": "Lento"
            },

            {
                "pregunta": "📝 6. ¿Cuál palabra está escrita correctamente?",
                "opciones": ["Hacer", "Aser", "Haser"],
                "correcta": "Hacer"
            },

            {
                "pregunta": "📖 7. ¿Qué está leyendo María?\n'María lee un libro'",
                "opciones": ["Una carta", "Un libro", "Una mesa"],
                "correcta": "Un libro"
            },

            {
                "pregunta": "🌎 8. ¿Cuál oración está correcta?",
                "opciones": [
                    "mexico es un país",
                    "México es un país",
                    "méxico Es un país"
                ],
                "correcta": "México es un país"
            },

            {
                "pregunta": "🎨 9. La palabra 'hermoso' es:",
                "opciones": ["Verbo", "Adjetivo", "Sustantivo"],
                "correcta": "Adjetivo"
            },

            {
                "pregunta": "💻 10. ¿Cuántas sílabas tiene 'computadora'?",
                "opciones": ["3", "4", "5"],
                "correcta": "5"
            }

        ]

        # =================================================
        # LAYOUT PRINCIPAL
        # =================================================

        self.layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        # MARCADOR
        self.lbl_marcador = Label(
            text="✅ 0 Correctas | ❌ 0 Incorrectas",
            font_size=15,
            bold=True,
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=0.07
        )

        self.layout.add_widget(self.lbl_marcador)

        # PROGRESO
        self.lbl_progreso = Label(
            text="Pregunta 1 de 10",
            font_size=14,
            bold=True,
            color=(0.1, 0.5, 0.5, 1),
            size_hint_y=0.05
        )

        self.layout.add_widget(self.lbl_progreso)

        # PREGUNTA
        self.lbl_pregunta = Label(
            text="",
            font_size=23,
            bold=True,
            halign="center",
            valign="middle",
            color=(0.1, 0.2, 0.25, 1),
            size_hint_y=0.22
        )

        self.lbl_pregunta.bind(
            size=self.lbl_pregunta.setter('text_size')
        )

        self.layout.add_widget(self.lbl_pregunta)

        # OPCIONES
        self.layout_opciones = BoxLayout(
            orientation='vertical',
            spacing=14,
            size_hint_y=0.45
        )

        self.layout.add_widget(self.layout_opciones)

        # FEEDBACK
        self.lbl_feedback = Label(
            text="",
            font_size=20,
            bold=True,
            size_hint_y=0.12
        )

        self.layout.add_widget(self.lbl_feedback)

        self.add_widget(self.layout)

        self.cargar_pregunta()

    # =================================================
    # CARGAR PREGUNTA
    # =================================================

    def cargar_pregunta(self):

        self.layout_opciones.clear_widgets()

        self.lbl_feedback.text = ""

        if self.indice_actual < len(self.preguntas):

            datos = self.preguntas[self.indice_actual]

            self.lbl_pregunta.text = datos["pregunta"]

            self.lbl_progreso.text = (
                f"⭐ Pregunta {self.indice_actual + 1} de {len(self.preguntas)}"
            )

            self.lbl_marcador.text = (
                f"✅ {self.correctas} Correctas | "
                f"❌ {self.incorrectas} Incorrectas"
            )

            for opcion in datos["opciones"]:

                btn = BotonBonito(
                    text=opcion,
                    color_fondo=(0.45, 0.75, 0.70, 1)
                )

                btn.bind(on_press=self.verificar_respuesta)

                self.layout_opciones.add_widget(btn)

        else:

            self.mostrar_resultados()

    # =================================================
    # VERIFICAR RESPUESTA
    # =================================================

    def verificar_respuesta(self, instance):

        respuesta_usuario = instance.text

        respuesta_correcta = (
            self.preguntas[self.indice_actual]["correcta"]
        )

        if respuesta_usuario == respuesta_correcta:

            self.correctas += 1

            self.lbl_feedback.text = "✅ ¡Correcto!"
            self.lbl_feedback.color = (0, 0.6, 0, 1)

        else:

            self.incorrectas += 1

            self.lbl_feedback.text = (
                f"❌ Incorrecto\nRespuesta: {respuesta_correcta}"
            )

            self.lbl_feedback.color = (1, 0, 0, 1)

        self.indice_actual += 1

        Clock.schedule_once(
            lambda dt: self.cargar_pregunta(),
            1.5
        )

    # =================================================
    # RESULTADOS
    # =================================================

    def mostrar_resultados(self):

        self.layout_opciones.clear_widgets()

        self.lbl_progreso.text = "🏁 Juego terminado"

        self.lbl_pregunta.text = "🎉 ¡CAMPAMENTO SUPERADO! 🎉"

        self.lbl_marcador.text = ""

        # NIVEL
        if self.correctas == 10:

            nivel = "👑 Nivel Maestro"

        elif self.correctas >= 7:

            nivel = "🔥 Nivel Avanzado"

        elif self.correctas >= 5:

            nivel = "⭐ Nivel Medio"

        else:

            nivel = "📚 Sigue practicando"

        self.lbl_feedback.text = (
            f"✅ Correctas: {self.correctas}\n"
            f"❌ Incorrectas: {self.incorrectas}\n\n"
            f"{nivel}"
        )

        self.lbl_feedback.color = (0.15, 0.3, 0.5, 1)

        # BOTÓN REINICIAR
        btn_reiniciar = BotonBonito(
            text="🔄 VOLVER A JUGAR",
            color_fondo=(0.20, 0.65, 0.45, 1),
            size_hint_y=None,
            height=60
        )

        btn_reiniciar.bind(on_press=self.reiniciar)

        self.layout_opciones.add_widget(btn_reiniciar)

    # =================================================
    # REINICIAR
    # =================================================

    def reiniciar(self, instance):

        self.indice_actual = 0
        self.correctas = 0
        self.incorrectas = 0

        self.cargar_pregunta()


# =====================================================
# APP PRINCIPAL
# =====================================================

class CampamentoDelSaber(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(PantallaInicio(name="inicio"))
        sm.add_widget(PantallaJuego(name="juego"))

        return sm


# =====================================================
# EJECUTAR APP
# =====================================================

if __name__ == "__main__":

    CampamentoDelSaber().run()
