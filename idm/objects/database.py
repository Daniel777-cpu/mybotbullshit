__version__ = '1.1.0 beta (1.3.2 public)'
import os
from os import path as p
import json

from wtflog import warden

logger = warden.get_boy(__name__)

get_dir = p.dirname # p = это os.path, если че)
path = p.join(get_dir(get_dir(get_dir(__file__))), 'database')


def read(name: str):
    'Возвращает словарь из файла с указанным названием'
    logger.debug(f'Открываю файл "{name}"')
    with open(p.join(path, f'{name}.json'), "r", encoding="utf-8") as file:
        return json.loads(file.read())



class ExcDB(Exception):
    code: int
    text: str
    def __init__(self, code):
        self.code = int(code)
        if self.code == 0:
            self.text = 'Ошибка БД: Указанный ID не существует в базе'
        elif self.code == 1:
            self.text = 'Ошибка БД: Указанный ID уже добавлен в базу'
        else: self.text = code



class DB_defaults:

    settings: dict = {
        "prefix": ".л ",
        "farm": {"on": False,"soft": False,"last_time": 0},
        "friends_add": False,
        "user_delete": {},
        "ignore_list": [],
        "del_requests": False,
        "online": False,
        "offline": False,
        "templates_bind": 0
        }

    lp: dict = {"unsynced_changes": {}, "installed": ""}

    warnings: dict = {"secret_fails": {"lp": {"count": 0, "last": ""}, "cb": {"count": 0,"last": ""}}}

    responses: dict = {
        "del_self": "&#13;",
        "del_process": "УДАЛЯЮ ЩАЩАЩ ПАДАЖЖЫ",
        "del_success": "✅ *Произошло удаление*",
        "del_err_924": "❗ Не прокатило. Дежурный администратор? 🤔",
        "del_err_vk": "❗ Не прокатило. Ошибка VK:{ошибка}",
        "del_err_not_found": "❗ Не нашел сообщения для удаления 🤷‍♀",
        "del_err_unknown": "❗ Неизвестная ошибка при удалении 👀",
        "chat_subscribe": "РАБОТАЕТ 👍<br>Идентификатор чатика<br>{имя}<br>во вселенной ириса: {ид}",
        "chat_bind": "Чат '{имя}' успешно привязан!",
        "user_ret_ban_expired": "💚 Срок бана пользователя {ссылка} истек",
        "user_ret_process": "💚 Добавляю {ссылка}",
        "user_ret_success": "✅ Пользователь {ссылка} добавлен в беседу",
        "user_ret_err_no_access": "❗ Не удалось добавить {ссылка}.<br>Нет доступа.<br> Возможно, он не в моих друзьях или он уже в беседе",
        "user_ret_err_vk": "❗ Не удалось добавить пользователя {ссылка}.<br>Ошибка ВК.<br>",
        "user_ret_err_unknown": "❗ Не удалось добавить пользователя {ссылка}.<br>Произошла неизвестная ошибка",
        "to_group_success": "✅ Запись опубликована",
        "to_group_err_forbidden": "❗ Ошибка при публикации. Публикация запрещена. Превышен лимит на число публикаций в сутки, либо на указанное время уже запланирована другая запись, либо для текущего пользователя недоступно размещение записи на этой стене",
        "to_group_err_recs": "❗ Ошибка при публикации. Слишком много получателей",
        "to_group_err_link": "❗ Ошибка при публикации. Запрещено размещать ссылки",
        "to_group_err_vk": "❗ Ошибка при публикации. Ошибка VK:<br>{ошибка}",
        "to_group_err_unknown": "❗ Ошибка при публикации. Неизвестная ошибка",
        "repeat_forbidden_words": [
            "передать",
            "купить",
            "повысить",
            "завещание",
            "модер"
        ],
        "repeat_if_forbidden": "Я это писать не буду.",
        "ping_duty": "{ответ}<br>Ответ за {время}сек.",
        "ping_myself": "{ответ} CB<br>Получено через {время}сек.<br>ВК ответил за {пингвк}сек.<br>Обработано за {обработано}сек.",
        "info_duty": "Информация о дежурном:<br>IDM v{версия}<br>Владелец: {владелец}<br>Чатов: {чаты}<br><br>Информация о чате:<br>Iris ID: {ид}<br>Имя: {имя}",
        "info_myself": "Информация о дежурном:<br>IDM v{версия}<br>Владелец: {владелец}<br>Чатов: {чаты}<br><br>Информация о чате:<br>Iris ID: {ид}<br>Имя: {имя}",
        "not_in_trusted": "Я тебе не доверяю 😑",
        "trusted_err_no_reply": "❗ Ошибка при выполнении, необходимо пересланное сообщение",
        "trusted_err_in_tr": "⚠ Пользователь уже в доверенных",
        "trusted_err_not_in_tr": "⚠ Пользователь не находился в доверенных",
        "trusted_success_add": "✅ Пользователь {ссылка} в доверенных",
        "trusted_success_rem": "✅ Пользователь {ссылка} удален из доверенных",
        "trusted_list": "Доверенные пользователи:"
    }

    def load_user(self, instance = 0) -> dict:
        if not instance:
            instance = DB
        return {
            "access_token": instance.access_token,
            "me_token": instance.me_token,
            "lp_token": instance.lp_token,
            "secret": instance.secret,
            "responses": instance.responses,
            "informed": instance.informed,
            "lp": instance.lp,
            "settings": instance.settings,
            "trusted_users": instance.trusted_users,
            "chats": instance.chats,
            "templates": instance.templates,
            "dyntemplates":instance.dyntemplates
        }



