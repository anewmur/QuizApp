from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.properties import ListProperty, NumericProperty


class Theme:
    # --- Палитра XXI века (Пастельные тона для черного текста) ---
    BG_MILK = [0.92, 0.92, 0.90, 1]
    BG_EXPLANATION = [0.88, 0.94, 1.0, 1]

    ACCENT_PRIMARY = [0.1, 0.4, 0.8, 1]

    # Цвета текста
    TEXT_TITLE = [0, 0, 0, 1]
    TEXT_MAIN = [0.1, 0.1, 0.1, 1]
    TEXT_LIGHT = [1, 1, 1, 1]
    TEXT_DIM = [0.4, 0.4, 0.4, 1]

    # Мягкие цвета полей
    STATE_SUCCESS = [0.75, 0.95, 0.8, 1]  # Пастельный зеленый
    STATE_ERROR = [1.0, 0.85, 0.85, 1]  # Пастельный красный
    STATE_SELECTED = [0.85, 0.92, 1.0, 1]  # Пастельный синий
    STATE_NORMAL = [1, 1, 1, 1]  # Белый

    # --- Размеры ---
    RADIUS_LG = dp(20)
    RADIUS_SM = dp(10)
    PADDING_OUTER = dp(24)
    PADDING_INNER = dp(18)
    SPACING = dp(14)
    TITLE_FONT_SIZE = dp(28)
    NORMAL_FONT_SIZE = dp(17)
    BTN_HEIGHT = dp(58)


class ModernLabel(Label):
    def __init__(self, is_title=False, color=None, **kwargs):
        if color is None:
            color = Theme.TEXT_TITLE if is_title else Theme.TEXT_MAIN
        super().__init__(**kwargs)
        self.color = color
        self.font_size = Theme.TITLE_FONT_SIZE if is_title else Theme.NORMAL_FONT_SIZE
        self.bold = is_title
        self.halign = 'center'
        self.valign = 'middle'
        self.size_hint_y = None
        self.bind(size=lambda l, s: setattr(l, 'text_size', s))


class ModernButton(Button):
    def __init__(self, text, is_accent=False, **kwargs):
        self.is_accent = is_accent
        super().__init__(text=text, **kwargs)
        self.size_hint_y = None
        self.height = Theme.BTN_HEIGHT

        # Отключаем дефолтное поведение Kivy
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0, 0, 0, 0]  # <-- ВОТ ЭТОТ ФИКС! Делаем слой прозрачным

        self.color = Theme.TEXT_LIGHT if is_accent else Theme.TEXT_TITLE
        self.bold = True
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_accent:
                Color(*Theme.ACCENT_PRIMARY)
            else:
                Color(0, 0, 0, 0.05)
                RoundedRectangle(pos=(self.x + dp(1), self.y - dp(2)), size=self.size, radius=[Theme.RADIUS_SM])
                Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.RADIUS_SM])
            if not self.is_accent:
                Color(0.8, 0.8, 0.8, 1)
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, Theme.RADIUS_SM), width=1)


class OptionButton(ModernButton):
    current_state_color = ListProperty(Theme.STATE_NORMAL)
    is_answer_locked = NumericProperty(0)

    def __init__(self, text, **kwargs):
        super().__init__(text=text, is_accent=False, **kwargs)
        self.color = Theme.TEXT_MAIN
        self.bold = False
        self.halign = 'left'
        self.valign = 'middle'  # <-- ЯВНО УКАЗЫВАЕМ ВЕРТИКАЛЬНОЕ ЦЕНТРИРОВАНИЕ
        self.padding = (dp(15), 0)
        self.bind(size=self._update_text_size, current_state_color=self._update_colors)

    def _update_text_size(self, instance, value):
        # Привязываем текстовый блок к размеру кнопки (с учетом отступов)
        self.text_size = (value[0] - dp(30), value[1])

    def _update_colors(self, *args):
        self._update_canvas()

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.current_state_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.RADIUS_SM])
            Color(0.85, 0.85, 0.85, 1)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, Theme.RADIUS_SM), width=1)

    def on_press(self):
        if self.is_answer_locked == 0:
            self.current_state_color = Theme.STATE_SELECTED
        super().on_press()

class ExplanationBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = Theme.PADDING_INNER
        self.size_hint_y = None
        self.opacity = 0
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Theme.BG_EXPLANATION)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.RADIUS_SM])


class CardLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = Theme.PADDING_INNER
        self.spacing = Theme.SPACING
        self.size_hint_x = 0.92
        self.pos_hint = {'center_x': 0.5}
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            RoundedRectangle(pos=(self.x + dp(4), self.y - dp(6)), size=self.size, radius=[Theme.RADIUS_LG])
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[Theme.RADIUS_LG])