from vkbottle.bot import Bot, Message
from vkbottle import API
import sqlite3
from datetime import datetime, timedelta
from pydantic import BaseModel
from backg import keep_alived
from set import Token

class Meser(BaseModel):
    first_name: str


conn = sqlite3.connect('BD-gbt.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS chats
                                (id INTEGER PRIMARY KEY, filtr TEXT DEFAULT off, quiet TEXT DEFAULT off, type TEXT DEFAULT game, server TEXT DEFAULT null000)'''
               )
conn.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS other
                                (gban TEXT PRIMARY KEY)''')
conn.commit()
bot = Bot(Token
)
api = API(
    token=Token)


@bot.on.private_message(text="<msg>")
async def echo_answer(ans: Message):
    if "#bug" in ans.text:

        await ans.answer(
            "Баг зарегистрирован и отправлен специалистам, если нам понадобятся подробности, мы обратимся к вам в этом чате"
        )
    else:
        await ans.answer(
            "Для работы с ботом, зайдите в группу, добавьте бота в чат и выдайте ему права администратора"
        )


@bot.on.chat_message(action=["chat_invite_user", "chat_invite_user_by_link"])
async def user_joined(ans: Message):
    if int(ans.action.member_id) == -224035401:
        await bot.api.messages.send(
            chat_id=ans.chat_id,
            message=
            "Привет :)\nВыдайте боту права администратора и дайте полный доступ к переписке",
            random_id=0)
    try:
        conn = sqlite3.connect('BD-gbt.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT mute, prban FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
            (ans.action.member_id,))
        ffg = cursor.fetchall()
        if ffg[0][0] == "2888q01q01q23q59q59q100000":
            await bot.api.messages.remove_chat_user(chat_id=ans.chat_id,
                                                    member_id=ans.action.member_id)
            await ans.answer(
                f'[id{ans.action.member_id}|Пользователь] находится в бане\nПричина: {ffg[0][1]}')

    except:
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO chat" + str(ans.chat_id) +
                    " (idd,mute,iwarn) VALUES (?,?,?)", (
                        ans.action.member_id,
                        "1900q01q01q23q59q59q100000",
                        "",
                    ))
                conn.commit()



@bot.on.chat_message(action="chat_kick_user")
async def user_kick(ans: Message):
    if ans.action.member_id == ans.from_id:
        conn = sqlite3.connect('BD-gbt.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE chat" + str(ans.chat_id) +
            " SET mute=(?), prban=(?), dban=(?) WHERE idd=(?)", (
                "2888q01q01q23q59q59q100000",
                "Выход из чата",
                str(datetime.now()),
                ans.from_id,
            ))
        conn.commit()
        await ans.answer('Пользователь вышел из чата и был заблокирован ')
        await bot.api.messages.remove_chat_user(chat_id=ans.chat_id,
                                                member_id=ans.action.member_id)


