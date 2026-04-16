from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle


class Theme:
    # Цветовая палитра
    BG_COLOR = [0.12, 0.12, 0.12, 1]
    PRIMARY = [0.2, 0.6, 1, 1]  # Акцентный синий
    SUCCESS = [0.3, 0.8, 0.3, 1]  # Правильный ответ
    ERROR = [0.8, 0.3, 0.3, 1]  # Ошибка
    TEXT_MAIN = [0.95, 0.95, 0.95, 1]

    # Размеры
    PADDING = dp(15)
    SPACING = dp(10)
    BTN_HEIGHT = dp(48)
    TITLE_FONT_SIZE = dp(22)
    NORMAL_FONT_SIZE = dp(16)


class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = Theme.BTN_HEIGHT
        self.background_normal = ''  # Отключаем стандартный градиент Kivy
        self.background_color = Theme.PRIMARY
        self.font_size = Theme.NORMAL_FONT_SIZE


class StyledLabel(Label):
    def __init__(self, is_title=False, **kwargs):
        super().__init__(**kwargs)
        self.color = Theme.TEXT_MAIN
        self.font_size = Theme.TITLE_FONT_SIZE if is_title else Theme.NORMAL_FONT_SIZE
        self.size_hint_y = None
        self.height = dp(40)
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self._update_text_size)

    def _update_text_size(self, instance, value):
        self.text_size = value