from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from game.user_manager import UserManager
from game.quest_data import QUEST_SCENES
from bot.keyboards import get_scene_keyboard


REGISTER_NAME = 1

user_manager = UserManager()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    user = user_manager.get_user(user_id)

    if not user["registered"]:
        await update.message.reply_text(
            "Добро пожаловать в QuestChronicle!\n\n"
            "Для начала игры, пожалуйста, введите ваше имя:"
        )
        return REGISTER_NAME
    else:
        await show_scene(update, context, user)
        return ConversationHandler.END


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ввода имени пользователя"""
    user_id = update.effective_user.id
    user_name = update.message.text.strip()

    if not user_name:
        await update.message.reply_text("Пожалуйста, введите ваше имя:")
        return REGISTER_NAME

    user_manager.register_user(user_id, user_name)

    await update.message.reply_text(
        f" Отлично, {user_name}! Регистрация завершена.\n"
        f"Используйте /help для списка команд.\n\n"
        f"Давайте начнем ваше приключение!"
    )

    await show_scene(update, context)
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        " **QuestChronicle - Текстовый квест**\n\n"
        "**Доступные команды:**\n"
        "/start - Начать или продолжить игру\n"
        "/help - Показать это сообщение\n"
        "/status - Показать текущее состояние\n"
        "/reset - Сбросить прогресс и начать заново\n\n"
        "**Как играть:**\n"
        "• Выбирайте действия с помощью кнопок\n"
        "• Собирайте предметы в инвентарь\n"
        "• Набирайте очки для успешного прохождения\n"
        "• Ваши выборы влияют на развитие сюжета!"
    )
    await update.message.reply_text(help_text)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /status"""
    user_id = update.effective_user.id
    user = user_manager.get_user(user_id)

    if not user["registered"]:
        await update.message.reply_text("❌ Вы еще не зарегистрированы. Используйте /start")
        return

    inventory_text = ", ".join(user["inventory"]) if user["inventory"] else "пусто"

    status_text = (
        f" **Статус игрока:** {user['user_name']}\n\n"
        f" Очки: {user['points']}\n"
        f" Инвентарь: {inventory_text}\n"
        f" Текущая локация: {user['current_scene']}"
    )
    await update.message.reply_text(status_text)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /reset"""
    user_id = update.effective_user.id
    user_manager.reset_user(user_id)

    await update.message.reply_text(
        " Ваш прогресс сброшен! Используйте /start чтобы начать новое приключение."
    )


async def show_scene(update: Update, context: ContextTypes.DEFAULT_TYPE, user=None):
    """Показывает текущую сцену пользователя"""
    if user is None:
        user_id = update.effective_user.id
        user = user_manager.get_user(user_id)

    scene_id = user["current_scene"]
    scene = QUEST_SCENES[scene_id]


    choices = []
    available_choices = []

    for choice in scene["choices"]:
        if "requires" in choice:
            if choice["requires"] in user["inventory"]:
                available_choices.append(choice)
                choices.append(choice["text"])
        else:
            available_choices.append(choice)
            choices.append(choice["text"])
    context.user_data["available_choices"] = available_choices

    reply_markup = get_scene_keyboard(choices)
    await update.message.reply_text(scene["text"], reply_markup=reply_markup)


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора пользователя"""
    user_id = update.effective_user.id
    user = user_manager.get_user(user_id)
    user_choice = update.message.text

    if not user["registered"]:
        await update.message.reply_text("❌ Сначала зарегистрируйтесь с помощью /start")
        return

    available_choices = context.user_data.get("available_choices", [])

    selected_choice = None
    for choice in available_choices:
        if choice["text"] == user_choice:
            selected_choice = choice
            break

    if selected_choice:
        next_scene_id = selected_choice["next_scene"]
        next_scene_data = QUEST_SCENES.get(next_scene_id, {})


        user_manager.update_user_scene(user_id, next_scene_id, next_scene_data)

        await show_scene(update, context)
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите один из предложенных вариантов.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик отмены регистрации"""
    await update.message.reply_text(
        "Регистрация отменена. Используйте /start чтобы начать заново."
    )
    return ConversationHandler.END