@bot.on.chat_message(text="<msg>")
async def hmmmm(ans: Message):
    conn = sqlite3.connect('BD-gbt.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chats")
    znack = cursor.fetchall()
    qw = 0
    for zn in znack:
        if zn[0] == ans.chat_id:
            stat_fil = zn[1]
            rquiet = zn[2]
            qw = 1
            cursor.execute(
                "SELECT idd FROM chat" + str(ans.chat_id) + " WHERE rol=(?)",
                ("creator",))
            prov = cursor.fetchone()
            if prov == ("",) or prov == (None,) or str(prov) == "None":
                qw = 0
    if qw == 0:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS chat" + str(ans.chat_id) +
            "(idd INTEGER PRIMARY KEY, rol TEXT, nick TEXT, mute TEXT, prban TEXT, dban TEXT, warn INTEGER DEFAULT 0, owarn INTEGER DEFAULT 0, iwarn TEXT, mmute TEXT)"
        )
        cursor.execute("INSERT OR IGNORE INTO chats (id) VALUES (?)",
                       (ans.chat_id,))
        conn.commit()
        conn = sqlite3.connect('BD-gbt.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS filtr" + str(ans.chat_id) +
                       "(slova TEXT PRIMARY KEY)")

        conn.commit()
        memb = await api.messages.get_conversation_members(peer_id=ans.peer_id)
        for m in memb.items:
            if str(m.is_owner) == "True":
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO chat" + str(ans.chat_id) +
                    " (idd,rol,mute,iwarn) VALUES (?,?,?,?)", (
                        m.member_id,
                        "creator",
                        "1900q01q01q23q59q59q100000",
                        "",
                    ))
                conn.commit()
            elif m.member_id > 0:
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO chat" + str(ans.chat_id) +
                    " (idd,mute,iwarn) VALUES (?,?,?)", (
                        m.member_id,
                        "1900q01q01q23q59q59q100000",
                        "",
                    ))
                conn.commit()
        stat_fil = "off"
        rquiet = "off"

    cursor.execute("SELECT rol FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
                   (ans.from_id,))
    role = cursor.fetchone()
    conn = sqlite3.connect('BD-gbt.db')
    cursor = conn.cursor()
    if str(ans.text)[0] == "!" or str(ans.text)[0] == "?" or str(
            ans.text)[0] == "+":
        ans.text = "/" + str(ans.text)[1:]
    # пользователи
    if "/sat" in ans.text:  #############################################
        cursor.execute(
            "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)", (
                "creator",
                ans.from_id,
            ))
        conn.commit()
    if ans.text == "/info":
        await ans.answer("""Официальные ресурсы проекта:
    Форум-
    Дискорд-
    Группа вк-
    Тех.поддержка- @club224035401
    Лаборатория разработчиков- @ld10000000001
    Начать сотрудничество-
    Спец администор-
    Вакансии-""")

    if ans.text == "/help":
        if role[0] == "creator":
            await ans.answer("""Команды:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном
      /ban — заблокировать пользователя в беседе
      /unban — разблокировать пользователя в беседе
      /addmoder — выдать пользователю модератора
      /removerole — забрать роль у пользователя
      /zov — упомянуть всех пользователей
      /online — упомянуть пользователей онлайн
      /banlist — посмотреть заблокированных
      /onlinelist — посмотреть пользователей в онлайн
      /skick — исключить пользователя с бесед сервера
      /quiet — Включить выключить режим тишины
      /sban — заблокировать пользователя в беседах сервера
      /sunban — разбанить пользователя в беседах сервера
      /addsenmoder — дать пользователю роль старшего модератора
      /bug — сообщить разработчику о баге
      /gban — заблокировать пользователя во всех беседах
      /gunban — разблокировать пользователя во всех беседах
      /sync — синхронизация с базой данных
      /type — выбрать тип беседы(по умолчанию — беседа игроков)
      /addadmin — выдать пользователю администратора
      /server — привязать беседу к серверу
      /gbanlist — посмотреть список в глобального бана
      /addword — добавить в фильтр слово
      /delword — удаляет из фильтра слово
      /settings — показать настройки беседы
      /filter — включить/выключить фильтр
      /banwords — посмотреть запрещённые слова
      /gbanpl — заблокировать пользователя в беседах игроков
      /gunbanpl — разблокировать пользователя в беседах игроков
      /gremoverole — забрать у пользователя роли во всех чатах
      /addsenadm — выдать пользователю старшего администратора
      /gzov — упомянуть всех пользователей в категории бесед
      /gsync — глобальная синхронизация
      /gnlist — отправить nlist во все беседы кроме бесед игроков и общих
      /urkick — кикнуть пользователей без роли
      /addzsa — назначить зам.спец администратора
      /addsa — назначить спец администратора""")
        elif role[0] == "spadmin":
            await ans.answer("""Команды:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном
      /ban — заблокировать пользователя в беседе
      /unban — разблокировать пользователя в беседе
      /addmoder — выдать пользователю модератора
      /removerole — забрать роль у пользователя
      /zov — упомянуть всех пользователей
      /online — упомянуть пользователей онлайн
      /banlist — посмотреть заблокированных
      /onlinelist — посмотреть пользователей в онлайн
      /skick — исключить пользователя с бесед сервера
      /quiet — Включить выключить режим тишины
      /sban — заблокировать пользователя в беседах сервера
      /sunban — разбанить пользователя в беседах сервера
      /addsenmoder — дать пользователю роль старшего модератора
      /bug — сообщить разработчику о баге
      /gban — заблокировать пользователя во всех беседах
      /gunban — разблокировать пользователя во всех беседах
      /sync — синхронизация с базой данных
      /type — выбрать тип беседы(по умолчанию — беседа игроков)
      /addadmin — выдать пользователю администратора
      /server — привязать беседу к серверу
      /gbanlist — посмотреть список в глобального бана
      /addword — добавить в фильтр слово
      /delword — удаляет из фильтра слово
      /settings — показать настройки беседы
      /filter — включить/выключить фильтр
      /banwords — посмотреть запрещённые слова
      /gbanpl — заблокировать пользователя в беседах игроков
      /gunbanpl — разблокировать пользователя в беседах игроков
      /gremoverole — забрать у пользователя роли во всех чатах
      /addsenadm — выдать пользователю старшего администратора
      /gzov — упомянуть всех пользователей в категории бесед
      /gsync — глобальная синхронизация
      /gnlist — отправить nlist во все беседы кроме бесед игроков и общих
      /urkick — кикнуть пользователей без роли
      /addzsa — назначить зам.спец администратора""")
        elif role[0] == "zspadmin":
            await ans.answer("""Команды:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном
      /ban — заблокировать пользователя в беседе
      /unban — разблокировать пользователя в беседе
      /addmoder — выдать пользователю модератора
      /removerole — забрать роль у пользователя
      /zov — упомянуть всех пользователей
      /online — упомянуть пользователей онлайн
      /banlist — посмотреть заблокированных
      /onlinelist — посмотреть пользователей в онлайн
      /skick — исключить пользователя с бесед сервера
      /quiet — Включить выключить режим тишины
      /sban — заблокировать пользователя в беседах сервера
      /sunban — разбанить пользователя в беседах сервера
      /addsenmoder — дать пользователю роль старшего модератора
      /bug — сообщить разработчику о баге
      /gban — заблокировать пользователя во всех беседах
      /gunban — разблокировать пользователя во всех беседах
      /sync — синхронизация с базой данных
      /type — выбрать тип беседы(по умолчанию — беседа игроков)
      /addadmin — выдать пользователю администратора
      /server — привязать беседу к серверу
      /gbanlist — посмотреть список в глобального бана
      /addword — добавить в фильтр слово
      /delword — удаляет из фильтра слово
      /settings — показать настройки беседы
      /filter — включить/выключить фильтр
      /banwords — посмотреть запрещённые слова
      /gbanpl — заблокировать пользователя в беседах игроков
      /gunbanpl — разблокировать пользователя в беседах игроков
      /gremoverole — забрать у пользователя роли во всех чатах
      /addsenadm — выдать пользователю старшего администратора
      /gzov — упомянуть всех пользователей в категории бесед
      /gsync — глобальная синхронизация
      /gnlist — отправить nlist во все беседы кроме бесед игроков и общих
      /urkick — кикнуть пользователей без роли""")
        elif role[0] == "stadmin":
            await ans.answer("""Команды:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном
      /ban — заблокировать пользователя в беседе
      /unban — разблокировать пользователя в беседе
      /addmoder — выдать пользователю модератора
      /removerole — забрать роль у пользователя
      /zov — упомянуть всех пользователей
      /online — упомянуть пользователей онлайн
      /banlist — посмотреть заблокированных
      /onlinelist — посмотреть пользователей в онлайн
      /skick — исключить пользователя с бесед сервера
      /quiet — Включить выключить режим тишины
      /sban — заблокировать пользователя в беседах сервера
      /sunban — разбанить пользователя в беседах сервера
      /addsenmoder — дать пользователю роль старшего модератора
      /bug — сообщить разработчику о баге
      /gban — заблокировать пользователя во всех беседах
      /gunban — разблокировать пользователя во всех беседах
      /sync — синхронизация с базой данных
      /type — выбрать тип беседы(по умолчанию — беседа игроков)
      /addadmin — выдать пользователю администратора
      /server — привязать беседу к серверу
      /gbanlist — посмотреть список в глобального бана
      /addword — добавить в фильтр слово
      /delword — удаляет из фильтра слово
      /settings — показать настройки беседы
      /filter — включить/выключить фильтр
      /banwords — посмотреть запрещённые слова
      /gbanpl — заблокировать пользователя в беседах игроков
      /gunbanpl — разблокировать пользователя в беседах игроков""")
        elif role[0] == "admin":
            await ans.answer("""Команды:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном
      /ban — заблокировать пользователя в беседе
      /unban — разблокировать пользователя в беседе
      /addmoder — выдать пользователю модератора
      /removerole — забрать роль у пользователя
      /zov — упомянуть всех пользователей
      /online — упомянуть пользователей онлайн
      /banlist — посмотреть заблокированных
      /onlinelist — посмотреть пользователей в онлайн
      /skick — исключить пользователя с бесед сервера
      /quiet — Включить выключить режим тишины
      /sban — заблокировать пользователя в беседах сервера
      /sunban — разбанить пользователя в беседах сервера
      /addsenmoder — дать пользователю роль старшего модератора
      /bug — сообщить разработчику о баге""")
        elif role[0] == "stmoder":
            await ans.answer("""Команды:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном
      /ban — заблокировать пользователя в беседе
      /unban — разблокировать пользователя в беседе
      /addmoder — выдать пользователю модератора
      /removerole — забрать роль у пользователя
      /zov — упомянуть всех пользователей
      /online — упомянуть пользователей онлайн
      /banlist — посмотреть заблокированных
      /onlinelist — посмотреть пользователей в онлайн""")
        elif role[0] == "moder":
            await ans.answer("""Команды пользователей:
      /info — официальные ресурсы проекта
      /stats — информация о пользователе
      /getid — узнать оригинальный ID пользователя в ВК
      /kick — исключить пользователя из беседы
      /mute — замутить пользователя
      /unmute — размутить пользователя
      /warn — выдать предупреждение пользователю
      /unwarn — снять предупреждение пользователю
      /getban — информация о банах пользователя
      /getwarn — информация о активных предупреждениях пользователя
      /warnhistory — информация о всех предупреждениях пользователя
      /staff — пользователи с ролями
      /setnick — сменить ник у пользователя
      /removenick — очистить ник у пользователя
      /nlist — посмотреть ники пользователей
      /nonick — пользователи без ников
      /getnick — проверить ник пользователя
      /alt — узнать альтернативные команды
      /getacc — узнать пользователя по нику
      /warnlist — список пользователей с варном""")
        else:
            await ans.answer("""Команды:
            /info — официальные ресурсы проекта
            /stats — информация о пользователе
            /getid — узнать оригинальный ID пользователя в ВК""")
    if ans.text == "/getid":
        nom1 = (ans.text.removeprefix("/kick")).strip()
        if nom1 == "":
            if ans.reply_message:
                nid = ans.reply_message.from_id
                await ans.answer("ID: " + str(ans.reply_message.from_id))
            else:
                await ans.answer(
                    'Ответьте на сообщение или упомяните пользователя после команды')
        elif "[id" in nom1:
            nid = nom1.removeprefix("[id").split("|")[0]
            await ans.answer("ID: " + str(nid))
        elif "vk.com/" in nom1:
            fgr = nom1.removeprefix("https://vk.com/")  # .split(" ")[0]
            nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
            await ans.answer("ID: " + str(nid))
        else:
            await ans.answer("Упомяните пользователя с помощью * или @")

    if "/stats" in ans.text:
        nom4 = (ans.text.removeprefix("/stats")).strip()
        if nom4 == "":
            if ans.reply_message:
                stid = ans.reply_message.from_id
            else:
                stid = ans.from_id
        elif "[id" in nom4:
            stid = nom4.removeprefix("[id").split("|")[0]
        elif "vk.com/" in nom4:
            fgr = nom4.removeprefix("https://vk.com/")
            stid = int((await bot.api.users.get(user_ids=fgr))[0].id)
        else:
            stid = ans.from_id

        try:
            conn = sqlite3.connect('BD-gbt.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
                           (stid,))
            stus = cursor.fetchall()
            if stus[0][1] == None:
                strol = "нет"
            else:
                strol = str(stus[0][1])
            if stus[0][2] == None:
                stnick = "нет"
            else:
                stnick = str(stus[0][2])
            if stus[0][3] == "1900q01q01q23q59q59q100000":
                stmut = "нет"
                stban = "нет"
            elif stus[0][3] == "2888q01q01q23q59q59q100000":
                stmut = "нет"
                stban = "есть" + "\nПричина:" + str(stus[0][4]) + f"\n[id{stus[0][9]}|Модератор]" + "\nДата:" + str(
                    stus[0][5][:-7])
            else:
                stmut = "есть, до " + str(
                    datetime.strptime(
                        stus[0][3], '%Yq%mq%dq%Hq%Mq%Sq%f'))[0:19] + "\nПричина:" + str(
                    stus[0][4]) + f"\n[id{stus[0][9]}|Модератор]" + "\nДата:" + str(stus[0][5][:-7])
                stban = "нет"
            if int(stus[0][6]) > 0:
                stiw = str(stus[0][6]) + "\nПричины: " + str(stus[0][8])
            elif int(stus[0][6]) == 0:
                stiw = "0"

            await ans.answer(
                f'ID: {stus[0][0]}\nРоль: {strol}\nНик: {stnick}\nМут: {stmut}\nБан: {stban}\nВсего предупреждений: {stus[0][7]}\nАктивных предупреждений: {stiw}'
            )
        except:
            await ans.answer("Что-то пошло не так...\nВозможно пользователя нет в чате")
    # moder
    if "/kick" in ans.text or "/mute" in ans.text or "/unmute" in ans.text or "/warn" in ans.text or "/unwarn" in ans.text or "/getban" in ans.text or "/getwarn" in ans.text or "/warnhistory" in ans.text or "/staff" in ans.text or "/setnick" in ans.text or "/removenick" in ans.text or "/nlist" in ans.text or "/nonick" in ans.text or "/getnick" in ans.text or "/alt" in ans.text or "/getacc" in ans.text or "/warnlist" in ans.text or "/clear" in ans.text:
        if role in [("admin",), ("zspadmin",), ("spadmin",), ("stmoder",),
                    ("moder",), ("stadmin",), ("creator",)]:
            if ans.text == "/nlist":
                cursor.execute("SELECT * FROM chat" + str(ans.chat_id))
                nuser = cursor.fetchall()
                nust1 = []
                nust2 = []
                nust3 = []
                nick_str = ""
                for nus in nuser:
                    if str(nus[2]) != "null" and int(nus[0]) > 0 and str(
                            nus[2]) != "None":
                        name = await bot.api.users.get(nus[0])
                        nust1.append(name[0].first_name)
                        nust2.append(nus[0])
                        nust3.append(nus[2])
                for i in range(len(nust2)):
                    nick_str = nick_str + str(
                        i + 1) + ". " + f'[id{nust2[i]}|{nust1[i]}]-{nust3[i]}\n'
                if nick_str == "":
                    await ans.answer("В этом чате нет пользователей с никами")
                else:
                    await ans.answer(nick_str)
            elif ans.text == "/nonick":
                cursor.execute("SELECT * FROM chat" + str(ans.chat_id))
                nuser = cursor.fetchall()
                noust1 = []
                noust2 = []
                nonick_str = ""
                for nus in nuser:
                    if (str(nus[2]) == "null" or str(nus[2]) == "None") and int(nus[0]) > 0:
                        name = await bot.api.users.get(nus[0])
                        noust1.append(name[0].first_name)
                        noust2.append(nus[0])
                for i in range(len(noust2)):
                    nonick_str = nonick_str + str(
                        i + 1) + ". " + f'[id{noust2[i]}|{noust1[i]}]\n'
                if nonick_str == "":
                    await ans.answer("В этом чате нет пользователей без ников")
                else:
                    await ans.answer(nonick_str)
            elif "/getacc" in ans.text:
                gacc = (ans.text.removeprefix("/getacc")).strip()
                if gacc != "":
                    try:
                        cursor.execute(
                            "SELECT idd FROM chat" + str(ans.chat_id) + " WHERE nick=(?)",
                            (gacc,))
                        gacc2 = cursor.fetchone()
                        await ans.answer(f'[id{gacc2[0]}|{gacc}]')
                    except:
                        await ans.answer("В этом чате нет пользователя с таким ником")
            elif "/staff" in ans.text:
                cursor.execute("SELECT * FROM chat" + str(ans.chat_id))
                stuser = cursor.fetchall()
                stust1 = []
                stust2 = []
                stust3 = []
                staff_str = ""
                for st in stuser:
                    if (str(st[1]) != "null"
                        and str(st[1]) != "None") and int(st[0]) > 0:
                        name = await bot.api.users.get(st[0])
                        stust1.append(name[0].first_name)
                        stust2.append(st[0])
                        stust3.append(st[1])
                for i in range(len(stust2)):
                    staff_str = staff_str + str(
                        i + 1) + ". " + f'[id{stust2[i]}|{stust1[i]}] - {stust3[i]}\n'
                await ans.answer(staff_str)
            elif "/warnlist" in ans.text:
                cursor.execute("SELECT * FROM chat" + str(ans.chat_id))
                wuser = cursor.fetchall()
                wust1 = []
                wust2 = []
                warn_str = ""
                for wus in wuser:
                    if int(wus[4]) > 0 and int(wus[0]) > 0:
                        name = await bot.api.users.get(wus[0])
                        wust1.append(name[0].first_name)
                        wust2.append(wus[0])
                for i in range(len(wust2)):
                    warn_str = warn_str + str(i +
                                              1) + ". " + f'[id{wust2[i]}|{wust1[i]}]\n'
                if warn_str == "":
                    await ans.answer(
                        "В этом чате нет пользователей с активными предупреждениями")
                else:
                    await ans.answer(warn_str)
            elif "/alt" in ans.text:
                await ans.answer(
                    "Альтернативные команды:\n\n Альтернативных команд нет")
            elif "/setnick" in ans.text:
                nom3 = (ans.text.removeprefix("/setnick")).strip()
                if nom3 == "":
                    await ans.answer(
                        'Ответьте на сообщение или упомяните пользователя после команды'
                    )
                elif "[id" in nom3:
                    nid = nom3.removeprefix("[id").split("|")[0]
                    nick1 = str(nom3.split("]")[1].strip())
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        nick1 = str(nom3.split(" ")[1].strip())
                    except ValueError:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        nick1 = ""

                elif ans.reply_message:
                    nid = ans.reply_message.from_id
                    nick1 = str(nom3.strip())
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                if nick1 != "":
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET nick=(?) WHERE idd=(?)",
                        (
                            nick1,
                            ans.reply_message.from_id,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = (cursor.fetchone())[0]
                    if nmnm != None:
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] сменил(а) ник [id{nid}|{name2[0].first_name}] на {nick1}'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] сменил(а) ник пользователя на {nick1}'
                        )
                else:
                    await ans.answer('Напишите ник после команды')
            elif "/kick" in ans.text:
                nom1 = (ans.text.removeprefix("/kick")).strip()
                if nom1 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom1:
                    nid = nom1.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom1:
                    try:
                        fgr = nom1.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom1.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                if int(nid) > 0:
                    await bot.api.messages.remove_chat_user(chat_id=ans.chat_id,
                                                            member_id=nid)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
                        (nid,))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] исключил из беседы [id{nid}|{name2[0].first_name}]'
                    )
            elif "/removenick" in ans.text:
                nom2 = (ans.text.removeprefix("/removenick")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Вы не ответили на сообщение, попробуйте заново.\nИли упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                cursor.execute(
                    "UPDATE chat" + str(ans.chat_id) + " SET nick=null WHERE idd=(?)",
                    (nid,))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                nmnm = str((cursor.fetchone())[0])
                if nmnm != "None":
                    name1 = [Meser.parse_obj({'first_name': nmnm})]
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] удалил(a) ник [id{nid}|{name2[0].first_name}]'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] удалил(a) ник пользователя'
                    )
            elif "/getnick" in ans.text:
                nom2 = (ans.text.removeprefix("/getnick")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                cursor.execute(
                    "SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
                    (nid,))
                gnick = cursor.fetchone()
                if gnick == ("null",) or gnick == (None,) or gnick == ("",):
                    await ans.answer('У пользователя нет ника')
                else:
                    await ans.answer(gnick[0])
            elif "/warnhistory" in ans.text:
                nom2 = (ans.text.removeprefix("/warnhistory")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                cursor.execute(
                    "SELECT warn,owarn,iwarn FROM chat" + str(ans.chat_id) +
                    " WHERE idd=(?)", (nid,))
                whis = cursor.fetchall()
                if int(whis[0][0]) > 0:
                    siw = str(whis[0][0]) + "\nПричины: " + str(whis[0][2])
                elif int(whis[0][0]) == 0:
                    siw = "0"
                await ans.answer(
                    f'Всего предупреждений: {whis[0][1]}\nАктивных предупреждений: {siw}'
                )
            elif "/warn" in ans.text:
                nom3 = (ans.text.removeprefix("/warn")).strip()
                if nom3 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                        prich1 = "Не указана"
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom3:
                    if nom3.split("]")[1].strip() == "":
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich1 = "Не указана"
                    else:
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich1 = str(nom3.split("]")[1].strip())
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich1 = str(nom3.removeprefix(str(nom3.split(" ")[0])).strip())
                        print(nid)
                    except ValueError:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich1 = "Не указана"
                        print("exception")
                elif ans.reply_message:
                    nid = ans.reply_message.from_id
                    prich1 = str(nom3.strip())
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                if int(nid) > 0:
                    cursor.execute(
                        "SELECT warn,iwarn FROM chat" + str(ans.chat_id) +
                        " WHERE idd=(?)", (nid,))
                    aws = cursor.fetchmany(2)
                    if int(aws[0][0]) >= 2:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(ans.chat_id) +
                            " SET mute=(?), prban=(?), dban=(?) WHERE idd=(?)", (
                                "2888q01q01q23q59q59q100000",
                                "Максимальное количество предупреждений",
                                str(datetime.now()),
                                nid,
                            ))
                        conn.commit()
                        await bot.api.messages.remove_chat_user(chat_id=ans.chat_id,
                                                                member_id=nid)
                        await ans.answer(
                            'Пользователь забанен, т.к. превышено количество предупреждений'
                        )
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(ans.chat_id) +
                            " SET warn=warn+1,owarn=owarn+1, iwarn=(?) WHERE idd=(?)", (
                                aws[0][1] + prich1,
                                nid,
                            ))
                        conn.commit()
                    elif int(aws[0][0]) < 2:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(ans.chat_id) +
                            " SET warn=warn+1,owarn=owarn+1, iwarn=(?) WHERE idd=(?)", (
                                aws[0][1] + prich1 + ",",
                                nid,
                            ))
                        conn.commit()
                    else:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(ans.chat_id) +
                            " SET warn=warn+1,owarn=owarn+1, iwarn=(?) WHERE idd=(?)", (
                                aws[0][1] + prich1 + ",",
                                nid,
                            ))
                        conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] выдал(а) предупреждение [id{nid}|{name2[0].first_name}]\nПричина: {prich1}'
                    )
            elif "/unwarn" in ans.text:
                nom2 = (ans.text.removeprefix("/unwarn")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                cursor.execute(
                    "SELECT warn,iwarn FROM chat" + str(ans.chat_id) +
                    " WHERE idd=(?)", (nid,))
                awed = cursor.fetchall()
                if awed[0][0] == 0:
                    await ans.answer("У пользователя нет активных предупреждений")
                elif awed[0][0] == 1:
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) +
                        " SET warn=0,iwarn=(?) WHERE idd=(?)", (
                            "",
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] снял(a) предупреждение [id{nid}|{name2[0].first_name}]\nАктивных предупреждений: 0'
                        )
                    except:
                        await ans.answer(
                            f'[id{nid}|{name1[0].first_name}] снял(a) предупреждение \nАктивных предупреждений: 0'
                        )
                elif awed[0][0] == 2:
                    furt = str(awed[0][1].split(",")[0]) + ","
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) +
                        " SET warn=1,iwarn=(?) WHERE idd=(?)", (
                            furt,
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{nid}|{name1[0].first_name}] снял(a) предупреждение [id{nid}|{name2[0].first_name}]\nАктивных предупреждений: 1'
                        )
                    except:
                        await ans.answer(
                            f'[id{nid}|{name1[0].first_name}] снял(a) предупреждение \nАктивных предупреждений: 1'
                        )
                elif awed[0][0] == 3:
                    furst = awed[0][1].split(",")[:2]
                    print(furst)
                    furt = furst[0] + "," + furst[1] + ","
                    print(furt)
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) +
                        " SET warn=2,iwarn=(?) WHERE idd=(?)", (
                            furt,
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{nid}|{name1[0].first_name}] снял(a) предупреждение [id{nid}|{name2[0].first_name}]\nПользователь разбанен\nАктивных предупреждений: 2'
                        )
                    except:
                        await ans.answer(
                            f'[id{nid}|{name1[0].first_name}] снял(а) предупреждение\nПользователь разбанен\nАктивных предупреждений: 2'
                        )
                else:
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) +
                        " SET warn=0,iwarn=(?) WHERE idd=(?)", (
                            "",
                            nid,
                        ))
                    conn.commit()
            elif "/unmute" in ans.text:
                nom2 = (ans.text.removeprefix("/unmute")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                try:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET mute=(?) WHERE idd=(?)",
                        (
                            "1900q01q01q23q59q59q100000",
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{nid}|{name1[0].first_name}] снял(a) мут [id{nid}|{name2[0].first_name}]'
                        )
                    except:
                        await ans.answer(f'[id{nid}|{name1[0].first_name}] снял(а) мут')
                except:
                    await ans.answer('Что-то пошло не так...\nПопробуйте еще раз')
            elif "/getwarn" == ans.text:
                nom2 = (ans.text.removeprefix("/getwarn")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")

                cursor.execute(
                    "SELECT warn,iwarn FROM chat" + str(ans.chat_id) +
                    " WHERE idd=(?)", (nid,))
                gwar = cursor.fetchall()
                if int(gwar[0][6]) > 0:
                    sw = str(gwar[0][6]) + "\nПричины: " + str(gwar[0][8])
                elif int(gwar[0][6]) == 0:
                    sw = "0"
                await ans.answer(f"Активных предупреждений: {sw}")
            elif "/getban" in ans.text:
                nom2 = (ans.text.removeprefix("/getban")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid1 = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid1 = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid1 = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid1 = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                ban_str = ""

                cursor.execute("SELECT * FROM other WHERE gban=(?)",(nid1,))
                gband = cursor.fetchall()
                print(gband)
                if len(gband)==0:

                    cursor.execute("SELECT id,type FROM chats")
                    gbanf = cursor.fetchall()
                    bn = 2
                    fkf=0
                    for gtf in gbanf:
                        print(gtf)
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT mute, prban, dban, mmute FROM chat" + str(gtf[0]) +
                            " WHERE idd=(?)", (nid1,))
                        dtf = cursor.fetchall()
                        print(dtf)
                        try:
                            if dtf[0][0] == "2888q01q01q23q59q59q100000":
                                if gtf[1]!="game":
                                    bn=8
                                    print(2)
                                else:
                                    print(1)
                                    ban_str1=f'\nПричина: {dtf[0][1]}\n[id{dtf[0][3]}|Модератор]\nДата: {dtf[0][2][:-7]}\n\n'
                                conv = await bot.api.messages.get_conversations_by_id(
                                    peer_ids=2000000000 + int(gtf[0]))
                                ch_nazv = conv.items[0].chat_settings.title
                                ban_str = ban_str + str(
                                    ch_nazv) + f'\nПричина: {dtf[0][1]}\n[id{dtf[0][3]}|Модератор]\nДата: {dtf[0][2][:-7]}\n\n'
                                fkf+=1
                            elif gtf[1] == "game":
                                bn=8
                        except Exception as err:
                            print("hhh")
                            print(err)
                else:
                    bn=5
                    toy=9
                    i=0
                    fkf=9
                    while toy==9:
                        i+=1
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        try:
                            cursor.execute(
                            "SELECT mute, prban, dban, mmute FROM chat" + str(i) +
                            " WHERE idd=(?)", (nid1,))
                            dtf = cursor.fetchall()


                            if dtf[0][0] == "2888q01q01q23q59q59q100000":
                                ban_str2 =f'\nПричина: {dtf[0][1]}\n[id{dtf[0][3]}|Модератор]\nДата: {dtf[0][2][:-7]}'
                                toy=2

                        except Exception as err:
                            print(i)

                if fkf==0:
                    await ans.answer(f"Информация о блокировках [id{nid1}|пользователя]\n\nБлокировка во всех беседах - отсутствует\n\nИнформация о блокировке в беседах игроков - отсутствует \nблокировки в беседах отсутствуют")

                elif (ban_str != "" and bn==8):
                    await ans.answer(f"Информация о блокировках [id{nid1}|пользователя]\n\nБлокировка во всех беседах - отсутствует\n\nИнформация о блокировке в беседах игроков - отсутствует \nИнформация о блокировке в беседах:\n{ban_str}")

                elif bn==2:
                    await ans.answer(f"Информация о блокировках [id{nid1}|пользователя]\n\nБлокировка во всех беседах - отсутствует\n\nИнформация о блокировке в беседах игроков:\n{ban_str1} \nблокировки в беседах отсутствуют")
                elif bn==5:
                    await ans.answer(f"Информация о блокировках [id{nid1}|пользователя]\n\nИнформация о блокировке во всех беседах:\n{ban_str2}\n\nИнформация о блокировке в беседах игроков:\n{ban_str2}\nблокировки в беседах отсутствуют")

                else:
                    await ans.answer(f"Информация о блокировках [id{nid1}|пользователя]\n\nБлокировка во всех беседах - отсутствует\n\nИнформация о блокировке в беседах игроков - отсутствует \nблокировки в беседах отсутствуют")
            elif "/mute" in ans.text:
                sep = 1
                df = 0
                nom2 = (ans.text.removeprefix("/mute")).strip()
                if "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                    df = 1
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        df = 2
                    except ValueError:
                        mutre = ""
                elif ans.reply_message:
                    nid = ans.reply_message.from_id

                else:
                    await ans.answer(
                        'Ответьте на сообщение или упомяните пользователя после команды')

                if df == 1:
                    mutre = (nom2.split("]")[1]).strip()
                elif df == 2:
                    mutre = nom2.removeprefix(str(nom2.split()[0]).strip()).strip()
                elif df == 0:
                    mutre = nom2
                print(mutre)
                if mutre != "":
                    if len(mutre.split()) == 1:
                        prin = "Не указана"
                    elif len(mutre.split()) > 1:
                        prin = mutre.removeprefix(mutre.split()[0]).strip()
                else:
                    await ans.answer('Напишите количество минут мута после команды')
                    sep = 0
                if sep != 0:
                    try:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(ans.chat_id) +
                            " SET mute=(?),prban=(?), dban=(?), mmute=(?) WHERE idd=(?)", (
                                (datetime.now() +
                                 timedelta(minutes=int(mutre.split()[0].strip()))
                                 ).strftime('%Yq%mq%dq%Hq%Mq%Sq%f'),
                                prin,
                                str(datetime.now()),
                                ans.from_id,
                                nid,
                            ))
                        conn.commit()
                        name1 = await bot.api.users.get(ans.from_id)
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                        nmnm = str((cursor.fetchone())[0])
                        if nmnm != "None":
                            name1 = [Meser.parse_obj({'first_name': nmnm})]
                        try:
                            name2 = await bot.api.users.get(nid)
                            await ans.answer(
                                f'[id{ans.from_id}|{name1[0].first_name}] замутил(a)  [id{nid}|{name2[0].first_name}] на {mutre.split()[0].strip()} минут\nПричина: {prin}'
                            )
                        except:
                            await ans.answer(
                                f'[id{nid}|{name1[0].first_name}] замутил(а) пользователя на {mutre.split()[0].strip()} минут\nПричина: {prin}'
                            )

                    except:
                        await ans.answer('Введите корректное число минут')

        else:
            await ans.answer('У вас недостаточно прав для использования этой команды.\nМинимальная роль-модер')

    # stmoder
    if "/ban" in ans.text or "/unban" in ans.text or "/addmoder" in ans.text or "/removerole" in ans.text or "/zov" in ans.text or "/online" in ans.text or "/banlist" in ans.text or "/onlinelist" in ans.text:
        if role in [("admin",), ("zspadmin",), ("spadmin",), ("stmoder",),
                    ("stadmin",), ('creator',)]:
            if "/zov" in ans.text:
                mss1 = (ans.text.removeprefix("/zov")).strip()
                cursor.execute("SELECT type FROM chats WHERE id=(?)", (ans.chat_id,))
                stat_tip = cursor.fetchone()
                if stat_tip[0] != "lider":
                    await ans.answer(
                        "@all\nВы были вызваны администртором беседы\n\nПричина вызова: "
                        + mss1)
                else:
                    await ans.answer("Команда недоступна в данном типе беседы")
            elif "/online" in ans.text:
                mss1 = (ans.text.removeprefix("/online")).strip()
                await ans.answer(
                    "@online\nВы были вызваны администртором беседы\n\nПричина вызова: "
                    + mss1)
            elif ans.text == "/banlist":
                cursor.execute("SELECT * FROM chat" + str(ans.chat_id))
                buser = cursor.fetchall()
                bust1 = []
                bust2 = []
                ban_str = ""
                for bus in buser:
                    try:
                        if bus[3] == "2888q01q01q23q59q59q100000" and int(bus[0]) > 0:
                            name = await bot.api.users.get(bus[0])
                            bust1.append(name[0].first_name)
                            bust2.append(bus[0])
                    except:
                        print("rrr")
                for i in range(len(bust2)):
                    ban_str = ban_str + str(i +
                                            1) + ". " + f'[id{bust2[i]}|{bust1[i]}]\n'
                if ban_str == "":
                    await ans.answer("В этом чате нет забаненных пользователей")
                else:
                    await ans.answer(ban_str)
            elif "/onlinelist" == ans.text:
                cursor.execute("SELECT idd FROM chat" + str(ans.chat_id))
                zuser = cursor.fetchall()
                zust1 = []
                zust2 = []
                znick_str = ""
                for zus in zuser:
                    naon = await bot.api.users.get(zus[0], fields="online")
                    if int(zus[0]) > 0 and str(naon[0].online) == "BaseBoolInt.yes":
                        zust1.append(naon[0].first_name)
                        zust2.append(zus[0])
                for i in range(len(zust2)):
                    znick_str = znick_str + str(
                        i + 1) + ". " + f'[id{zust2[i]}|{zust1[i]}]\n'
                if znick_str == "":
                    await ans.answer("Кроме вас в этом чате нет пользователей онлайн")
                else:
                    await ans.answer(znick_str)
            elif "/addmoder" in ans.text:
                nom2 = (ans.text.removeprefix("/addmoder")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                try:
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)",
                        (
                            "moder",
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначил(а) [id{nid}|{name2[0].first_name}] модератором'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначила(а) пользователя модератором'
                        )
                except:
                    await ans.answer("Что-то пошло не так...\nПопробуйте ещё раз")
            elif "/removerole" in ans.text:
                nom2 = (ans.text.removeprefix("/removerole")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                cursor.execute(
                    "UPDATE chat" + str(ans.chat_id) + " SET rol=null WHERE idd=(?)",
                    (nid,))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                nmnm = str((cursor.fetchone())[0])
                if nmnm != "None":
                    name1 = [Meser.parse_obj({'first_name': nmnm})]
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] удалил(a) роль [id{nid}|{name2[0].first_name}]'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] удалил(a) роль пользователя'
                    )
            elif "/unban" in ans.text:
                nom2 = (ans.text.removeprefix("/unban")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                try:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET mute=(?) WHERE idd=(?)",
                        (
                            "1900q01q01q23q59q59q100000",
                            nid,
                        ))
                    conn.commit()
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM other WHERE gban=(?)", (nid,))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] разбанил(a) [id{nid}|{name2[0].first_name}]'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] разбанил(а) пользователя'
                        )
                except:
                    await ans.answer('Что-то пошло не так...\nПопробуйте еще раз')
            elif "/ban" in ans.text and "/banlist" not in ans.text and "/banword" not in ans.text:
                nom3 = (ans.text.removeprefix("/ban")).strip()
                if nom3 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                        prich = "Не указана"
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom3:
                    if nom3.split("]")[1].strip() == "":
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = "Не указана"
                    else:
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = str(nom3.split("]")[1].strip())
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = str(nom3.split(" ")[1].strip())
                    except:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)

                        prich = "Не указана"
                elif ans.reply_message:
                    nid = ans.reply_message.from_id
                    prich = str(nom3.strip())
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                if int(nid) > 0:
                    try:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(ans.chat_id) +
                            " SET mute=(?), prban=(?), dban=(?), mmute=(?) WHERE idd=(?)", (
                                "2888q01q01q23q59q59q100000",
                                prich,
                                str(datetime.now()),
                                ans.from_id,
                                nid,
                            ))
                        conn.commit()
                        await bot.api.messages.remove_chat_user(chat_id=ans.chat_id,
                                                                    member_id=nid)
                        name1 = await bot.api.users.get(ans.from_id)
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                        nmnm = str((cursor.fetchone())[0])
                        if nmnm != "None":
                            name1 = [Meser.parse_obj({'first_name': nmnm})]
                        try:
                            name2 = await bot.api.users.get(nid)
                            await ans.answer(
                                f'[id{ans.from_id}|{name1[0].first_name}] забанил(a) [id{nid}|{name2[0].first_name}]'
                            )
                        except:
                            await ans.answer(
                                f'[id{ans.from_id}|{name1[0].first_name}] забанил(а) пользователя'
                            )
                    except Exception as error:
                        if str(error)=="User not found in chat":

                            conn = sqlite3.connect('BD-gbt.db')
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT OR IGNORE INTO chat" + str(ans.chat_id) +
                                " (idd,mute,prban,dban,mmute,iwarn) VALUES (?,?,?,?,?,?)", (
                                    nid,
                                    "2888q01q01q23q59q59q100000",
                                    prich,
                                    str(datetime.now()),
                                    ans.from_id,
                                    "",
                                ))
                            conn.commit()
                            await ans.answer("Пользователь успешно добавлен в бан")
                        else:
                            await ans.answer('Что-то пошло не так...')
                            print(error)
        else:
            await ans.answer(
                'У вас недостаточно прав для использования этой команды.\nМинимальная роль- старший модер'
            )

    # admin
    if "/skick" in ans.text or "/bug" in ans.text or "/quiet" in ans.text or "/sban" in ans.text or "/sunban" in ans.text or "/addsenmoder" in ans.text:
        if role in [("admin",), ("zspadmin",), ("spadmin",), ("stadmin",),
                    ("creator",)]:
            if ans.text in "/bug":
                await ans.answer(
                    "Напишите о баге в сообщения сообщества(бота) с тегом #bug")
            elif "/quiet" == ans.text:
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT quiet FROM chats WHERE id=(?)", (ans.chat_id,))
                squiet = cursor.fetchone()
                if squiet[0] == "off":
                    cursor.execute("UPDATE chats SET quiet=(?) WHERE id=(?)", (
                        "on",
                        ans.chat_id,
                    ))
                    conn.commit()
                    await ans.answer('Режим тишины включен')
                elif squiet[0] == "on":
                    cursor.execute("UPDATE chats SET quiet=(?) WHERE id=(?)", (
                        "off",
                        ans.chat_id,
                    ))
                    conn.commit()
                    await ans.answer('Режим тишины выключен')
                else:
                    await ans.answer(
                        "Что-то пошло не так...\nНапишите в сообщения сообщества(бота) с тегом #bug"
                    )
                    print('Режим тишины. В бд ошибка.')
                conn.commit()
            if "/addsenmoder" in ans.text:
                nom2 = (ans.text.removeprefix("/addsenmoder")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                try:
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)",
                        (
                            "stmoder",
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначил(а) [id{nid}|{name2[0].first_name}] старшим модератором'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначила(а) пользователя старшим модератором'
                        )
                except:
                    await ans.answer("Что-то пошло не так...\nПопробуйте ещё раз")
            elif "/skick" in ans.text:
                nom2 = (ans.text.removeprefix("/skick")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT server FROM chats WHERE id=(?)",
                               (ans.chat_id,))
                servt = cursor.fetchone()
                cursor.execute("SELECT id FROM chats WHERE server=(?)", (servt[0],))
                servav = cursor.fetchall()
                try:
                    for ser in servav:
                        await bot.api.messages.remove_chat_user(chat_id=ser, member_id=nid)
                except:
                    print("555555")
                name1 = await bot.api.users.get(ans.from_id)
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                nmnm = str((cursor.fetchone())[0])
                if nmnm != "None":
                    name1 = [Meser.parse_obj({'first_name': nmnm})]
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] исключил(a) [id{nid}|{name2[0].first_name}] из бесед сервера "{servt[0]}"'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] исключил(а) пользователя из бесед сервера "{servt[0]}"'
                    )
            elif "/sban" in ans.text:
                nom3 = (ans.text.removeprefix("/sban")).strip()
                if nom3 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                        prich = "Не указана"
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom3:
                    if nom3.split("]")[1].strip() == "":
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = "Не указана"
                    else:
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = str(nom3.split("]")[1].strip())
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = str(nom3.removeprefix(str(nom3.split(" ")[0])).strip())
                    except ValueError:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = "Не указана"
                elif ans.reply_message:
                    nid = ans.reply_message.from_id
                    prich = str(nom3.strip())
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                if int(nid) > 0:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT server FROM chats WHERE id=(?)",
                                   (ans.chat_id,))
                    sbvt = cursor.fetchone()
                    if sbvt[0] != "null000":
                        cursor.execute("SELECT id FROM chats WHERE server=(?)",
                                       (sbvt[0],))
                        sbvav = cursor.fetchall()
                        for sbv in sbvav:
                            conn = sqlite3.connect('BD-gbt.db')
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE chat" + str(sbv[0]) +
                                " SET mute=(?), prban=(?), dban=(?), mmute=(?) WHERE idd=(?)", (
                                    "2888q01q01q23q59q59q100000",
                                    prich,
                                    str(datetime.now()),
                                    ans.from_id,
                                    nid,
                                ))
                            conn.commit()
                            try:
                                await bot.api.messages.remove_chat_user(chat_id=sbv[0],
                                                                        member_id=nid)
                            except:
                                print("bbb")
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] забанил(a) [id{nid}|{name2[0].first_name}] в беседах сервера "{sbvt[0]}"\nПричина: {prich}'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] забанил(а) пользователя в беседах сервера "{sbvt[0]}"'
                        )
            elif "/sunban" in ans.text:
                nom2 = (ans.text.removeprefix("/sunban")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT server FROM chats WHERE id=(?)",
                               (ans.chat_id,))
                sbvt = cursor.fetchone()
                cursor.execute("SELECT id FROM chats WHERE server=(?)", (sbvt[0],))
                sbunvav = cursor.fetchall()
                for sbunv in sbunvav:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE chat" + str(sbunv[0]) + " SET mute=(?) WHERE idd=(?)", (
                            "1900q01q01q23q59q59q100000",
                            nid,
                        ))
                    conn.commit()
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM other WHERE gban=(?)", (nid,))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                nmnm = str((cursor.fetchone())[0])
                if nmnm != "None":
                    name1 = [Meser.parse_obj({'first_name': nmnm})]
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] разбанил(a) [id{nid}|{name2[0].first_name}] в беседах сервера "{sbvt[0]}"'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] разбанил(а) пользователя в беседах сервера "{sbvt[0]}"'
                    )

        else:
            await ans.answer(
                'У вас недостаточно прав для использования этой команды.\nМинимальная роль - админ'
            )

    # stadmin
    if "/gban" in ans.text or "/gunban" in ans.text or "/addadmin" in ans.text or "/type" in ans.text or "/sync" in ans.text or "/server" in ans.text or "/gbanlist" in ans.text or "/addword" in ans.text or "/delword" in ans.text or "/settings" in ans.text or "/filter" in ans.text or "/banwords" in ans.text or "/gbanpl" in ans.text or "gunbanpl" in ans.text:
        if role in [("zspadmin",), ("spadmin",), ("stadmin",), ("creator",)]:
            if "/addword" in ans.text:
                novslov = (ans.text.removeprefix("/addword")).strip()
                if novslov != "":
                    cursor.execute(
                        "INSERT OR IGNORE INTO filtr" + str(ans.chat_id) +
                        "(slova) VALUES (?)", (novslov,))
                    conn.commit()
                    await ans.answer('Слово добавлено')
                else:
                    await ans.answer('Напишите слово после команды')
            elif "/delword" in ans.text:
                delslov = (ans.text.removeprefix("/delword")).strip()
                if delslov != "":
                    try:
                        cursor.execute(
                            "DELETE FROM filtr" + str(ans.chat_id) + " WHERE slova=(?)",
                            (delslov,))
                        conn.commit()
                        await ans.answer('Слово удалено')
                    except:
                        await ans.answer('Ошибка...\nСкорее всего слова нет в банлисте')
                else:
                    await ans.answer('Напишите слово после команды')
            elif "/filter" == ans.text:
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT filtr FROM chats WHERE id=(?)", (ans.chat_id,))
                sfilt = cursor.fetchone()
                if sfilt[0] == "off":
                    cursor.execute("UPDATE chats SET filtr=(?) WHERE id=(?)", (
                        "on",
                        ans.chat_id,
                    ))
                    conn.commit()
                    await ans.answer('Фильтр включен')
                elif sfilt[0] == "on":
                    cursor.execute("UPDATE chats SET filtr=(?) WHERE id=(?)", (
                        "off",
                        ans.chat_id,
                    ))
                    conn.commit()
                    await ans.answer('Фильтр выключен')
                else:
                    await ans.answer(
                        'Фильтр. В бд ошибка.\nОбратитесь в сообщения сообщества(бота)')
            elif "/banwords" == ans.text:
                cursor.execute("SELECT slova FROM filtr" + str(ans.chat_id))
                bwuser = cursor.fetchall()
                bword_str = ""
                for nus in bwuser:
                    bword_str = bword_str + str(nus[0]) + "\n"
                if bword_str == "":
                    await ans.answer("В этом чате нет заблокированных слов")
                else:
                    await ans.answer(bword_str)
            elif "/gbanlist" == ans.text:
                cursor.execute("SELECT gban FROM other")
                gbuser = cursor.fetchall()
                gbord_str = ""
                for gbus in gbuser:
                    gbord_str = gbord_str + "id" + str(gbus[0]) + "\n"
                if gbord_str == "":
                    await ans.answer("Пользователей в глобальном бане нет")
                else:
                    await ans.answer(gbord_str)
            elif "/server" in ans.text:
                novserv = (ans.text.removeprefix("/server")).strip()
                if novserv != "":
                    cursor.execute("UPDATE chats SET server=(?) WHERE id=(?)", (
                        novserv,
                        ans.chat_id,
                    ))
                    conn.commit()
                    await ans.answer(f'Беседа привязана к серверу "{novserv}"')
                else:
                    await ans.answer('Напишите название сервера после команды')
            elif "/type" in ans.text:
                novtype = (ans.text.removeprefix("/type")).strip()
                if novtype == "game" or novtype == "admin" or novtype == "lider":
                    cursor.execute("UPDATE chats SET type=(?) WHERE id=(?)", (
                        novtype,
                        ans.chat_id,
                    ))
                    conn.commit()
                    await ans.answer(f'Новый тип беседы "{novtype}"')
                else:
                    await ans.answer(
                        'Напишите тип после команды. Доступные типы:\ngame - беседа игроков\nadmin - беседа администраторов\nlider- беседа лидеров или хелперов'
                    )
            elif "/sync" == ans.text:
                conn = sqlite3.connect('BD-gbt.db')
                conn.commit()
                conn.close()
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM chats")
                znack = cursor.fetchall()
                qw = 0


                if qw == 0:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS chat" + str(ans.chat_id) +
                        "(idd INTEGER PRIMARY KEY, rol TEXT, nick TEXT, mute TEXT, prban TEXT, dban TEXT, warn INTEGER DEFAULT 0, owarn INTEGER DEFAULT 0, iwarn TEXT )"
                    )
                    cursor.execute("INSERT OR IGNORE INTO chats (id) VALUES (?)",
                                   (ans.chat_id,))
                    conn.commit()
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS filtr" + str(ans.chat_id) +
                                   "(slova TEXT PRIMARY KEY)")

                    conn.commit()
                    memb = await api.messages.get_conversation_members(peer_id=ans.peer_id)
                    for m in memb.items:
                        if str(m.is_owner) == "True":
                            conn = sqlite3.connect('BD-gbt.db')
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT OR IGNORE INTO chat" + str(ans.chat_id) +
                                " (idd,rol,mute,iwarn) VALUES (?,?,?,?)", (
                                    m.member_id,
                                    "creator",
                                    "1900q01q01q23q59q59q100000",
                                    "",
                                ))
                            conn.commit()
                        else:
                            conn = sqlite3.connect('BD-gbt.db')
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT OR IGNORE INTO chat" + str(ans.chat_id) +
                                " (idd,mute,iwarn) VALUES (?,?,?)", (
                                    m.member_id,
                                    "1900q01q01q23q59q59q100000",
                                    "",
                                ))
                            conn.commit()

                await ans.answer("Синхронизация завершена")
            elif "/settings" == ans.text:
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM chats WHERE id=(?)", (ans.chat_id,))
                sin = cursor.fetchall()
                await ans.answer(
                    f'Фильтр: {sin[0][1]}\nРежим тишины: {sin[0][2]}\nТип: {sin[0][3]}\nСервер: {sin[0][4]}'
                )
            elif "/addadmin" in ans.text:
                nom2 = (ans.text.removeprefix("/addadmin")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                try:
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)",
                        (
                            "admin",
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначил(а) [id{nid}|{name2[0].first_name}] админом'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначила(а) пользователя админом'
                        )
                except:
                    await ans.answer("Что-то пошло не так...\nПопробуйте ещё раз")
            elif "/gbanpl" in ans.text:
                nom3 = (ans.text.removeprefix("/gbanpl")).strip()
                if nom3 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                        prich = "Не указана"
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom3:
                    if nom3.split("]")[1].strip() == "":
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = "Не указана"
                    else:
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = str(nom3.split("]")[1].strip())
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split()[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = str(nom3.removeprefix(str(nom3.split()[0])).strip())
                        if prich=="":
                            prich = "Не указана"
                    except ValueError:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = "Не указана"
                elif ans.reply_message:
                    nid = ans.reply_message.from_id
                    prich = str(nom3.strip())
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                if int(nid) > 0:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM chats WHERE type=(?)", ("game",))
                    gpbvav = cursor.fetchall()
                    for gpbv in gpbvav:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        try:
                            await bot.api.messages.remove_chat_user(chat_id=gpbv[0],
                                                                    member_id=nid)
                            cursor.execute(
                                "UPDATE chat" + str(gpbv[0]) +
                                " SET mute=(?), prban=(?), dban=(?),mmute=(?) WHERE idd=(?)", (
                                    "2888q01q01q23q59q59q100000",
                                    prich,
                                    str(datetime.now()),
                                    ans.from_id,
                                    nid,
                                ))
                            conn.commit()
                        except Exception as error:
                            if str(error) == "User not found in chat":

                                conn = sqlite3.connect('BD-gbt.db')
                                cursor = conn.cursor()
                                cursor.execute(
                                    "INSERT OR IGNORE INTO chat" + str(gpbv[0]) +
                                    " (idd,mute,prban,dban,mmute,iwarn) VALUES (?,?,?,?,?,?)", (
                                        nid,
                                        "2888q01q01q23q59q59q100000",
                                        prich,
                                        str(datetime.now()),
                                        ans.from_id,
                                        "",
                                    ))
                                conn.commit()
                            else:
                                await ans.answer('Что-то пошло не так...')
                                print(error)
                    name1 = await bot.api.users.get(ans.from_id)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                    nmnm = str((cursor.fetchone())[0])
                    if nmnm != "None":
                        name1 = [Meser.parse_obj({'first_name': nmnm})]
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] забанил(a) [id{nid}|{name2[0].first_name}] в беседах игроков\nПричина: {prich}'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] забанил(а) пользователя в беседах игроков\nПричина: {prich}'
                        )
            elif "/gunbanpl" in ans.text:
                nom2 = (ans.text.removeprefix("/gunbanpl")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM chats WHERE type=(?)", ("game",))
                gpbvav = cursor.fetchall()
                for gpbv in gpbvav:
                    try:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(gpbv[0]) + " SET mute=(?) WHERE idd=(?)", (
                                "1900q01q01q23q59q59q100000",
                                nid,
                            ))
                        conn.commit()
                    except:
                        print("YYY")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM other WHERE gban=(?)", (nid,))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT nick FROM chat" + str(ans.chat_id) + " WHERE idd=(?)", (ans.from_id,))
                nmnm = str((cursor.fetchone())[0])
                if nmnm != "None":
                    name1 = [Meser.parse_obj({'first_name': nmnm})]
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] разбанил(a) [id{nid}|{name2[0].first_name}] в беседах игроков'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] разбанил(а) пользователя в беседах игроков'
                    )
            elif "/gban" in ans.text:
                nom3 = (ans.text.removeprefix("/gban")).strip()
                if nom3 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                        prich = "Не указана"
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom3:
                    if nom3.split("]")[1].strip() == "":
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = "Не указана"
                    else:
                        nid = nom3.removeprefix("[id").split("|")[0]
                        prich = str(nom3.split("]")[1].strip())
                elif "vk.com/" in nom3:
                    try:
                        fgr = nom3.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = str(nom3.removeprefix(str(nom3.strip().split(" ")[0])).strip())
                        if prich=="":
                            prich = "Не указана"
                    except:
                        fgr = nom3.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                        prich = "Не указана"
                elif ans.reply_message:
                    nid = ans.reply_message.from_id
                    prich = str(nom3.strip())
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                print(nid)
                if int(nid) > 0:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM chats")
                    gbvav = cursor.fetchall()
                    for gbv in gbvav:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(gbv[0]) +
                            " SET mute=(?), prban=(?), dban=(?), mmute=(?) WHERE idd=(?)", (
                                "2888q01q01q23q59q59q100000",
                                prich,
                                str(datetime.now()),
                                ans.from_id,
                                nid,
                            ))
                        conn.commit()
                        try:
                            await bot.api.messages.remove_chat_user(chat_id=gbv[0],
                                                                    member_id=nid)
                            print("succes")
                        except Exception as error:
                            if str(error) == "User not found in chat":

                                conn = sqlite3.connect('BD-gbt.db')
                                cursor = conn.cursor()
                                cursor.execute(
                                    "INSERT OR IGNORE INTO chat" + str(gbv[0]) +
                                    " (idd,mute,prban,dban,mmute,iwarn) VALUES (?,?,?,?,?,?)", (
                                        nid,
                                        "2888q01q01q23q59q59q100000",
                                        prich,
                                        str(datetime.now()),
                                        ans.from_id,
                                        "",
                                    ))
                                conn.commit()
                            else:
                                await ans.answer('Что-то пошло не так...')
                                print(error)
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT OR IGNORE INTO other (gban) VALUES (?)",
                                   (nid,))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] забанил(a) [id{nid}|{name2[0].first_name}] во всех беседах\nПричина: {prich}'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] забанил(а) пользователя во всех беседах\nПричина: {prich}'
                        )
            elif "/gunban" in ans.text:
                nom2 = (ans.text.removeprefix("/gunban")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM chats")
                gunbvav = cursor.fetchall()
                for gunbv in gunbvav:

                    try:
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE chat" + str(gunbv[0]) + " SET mute=(?) WHERE idd=(?)",
                            (
                                "1900q01q01q23q59q59q100000",
                                nid,
                            ))
                        conn.commit()
                    except:
                        print("WWW")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM other WHERE gban=(?)", (nid,))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] разбанил(a) [id{nid}|{name2[0].first_name}] во всех беседах'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] разбанил(а) пользователя во всех беседах'
                    )

        else:
            await ans.answer(
                'У вас недостаточно прав для использования этой команды.\nМинимальная роль - старший админ'
            )

    # zspadmin
    if "/gremoverole" in ans.text or "/gzov" in ans.text or "/gsync" in ans.text or "/gnlist" in ans.text or "/urkick" in ans.text or "/addsenadm" in ans.text:
        if role in [("zspadmin",), ("spadmin",), ("creator",)]:
            if "/gsync" == ans.text:
                conn = sqlite3.connect('BD-gbt.db')
                conn.commit()
                conn.close()
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                await ans.answer(
                    "Синхронизация завершена\nЕсли вы заметели, что синхронизировалось не все, попробуйте синхронизировать еще раз или перезагрузите бота"
                )
            elif "/urkick" == ans.text:
                cursor.execute("SELECT * FROM chat" + str(ans.chat_id))
                kuser = cursor.fetchall()
                kqdr = 1
                for kus in kuser:
                    if (str(kus[1]) == "null" or kus[1] == None) and int(kus[0]) > 0:
                        kqdr = 5
                        await bot.api.messages.remove_chat_user(chat_id=ans.chat_id,
                                                                member_id=kus[0])
                        conn = sqlite3.connect('BD-gbt.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "DELETE FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
                            (kus[0],))
                        conn.commit()
                if kqdr == 1:
                    await ans.answer("В этом чате нет пользователей без ролей")
                else:
                    await ans.answer('Пользователи исключены из беседы')
                    kqdr = 1
            elif "/gzov" in ans.text:
                mss = (ans.text.removeprefix("/gzov")).strip()
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM chats WHERE NOT type='lider'")
                gzvav = cursor.fetchall()
                for gzv in gzvav:
                    await bot.api.messages.send(
                        chat_id=gzv[0],
                        message=
                        "@all \nВы были вызваны администратором беседы\n\nПричина вызова: "
                        + mss,
                        random_id=0)
            elif "/gnlist" == ans.text:
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM chats")
                gzvav = cursor.fetchall()
                for gzv in gzvav:
                    cursor.execute("SELECT * FROM chat" + str(gzv[0]))
                    nuser = cursor.fetchall()
                    nust1 = []
                    nust2 = []
                    nust3 = []
                    nick_str = ""
                    for nus in nuser:
                        if str(nus[2]) != "null" and int(nus[0]) > 0 and str(
                                nus[2]) != "None":
                            name = await bot.api.users.get(nus[0])
                            nust1.append(name[0].first_name)
                            nust2.append(nus[0])
                            nust3.append(nus[2])
                    for i in range(len(nust2)):
                        nick_str = nick_str + str(
                            i + 1) + ". " + f'[id{nust2[i]}|{nust1[i]}]-{nust3[i]}\n'
                    if nick_str == "":
                        await bot.api.messages.send(
                            chat_id=gzv[0],
                            message="В этом чате нет пользователей с никами",
                            random_id=0)

                    else:
                        await bot.api.messages.send(chat_id=gzv[0],
                                                    message=nick_str,
                                                    random_id=0)
                    await ans.answer("Списки ников отправлены")
            elif "/addsenadm" in ans.text:
                nom2 = (ans.text.removeprefix("/addsenadm")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                try:
                    cursor.execute(
                        "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)",
                        (
                            "stadmin",
                            nid,
                        ))
                    conn.commit()
                    name1 = await bot.api.users.get(ans.from_id)
                    try:
                        name2 = await bot.api.users.get(nid)
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначил(а) [id{nid}|{name2[0].first_name}] старшим админом'
                        )
                    except:
                        await ans.answer(
                            f'[id{ans.from_id}|{name1[0].first_name}] назначила(а) пользователя старшим админом'
                        )
                except:
                    await ans.answer("Что-то пошло не так...\nПопробуйте ещё раз")
            elif "/gremoverole" in ans.text:
                nom2 = (ans.text.removeprefix("/gremoverole")).strip()
                if nom2 == "":
                    if ans.reply_message:
                        nid = ans.reply_message.from_id
                    else:
                        await ans.answer(
                            'Ответьте на сообщение или упомяните пользователя после команды'
                        )
                elif "[id" in nom2:
                    nid = nom2.removeprefix("[id").split("|")[0]
                elif "vk.com/" in nom2:
                    try:
                        fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                    except ValueError:
                        fgr = nom2.removeprefix("https://vk.com/")
                        nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                else:
                    await ans.answer("Упомяните пользователя с помощью * или @")
                conn = sqlite3.connect('BD-gbt.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM chats")
                grvav = cursor.fetchall()
                for grv in grvav:
                    conn = sqlite3.connect('BD-gbt.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE chat" + str(grv[0]) + " SET rol=null WHERE idd=(?)",
                        (nid,))
                    conn.commit()
                await ans.answer('Пользователь лишен ролей')
        else:
            await ans.answer(
                'У вас недостаточно прав для использования этой команды.\nМинимальная роль - зам. спец. админа'
            )
    # spadmin
    if "/addzsa" in ans.text:
        if role == [("spadmin",), ("creator",)]:
            nom2 = (ans.text.removeprefix("/addzsa")).strip()
            if nom2 == "":
                if ans.reply_message:
                    nid = ans.reply_message.from_id
                else:
                    await ans.answer(
                        'Ответьте на сообщение или упомяните пользователя после команды')
            elif "[id" in nom2:
                nid = nom2.removeprefix("[id").split("|")[0]
            elif "vk.com/" in nom2:
                try:
                    fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                    nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                except ValueError:
                    fgr = nom2.removeprefix("https://vk.com/")
                    nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
            else:
                await ans.answer("Упомяните пользователя с помощью * или @")
            try:
                cursor.execute(
                    "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)", (
                        "zspadmin",
                        nid,
                    ))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] назначил(а) [id{nid}|{name2[0].first_name}] модератором'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] назначила(а) пользователя зам. спец. админом'
                    )
            except:
                await ans.answer("Что-то пошло не так...\nПопробуйте ещё раз")

        else:
            await ans.answer(
                'У вас недостаточно прав для использования этой команды.\nМинимальная роль - спец. админ'
            )
    # creator
    if "/addsa" in ans.text:
        if role == ("creator",):
            nom2 = (ans.text.removeprefix("/addsa")).strip()
            if nom2 == "":
                if ans.reply_message:
                    nid = ans.reply_message.from_id
                else:
                    await ans.answer(
                        'Ответьте на сообщение или упомяните пользователя после команды')
            elif "[id" in nom2:
                nid = nom2.removeprefix("[id").split("|")[0]
            elif "vk.com/" in nom2:
                try:
                    fgr = nom2.removeprefix("https://vk.com/").split(" ")[0]
                    nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
                except ValueError:
                    fgr = nom2.removeprefix("https://vk.com/")
                    nid = int((await bot.api.users.get(user_ids=fgr))[0].id)
            else:
                await ans.answer("Упомяните пользователя с помощью * или @")
            try:
                cursor.execute(
                    "UPDATE chat" + str(ans.chat_id) + " SET rol=(?) WHERE idd=(?)", (
                        "spadmin",
                        nid,
                    ))
                conn.commit()
                name1 = await bot.api.users.get(ans.from_id)
                try:
                    name2 = await bot.api.users.get(nid)
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] назначил(а) [id{nid}|{name2[0].first_name}] спец админом'
                    )
                except:
                    await ans.answer(
                        f'[id{ans.from_id}|{name1[0].first_name}] назначила(а) пользователя спец админом'
                    )
            except:
                await ans.answer("Что-то пошло не так...\nПопробуйте ещё раз")

        else:
            await ans.answer(
                'У вас недостаточно прав для использования этой команды.\nМинимальная роль - создатель'
            )

    if stat_fil == "on" and int(ans.from_id) > 0:
        conn = sqlite3.connect('BD-gbt.db')
        cursor = conn.cursor()
        cursor.execute("SELECT slova FROM filtr" + str(ans.chat_id))
        slva = cursor.fetchall()
        for slv in slva:
            if slv[0] in ans.text.lower():
                await bot.api.messages.delete(peer_id=ans.peer_id,
                                              cmids=ans.conversation_message_id,
                                              delete_for_all=True,
                                              group_id=ans.group_id)
                await ans.answer("Сообщение удалено, тк слово '" + slv +
                                 "' присутствует в банлисте")

    conn = sqlite3.connect('BD-gbt.db')
    cursor = conn.cursor()
    cursor.execute("SELECT mute FROM chat" + str(ans.chat_id) + " WHERE idd=(?)",
                   (ans.from_id,))
    m_b = cursor.fetchone()
    if datetime.now() <= datetime.strptime(m_b[0], '%Yq%mq%dq%Hq%Mq%Sq%f'):
        await bot.api.messages.delete(peer_id=ans.peer_id,
                                      cmids=ans.conversation_message_id,
                                      delete_for_all=True,
                                      group_id=ans.group_id)
    conn.commit()

    if rquiet == "on":
        await bot.api.messages.delete(peer_id=ans.peer_id,
                                      cmids=ans.conversation_message_id,
                                      delete_for_all=True,
                                      group_id=ans.group_id)


conn.close()
keep_alived()
bot.run_forever()
