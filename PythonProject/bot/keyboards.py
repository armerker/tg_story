from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def get_scene_keyboard(choices):
    """Создает клавиатуру для сцены на основе доступных выборов"""
    if not choices:
        return ReplyKeyboardRemove()

    keyboard = [choices[i:i + 2] for i in range(0, len(choices), 2)]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_main_menu_keyboard():
    """Клавиатура для главного меню"""
    keyboard = [
        ["🎮 Продолжить игру"],
        ["📊 Статус", "🔄 Сбросить"],
        ["ℹ️ Помощь"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)