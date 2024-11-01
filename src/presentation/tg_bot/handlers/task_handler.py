from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram_patch.fsm import State
from pyrogram_patch.fsm.filter import StateFilter
from pyrogram_patch.router import Router

from src.application.common.gateway import TaskGateway
from src.application.service.task import TaskService
from src.domain.value_objects.task_state import TaskState
from src.presentation.tg_bot.fsm.states import ActionTaskState

task_router = Router()


@task_router.on_message(filters.text & StateFilter(ActionTaskState.chose_task))
async def add_new_task_handler(bot, message, state: State, task_gateway: TaskGateway):
    if message.text == "Создать новую задачу":
        await bot.send_message(message.chat.id, "Введите название задачи, которую хотите записать")
        await state.set_state(ActionTaskState.add_task)
    elif message.text == "Мои задачи":
        task_service = TaskService(gateway=task_gateway)
        tasks = await task_service.get_all_users_tasks(user_id=message.from_user.id)
        if not tasks:
            await bot.send_message(message.chat.id, "Вы не записали ни одной задачи.")
        else:
            inline_list = []
            for task in tasks:
                wrap_lst = []
                flag = None
                if task.state == TaskState.PENDING:
                    flag = "⏳"
                elif task.state == TaskState.DONE:
                    flag = "✅"
                wrap_lst.append(InlineKeyboardButton(f"{task.name} {flag}", callback_data=str(task.id)))
                inline_list.append(wrap_lst)
            await bot.send_message(message.chat.id, "Ваши задачи:", reply_markup=InlineKeyboardMarkup(inline_list))


@task_router.on_callback_query(StateFilter(ActionTaskState.chose_task))
async def choose_task(client: Client, callback_query: CallbackQuery, state: State, task_gateway: TaskGateway):
    task = await task_gateway.get_tasks_by_id(int(callback_query.data))
    flag = None
    if task.state == TaskState.PENDING:
        flag = "⏳"
    elif task.state == TaskState.DONE:
        flag = "✅"
    await callback_query.message.edit_text(
        f"{task.name} {flag}\n\nОписание:\n{task.description}\n\nВыберите действие над задачей",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Удалить задачу", callback_data="Удалить задачу")],
                [InlineKeyboardButton("Пометить задачу как выполненную",
                                      callback_data="Пометить задачу как выполненную")],
            ]
        )
    )
    await state.set_data({"task_id": task.id})
    await state.set_state(ActionTaskState.delete_or_change_task)


@task_router.on_callback_query(StateFilter(ActionTaskState.delete_or_change_task))
async def handle_task(client: Client, callback_query: CallbackQuery, state: State, task_gateway: TaskGateway):
    data = await state.get_data()
    task_id = data["task_id"]
    task_service = TaskService(task_gateway)
    task = await task_service.find_task_by_id(task_id=int(task_id))
    if callback_query.data == "Удалить задачу":
        await task_service.delete_task(task)
        await callback_query.message.edit_text("Задача успешно удалена")

    elif callback_query.data == "Пометить задачу как выполненную":
        await task_service.change_task_to_done(task)
        await callback_query.message.edit_text("Задача успешно помечена выполненной")

    await state.set_state(ActionTaskState.chose_task)


@task_router.on_message(filters.text & StateFilter(ActionTaskState.add_task))
async def add_name_to_new_task_handler(bot, message, state: State):
    await state.set_data({"task_name": message.text})
    await bot.send_message(message.chat.id, "Отлично! Теперь запишите описание задачи")
    await state.set_state(ActionTaskState.set_desc_to_task)


@task_router.on_message(filters.text & StateFilter(ActionTaskState.set_desc_to_task))
async def add_description_to_new_task_handler(bot, message, state: State, task_gateway: TaskGateway):
    task_service = TaskService(gateway=task_gateway)
    data_for_new_task = await state.get_data()
    await task_service.add_new_task(
        name=data_for_new_task["task_name"],
        description=message.text,
        user_id=message.from_user.id
    )
    await bot.send_message(message.chat.id, "Отлично! Задача успешно записана")
    await state.set_state(ActionTaskState.chose_task)
