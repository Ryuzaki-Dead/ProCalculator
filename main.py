import math
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

Window.clearcolor = (0, 0, 0, 1)


# ---------------- iPhone Style Button ----------------
class ModernButton(Button):
    def __init__(self, role="number", **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        if role == "number":
            self.base_color = (0.2, 0.2, 0.2, 1)
        elif role == "function":
            self.base_color = (0.6, 0.6, 0.6, 1)
        elif role == "operator":
            self.base_color = (1, 0.55, 0, 1)
        else:
            self.base_color = (0.2, 0.2, 0.2, 1)

        with self.canvas.before:
            self.color_instruction = Color(*self.base_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[100])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        Animation(rgba=(1, 1, 1, 1), duration=0.05).start(self.color_instruction)

    def on_release(self):
        Animation(rgba=self.base_color, duration=0.1).start(self.color_instruction)


# ---------------- Splash Screen ----------------
class SplashScreen(Screen):

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", spacing=15)

        with self.canvas.before:
            Color(0.06, 0.06, 0.08, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=Window.size)

        self.bind(size=self.update_bg, pos=self.update_bg)

        self.title = Label(
            text="[b]Pro Calculator[/b]",
            markup=True,
            font_size="46sp",
            opacity=0
        )

        self.subtitle = Label(
            text="[color=888888]Made by Ryuzaki[/color]",
            markup=True,
            font_size="18sp",
            opacity=0
        )

        layout.add_widget(Label())
        layout.add_widget(self.title)
        layout.add_widget(self.subtitle)
        layout.add_widget(Label())

        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_enter(self):
        Animation(opacity=1, duration=1.2).start(self.title)
        Animation(opacity=1, duration=2).start(self.subtitle)
        Clock.schedule_once(self.go_to_calc, 3)

    def go_to_calc(self, *args):
        self.manager.transition = SlideTransition(direction="left", duration=0.3)
        self.manager.current = "calc"


# ---------------- iPhone Calculator Screen ----------------
class CalculatorScreen(Screen):

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", spacing=15, padding=15)

        self.display = TextInput(
            multiline=False,
            readonly=True,
            font_size="60sp",
            halign="right",
            size_hint=(1, 0.3),
            foreground_color=(1,1,1,1),
            background_color=(0,0,0,1)
        )
        layout.add_widget(self.display)

        grid = GridLayout(cols=4, spacing=12)

        buttons = [
            ('C','function'), ('+/-','function'), ('%','function'), ('/','operator'),
            ('7','number'), ('8','number'), ('9','number'), ('*','operator'),
            ('4','number'), ('5','number'), ('6','number'), ('-','operator'),
            ('1','number'), ('2','number'), ('3','number'), ('+','operator'),
            ('0','number'), ('.','number'), ('=','operator')
        ]

        for text, role in buttons:
            btn = ModernButton(text=text, role=role, font_size="28sp")
            btn.bind(on_press=self.on_click)
            grid.add_widget(btn)

        layout.add_widget(grid)
        self.add_widget(layout)

    def safe_eval(self, expression):
        return eval(expression, {"__builtins__": None}, {})

    def on_click(self, instance):
        text = instance.text

        if text == "C":
            self.display.text = ""

        elif text == "=":
            try:
                result = str(self.safe_eval(self.display.text))
                self.display.text = result
            except:
                self.display.text = "Error"

        elif text == "+/-":
            if self.display.text:
                if self.display.text.startswith("-"):
                    self.display.text = self.display.text[1:]
                else:
                    self.display.text = "-" + self.display.text

        elif text == "%":
            try:
                value = float(self.display.text)
                self.display.text = str(value / 100)
            except:
                self.display.text = "Error"

        else:
            self.display.text += text


# ---------------- Converter Screen (unchanged) ----------------
class ConverterScreen(Screen):

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.input_box = TextInput(
            multiline=False,
            hint_text="Enter value",
            background_color=(0.12,0.12,0.15,1),
            foreground_color=(1,1,1,1)
        )
        layout.add_widget(self.input_box)

        self.result = Label(font_size="20sp")
        layout.add_widget(self.result)

        back = ModernButton(text="Back", role="function")
        back.bind(on_press=self.go_back)
        layout.add_widget(back)

        self.add_widget(layout)

    def go_back(self, *args):
        self.manager.transition = SlideTransition(direction="right", duration=0.3)
        self.manager.current = "calc"


# ---------------- Main App ----------------
class ProCalcApp(App):
    def build(self):
        sm = ScreenManager()

        splash = SplashScreen(name="splash")
        splash.build_ui()

        calc = CalculatorScreen(name="calc")
        calc.build_ui()

        conv = ConverterScreen(name="converter")
        conv.build_ui()

        sm.add_widget(splash)
        sm.add_widget(calc)
        sm.add_widget(conv)

        return sm


if __name__ == "__main__":
    ProCalcApp().run()