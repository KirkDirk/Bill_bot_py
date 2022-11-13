# Код для телеграм-бота с применением pyTelegramBotAPI

# import telebot
# from telebot import types

with open("token.txt", "r", encoding = "UTF-8") as num_token:
    token = num_token.read()

# bot = telebot.TeleBot(token)

# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button1 = types.KeyboardButton("+")
#     button2 = types.KeyboardButton("-")
#     button3 = types.KeyboardButton("*")
#     button4 = types.KeyboardButton("/")
#     markup.add(button1, button2, button3, button4)
#     bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user), reply_markup = markup)

# @bot.message_handler(content_types=["text"])
# def bot_message(message):
#     if message.chat.type == "private":
#         if message.text == "+":
#             bot.send_message(message.chat.id)

# bot.polling(none_stop = True)

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(
    filename='log.txt',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update, _):
    keyboard = [
        [
            InlineKeyboardButton("Тренировка", callback_data='1'),
            InlineKeyboardButton("Игра 1х1", callback_data='2'),
        ],
        [InlineKeyboardButton("Не сегодня", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Добро пожаловать в бильярд-бота.')
    update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

# выбор варианта кнопки, клик и возвращение результата
def button(update, _):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == "3": 
        query.edit_message_text(text=f"Тогда в другой раз.\nЗахочешь продолжить, нажми: /start")

# по команде подмоги
def help_command(update, _):
    update.message.reply_text("Используйте `/start` для тестирования.")

if __name__ == '__main__':
    updater = Updater(token)
    app = updater.dispatcher

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('help', help_command))

    updater.start_polling()
    updater.idle()

# import logging
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

# # Ведение журнала логов
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Этапы/состояния разговора
# FIRST, SECOND = range(2)
# # Данные обратного вызова
# ONE, TWO, THREE, FOUR = range(4)


# def start(update, _):
#     """Вызывается по команде `/start`."""
#     # Получаем пользователя, который запустил команду `/start`
#     user = update.message.from_user
#     logger.info("Пользователь %s начал разговор", user.first_name)
#     # Создаем `InlineKeyboard`, где каждая кнопка имеет 
#     # отображаемый текст и строку `callback_data`
#     # Клавиатура - это список строк кнопок, где каждая строка, 
#     # в свою очередь, является списком `[[...]]`
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
#     update.message.reply_text(
#         text="Запустите обработчик, выберите маршрут", reply_markup=reply_markup
#     )
#     # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
#     return FIRST


# def start_over(update, _):
#     """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
#     # Получаем `CallbackQuery` из обновления `update`
#     query = update.callback_query
#     # На запросы обратного вызова необходимо ответить, 
#     # даже если уведомление для пользователя не требуется.
#     # В противном случае у некоторых клиентов могут возникнуть проблемы.
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#    # Отредактируем сообщение, вызвавшее обратный вызов.
#    # Это создает ощущение интерактивного меню.
#     query.edit_message_text(
#         text="Выберите маршрут", reply_markup=reply_markup
#     )
#     # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
#     return FIRST


# def one(update, _):
#     """Показ нового выбора кнопок"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("3", callback_data=str(THREE)),
#             InlineKeyboardButton("4", callback_data=str(FOUR)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Вызов `CallbackQueryHandler`, выберите маршрут", reply_markup=reply_markup
#     )
#     return FIRST


# def two(update, _):
#     """Показ нового выбора кнопок"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("3", callback_data=str(THREE)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Второй CallbackQueryHandler", reply_markup=reply_markup
#     )
#     return FIRST


# def three(update, _):
#     """Показ выбора кнопок"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("Да, сделаем это снова!", callback_data=str(ONE)),
#             InlineKeyboardButton("Нет, с меня хватит ...", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Третий CallbackQueryHandler. Начать сначала?", reply_markup=reply_markup
#     )
#     # Переход в состояние разговора `SECOND`
#     return SECOND


# def four(update, _):
#     """Показ выбора кнопок"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#             InlineKeyboardButton("4", callback_data=str(FOUR)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Четвертый CallbackQueryHandler, выберите маршрут", reply_markup=reply_markup
#     )
#     return FIRST


# def end(update, _):
#     """Возвращает `ConversationHandler.END`, который говорит 
#     `ConversationHandler` что разговор окончен"""
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(text="See you next time!")
#     return ConversationHandler.END


# if __name__ == '__main__':
#     updater = Updater(token)
#     dispatcher = updater.dispatcher

#     # Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
#     # Используем параметр `pattern` для передачи `CallbackQueries` с
#     # определенным шаблоном данных соответствующим обработчикам
#     # ^ - означает "начало строки"
#     # $ - означает "конец строки"
#     # Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={ # словарь состояний разговора, возвращаемых callback функциями
#             FIRST: [
#                 CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
#                 CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
#                 CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
#                 CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
#             ],
#             SECOND: [
#                 CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
#                 CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
#             ],
#         },
#         fallbacks=[CommandHandler('start', start)],
#     )

#     # Добавляем `ConversationHandler` в диспетчер, который
#     # будет использоваться для обработки обновлений
#     dispatcher.add_handler(conv_handler)

#     updater.start_polling()
#     updater.idle()