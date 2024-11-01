from pyrogram import filters
from pyrogram_patch.fsm import State
from pyrogram_patch.fsm.filter import StateFilter
from pyrogram_patch.router import Router

from src.application.common.gateway import UserGateway
from src.application.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from src.application.service.user import UserService
from src.domain.exceptions.user import InvalidUserLoginError, InvalidUserNameError
from src.domain.value_objects.username import UserName
from src.presentation.tg_bot.fsm.states import (
    ActionTaskState,
    LoginState,
    RegistrationState,
)
from src.presentation.tg_bot.keyboards.default_keyboard import default_keyboard

auth_router = Router()


@auth_router.on_message(filters.command("start") & StateFilter())
async def start(bot, cmd, state: State, user_gateway: UserGateway):
    user_service = UserService(gateway=user_gateway)
    try:
        await user_service.get_current_user(user_id=cmd.from_user.id)
    except UserNotFoundError:
        await cmd.reply_text(
            f"Привет, {cmd.from_user.first_name}! Для начала нужно зарегистрироваться. Пожалуйста введи свое имя",
        )
        await state.set_state(RegistrationState.set_name)
    else:
        await cmd.reply_text(
            f"Привет, {cmd.from_user.first_name}! Ты уже зарегистрирован. Пожалуйста свой логин для авторизации",
        )
        await state.set_state(LoginState.check_login)


@auth_router.on_message(filters.text & StateFilter(LoginState.check_login))
async def check_login_handler(bot, message, state: State, user_gateway: UserGateway):
    user_service = UserService(gateway=user_gateway)
    is_valid_login = await user_service.check_login(
        user_id=message.from_user.id, input_login=message.text
    )
    if is_valid_login:
        await bot.send_message(
            message.chat.id,
            "Отлично! Теперь выбери действие.",
            reply_markup=default_keyboard,
        )
        await state.set_state(ActionTaskState.chose_task)
    else:
        await bot.send_message(message.chat.id, "Логин неверный, попробуйте еще раз")


@auth_router.on_message(filters.text & StateFilter(RegistrationState.set_name))
async def set_user_name_handler(bot, message, state: State):
    try:
        UserName(message.text)
    except InvalidUserNameError as err:
        await bot.send_message(message.chat.id, err.description)
    else:
        await state.set_data({"username": message.text})
        await bot.send_message(
            message.chat.id, "Отлично! Теперь придумай и введи логин."
        )
        await state.set_state(RegistrationState.set_login)


@auth_router.on_message(filters.text & StateFilter(RegistrationState.set_login))
async def set_user_login_handler(bot, message, state: State, user_gateway: UserGateway):
    data = await state.get_data()
    user_service = UserService(gateway=user_gateway)
    try:
        await user_service.register_new_user(
            user_id=message.from_user.id,
            name=data["username"],
            login=message.text,
        )
    except (InvalidUserLoginError, UserAlreadyExistsError) as err:
        await bot.send_message(message.chat.id, err.description)
    else:
        await bot.send_message(
            message.chat.id, "А теперь выбери действие!", reply_markup=default_keyboard
        )
        await state.set_state(state=ActionTaskState.chose_task)