class DB_general:
    'БД с основной информацией'
    path: str = path
    general: dict = {}
    owner_id: int = 0
    users: list = []
    host: str = ""
    installed: bool = False
    v_last: str = __version__
    mode: str = ""
    warnings: dict =  DB_defaults.warnings
    vk_app_id: int = 0
    vk_app_secret: str = ""
    group_id = -195759899

    def __init__(self):
        logger.debug('Инициализация основной БД')
        self.general = read('general')
        self.users = self.general['users']
        self.owner_id = self.general['owner_id']
        self.host = self.general['host']
        self.installed = self.general['installed']
        self.v_last = self.general['v_last']
        self.mode = self.general['mode']
        self.warnings =  self.general['warnings']
        self.vk_app_id = self.general['vk_app_id']
        self.vk_app_secret = self.general['vk_app_secret']

    @property
    def update_general(self):
        'Обновляет экземпляр основной БД в файле database.py'
        global db_gen
        db_gen = DB_general()

    def add_user(self, user_id: int, owner: bool = False):
        if user_id in self.users: raise ExcDB(1)
        self.users.append(user_id)
        if owner: self.owner_id = user_id
        with open(p.join(path, f'{user_id}.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(DB_defaults().load_user(), ensure_ascii=False, indent=4))
        self.save()
        self.update_general
        return DB(user_id)


    def save(self) -> str:
        'Сохранение основной БД'
        logger.debug("Сохраняю основную базу данных")
        self.general['users'] = self.users
        self.general['host'] = self.host
        self.general['installed'] = self.installed
        self.general['v_last'] = self.v_last
        self.general['mode'] = self.mode
        self.general['warnings'] = self.warnings
        self.general['vk_app_id'] = self.vk_app_id
        self.general['vk_app_secret'] = self.vk_app_secret
        self.general['owner_id'] = self.owner_id
        with open(p.join(path, 'general.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(self.general, ensure_ascii=False, indent=4))
        self.update_general
        return "ok"


class DB:
    'БД для конкретного пользователя'
    path: str = path
    full_db: dict = {}
    gen: DB_general

    access_token: str = "Не установлен"
    me_token: str = "Не установлен"
    lp_token: str = "Не установлен"
    secret: str = ""
    chats: dict = {}
    trusted_users: list = []
    duty_id: int = 0
    templates: list = []
    dyntemplates: list = []
    informed: bool = False
    responses: dict = DB_defaults.responses

    lp: dict =  DB_defaults.lp
    settings: dict = DB_defaults.settings


    def __init__(self, user_id: int = 0):
        if not user_id: user_id = db_gen.owner_id
        self.gen = db_gen
        self.duty_id = int(user_id)
        self.full_db = db_gen.general
        self.users = db_gen.users
        self.host = db_gen.host
        self.installed = db_gen.installed
        self.v_last = db_gen.v_last
        self.mode = db_gen.mode
        self.warnings =  db_gen.warnings
        self.vk_app_id = db_gen.vk_app_id
        self.vk_app_secret = db_gen.vk_app_secret
        self.load_user()



    def load_user(self):
        if not self.duty_id: self.duty_id = self.gen.owner_id
        user_db = read(str(self.duty_id))
        logger.debug(f'Загрузка БД пользователя {self.duty_id}')
        if user_db: self.__dict__.update(user_db)
        else: raise ExcDB(0)


    def save(self) -> str:
        'Сохраняет БД пользователя, которая открыта в данном экземпляре DB'
        logger.debug("Сохраняю базу данных")
        with open(p.join(path, f'{str(self.duty_id)}.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(DB_defaults().load_user(self), ensure_ascii=False, indent = 4))
        return "ok"


DB_general().update_general# инициализация основной БД при запуске скрипта

