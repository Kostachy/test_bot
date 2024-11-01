from pyrogram_patch.fsm import StatesGroup, StateItem


class RegistrationState(StatesGroup):
    set_name = StateItem()
    set_login = StateItem()


class LoginState(StatesGroup):
    check_login = StateItem()


class ActionTaskState(StatesGroup):
    chose_action = StateItem()
    chose_task = StateItem()
    get_task = StateItem()
    add_task = StateItem()
    set_desc_to_task = StateItem()
    delete_or_change_task = StateItem()
