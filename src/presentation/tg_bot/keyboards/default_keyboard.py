from pyrogram.types import ReplyKeyboardMarkup

default_keyboard = ReplyKeyboardMarkup(
    [
        ["Мои задачи"],
        ["Создать новую задачу"],
    ],
    resize_keyboard=True,
)
