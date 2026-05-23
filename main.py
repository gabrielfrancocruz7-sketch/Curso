from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


class BotonRedondeado(Button):
    """Un botón personalizado con bordes redondeados y colores modernos."""

    def __init__(self, color_fondo=(0.92, 0.95, 0.98, 1), **kwargs):
        self.color_fondo = color_fondo
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  
        self.color = (0.1, 0.1, 0.1, 1)       
        self.bold = True
        self.bind(pos=self.actualizar_canvas, size=self.actualizar_canvas)

    def actualizar_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color_fondo)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])


class PantallaInicio(Screen):
    """Pantalla de bienvenida con el título e integrantes."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=20)

        # Título de la App
        titulo = Label(
            text="Curso de Espanol\nInteractivo",
            font_size=28,
            bold=True,
            halign="center",
            color=(0.15, 0.15, 0.2, 1),
            size_hint_y=0.25
        )
        layout_principal.add_widget(titulo)

        # Bloque de Integrantes de Equipo
        bloque_integrantes = BoxLayout(orientation='vertical', spacing=8, size_hint_y=0.50)

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
            "CARMEN OROPEZA BRAYAN NL.2",
            "Jimenez Hernandez Lizette Gabriela NL.18",
            "Hernandez Gonzalez Lizbeth NL.16"
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
            size_hint_y=0.15
        )
        btn_iniciar.color = (1, 1, 1, 1)
        btn_iniciar.bind(on_press=self.ir_a_preguntas)

        layout_principal.add_widget(btn_iniciar)
        self.add_widget(layout_principal)

    def ir_a_preguntas(self, instance):
        self.manager.current = 'juego'


class PantallaJuego(Screen):
    """Pantalla dinámica con 20 preguntas."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Banco de preguntas sin caracteres especiales conflictivos
        self.preguntas = [
            {"pregunta": "1. ¿Como se dice 'Book' en espanol?", "opciones": ["Mesa", "Libro", "Lapiz"], "correcta": "Libro"},
            {"pregunta": "2. Identifica el sustantivo en:\n'El perro corre rapido'", "opciones": ["Corre", "Rapido", "Perro"], "correcta": "Perro"},
            {"pregunta": "3. ¿Cual palabra lleva acento ortografico (tilde)?", "opciones": ["Cancion", "Mesa", "Gato"], "correcta": "Cancion"},
            {"pregunta": "4. La palabra 'arbol' es un ejemplo de palabra:", "opciones": ["Aguda", "Grave / Llana", "Esdrujula"], "correcta": "Grave / Llana"},
            {"pregunta": "5. Elige la opcion redactada correctamente:", "opciones": ["El iba a cambiar de rumbo", "El hiba a cambar de rumbo", "El iba a camviar de rumbo"], "correcta": "El iba a cambiar de rumbo"},
            {"pregunta": "6. ¿Cual es el sujeto en:\n'Ayer por la tarde, ellos ganaron el partido'?", "opciones": ["Ayer por la tarde", "El partido", "Ellos"], "correcta": "Ellos"},
            {"pregunta": "7. En 'Estudio mucho, pero no aprobo', el conector 'pero' es:", "opciones": ["Adversativo", "Causal", "Copulativo"], "correcta": "Adversativo"},
            {"pregunta": "8. ¿Que vicio se comete en la frase:\n'Sube para arriba'?", "opciones": ["Cacofonia", "Pleonasmo / Redundancia", "Solecismo"], "correcta": "Pleonasmo / Redundancia"},
            {"pregunta": "9. ¿Cual es el Objeto Directo en:\n'Mariana escribio una carta ayer'?", "opciones": ["Una carta", "Mariana", "Ayer"], "correcta": "Una carta"},
            {"pregunta": "10. 'Cuando llegues, llamame'.\n¿Que tipo de oracion subordinada es?", "opciones": ["Sustantiva", "Adjetiva", "Adverbial de tiempo"], "correcta": "Adverbial de tiempo"},
            {"pregunta": "11. ¿Cual es un sinonimo de 'feliz'?", "opciones": ["Triste", "Contento", "Enojado"], "correcta": "Contento"},
            {"pregunta": "12. ¿Cual es el antonimo de 'rapido'?", "opciones": ["Lento", "Grande", "Alto"], "correcta": "Lento"},
            {"pregunta": "13. ¿Que signo se usa para hacer una pregunta?", "opciones": ["?", ".", ","], "correcta": "?"},
            {"pregunta": "14. ¿Cual de las siguientes palabras es un verbo?", "opciones": ["Correr", "Mesa", "Bonito"], "correcta": "Correr"},
            {"pregunta": "15. En la oracion 'Maria lee un libro', ¿que esta leyendo Maria?", "opciones": ["Una mesa", "Un libro", "Una carta"], "correcta": "Un libro"},
            {"pregunta": "16. ¿Cual oracion esta escrita correctamente?", "opciones": ["mexico es un pais", "Mexico es un pais", "mexico Es un pais"], "correcta": "Mexico es un pais"},
            {"pregunta": "17. La palabra 'hermoso' es:", "opciones": ["Un sustantivo", "Un adjetivo", "Un verbo"], "correcta": "Un adjetivo"},
            {"pregunta": "18. ¿Que hace Juan en la oracion:\n'Juan juega futbol con sus amigos'?", "opciones": ["Correr", "Juega futbol", "Estudia"], "correcta": "Juega futbol"},
            {"pregunta": "19. ¿Cual palabra esta escrita correctamente?", "opciones": ["Hacer", "Aser", "Haser"], "correcta": "Hacer"},
            {"pregunta": "20. ¿Cuantas silabas tiene la palabra 'computadora'?", "opciones": ["3", "4", "5"], "correcta": "5"}
        ]

        self.indice_actual = 0
        self.buenas = 0
        self.malas = 0
        self.vidas = 3

        self.layout_principal = BoxLayout(orientation='vertical', padding=25, spacing=15)

        # Contenedor superior para el estatus (Vidas + Progreso)
        self.layout_estatus = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)

        self.vidas_label = Label(text="VIDAS: 3", font_size=16, color=(0.9, 0.2, 0.2, 1), halign="left")
        self.vidas_label.bind(size=self.vidas_label.setter('text_size'))

        self.progreso_label = Label(text="Progreso: 0%", font_size=14, color=(0.3, 0.3, 0.3, 1), halign="right")
        self.progreso_label.bind(size=self.progreso_label.setter('text_size'))

        self.layout_estatus.add_widget(self.vidas_label)
        self.layout_estatus.add_widget(self.progreso_label)
        self.layout_principal.add_widget(self.layout_estatus)

        # Marcador en tiempo real
        self.marcador_label = Label(
            text="Correctas: 0 | Incorrectas: 0",
            font_size=14,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.06
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
        self.layout_opciones = BoxLayout(orientation='vertical', spacing=12, size_hint_y=0.46)
        self.layout_principal.add_widget(self.layout_opciones)

        # Label de Retroalimentación
        self.feedback_label = Label(text="", font_size=18, bold=True, size_hint_y=0.18)
        self.layout_principal.add_widget(self.feedback_label)

        self.add_widget(self.layout_principal)
        self.cargar_pregunta()

    def cargar_pregunta(self):
        self.feedback_label.text = ""
        self.layout_opciones.clear_widgets()

        self.vidas_label.text = f"VIDAS: {self.vidas}" if self.vidas > 0 else "GAME OVER"

        porcentaje = int((self.indice_actual / len(self.preguntas)) * 100)
        self.progreso_label.text = f"Progreso: {porcentaje}%"

        if self.vidas <= 0:
            self.terminar_juego("Te quedaste sin vidas... \nIntentalo de nuevo.")
            return

        if self.indice_actual < len(self.preguntas):
            self.marcador_label.text = f"Correctas: {self.buenas} | Incorrectas: {self.malas}"

            datos_pregunta = self.preguntas[self.indice_actual]
            self.pregunta_label.text = datos_pregunta["pregunta"]

            for opcion in datos_pregunta["opciones"]:
                btn = BotonRedondeado(text=opcion, font_size=16)
                btn.bind(on_press=self.verificar_respuesta)
                self.layout_opciones.add_widget(btn)
        else:
            self.terminar_juego("Campamento Terminado! \n\nResultados finales:")

    def verificar_respuesta(self, instance):
        correcta = self.preguntas[self.indice_actual]["correcta"]

        if instance.text == correcta:
            self.buenas += 1
            self.feedback_label.text = "Correcto!"
            self.feedback_label.color = (0.15, 0.68, 0.37, 1)  
            self.layout_opciones.disabled = True
            Clock.schedule_once(self.avanzar_pregunta, 1.2)
        else:
            self.malas += 1
            self.vidas -= 1  
            self.feedback_label.text = f"Incorrecto\n(Era: {correcta})"
            self.feedback_label.color = (0.90, 0.30, 0.26, 1)  
            self.layout_opciones.disabled = True
            Clock.schedule_once(self.avanzar_pregunta, 1.8)

    def avanzar_pregunta(self, dt):
        self.layout_opciones.disabled = False
        self.indice_actual += 1
        self.cargar_pregunta()

    def terminar_juego(self, mensaje_final):
        self.marcador_label.text = ""
        self.pregunta_label.text = mensaje_final

        lbl_puntos = Label(
            text=f"Buenas: {self.buenas}\nMalas: {self.malas}",
            font_size=22,
            bold=True,
            color=(0.2, 0.2, 0.3, 1),
            halign="center"
        )
        self.layout_opciones.add_widget(lbl_puntos)

        btn_volver = BotonRedondeado(text="Regresar al Inicio", font_size=18, color_fondo=(0.2, 0.2, 0.2, 1))
        btn_volver.color = (1, 1, 1, 1)
        btn_volver.bind(on_press=self.reiniciar_todo)
        self.layout_opciones.add_widget(btn_volver)

    def reiniciar_todo(self, instance):
        self.indice_actual = 0
        self.buenas = 0
        self.malas = 0
        self.vidas = 3  
        self.cargar_pregunta()
        self.manager.current = 'inicio'


class MyApp(App):  
    def build(self):
        # Configuramos el tamaño aquí dentro para evitar errores de carga en hilos gráficos
        Window.size = (400, 600)
        Window.clearcolor = (0.98, 0.98, 0.98, 1)

        sm = ScreenManager()
        sm.add_widget(PantallaInicio(name='inicio'))
        sm.add_widget(PantallaJuego(name='juego'))

        return sm


if __name__ == "__main__":
    MyApp().run()

    CampamentoDelSaber().run()
