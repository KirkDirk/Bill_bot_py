# Код для телеграм-бота для учета статистики игры на бильярде

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

import db_rewrite

with open("token.txt", "r", encoding = "UTF-8") as num_token:
    token = num_token.read()

logging.basicConfig(
    filename="log.txt",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOISE, TYPE_STRIKE, RES_STRIKE = range(3)
STRIKE, STAT, EXITS, MINE_S, ALIEN_S, HIT_S, MISS_S = range(7)

def start(update, _):
    keyboard = [
        [
            InlineKeyboardButton("Удар", callback_data=str(STRIKE)),
            InlineKeyboardButton("Статистика", callback_data=str(STAT)),
        ],
        [InlineKeyboardButton("Не сегодня", callback_data=str(EXITS))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Добро пожаловать в бота.\nПожалуйста, выберите:", reply_markup=reply_markup)
    return CHOISE

def strike(update, _):        
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Свой", callback_data=str(MINE_S)),
            InlineKeyboardButton("Чужой", callback_data=str(ALIEN_S)),
        ],
        [
            InlineKeyboardButton("Закончить", callback_data=str(EXITS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите удар:", reply_markup=reply_markup)
    return TYPE_STRIKE

# формат данных в файле db.txt: 
# [0] всего ударов, [1] из них своих, [2] из них чужих, 
# [3] забитых, [4] процент, 
# [5] из них своих, [6] процент, [7] из них чужих, [8] процент

def mine(update, _):
    data_play = db_rewrite.read_db()
    global temp_type_strike 
    temp_type_strike = "mine"
    data_play[0] += 1
    data_play[1] += 1
    db_rewrite.write_db(data_play)
    
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Попадание", callback_data=str(HIT_S)),
            InlineKeyboardButton("Промах", callback_data=str(MISS_S)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("И каков результат:", reply_markup=reply_markup)
    return RES_STRIKE

def alien(update, _):
    data_play = db_rewrite.read_db()
    global temp_type_strike 
    temp_type_strike = "alien"
    data_play[0] += 1
    data_play[2] += 1
    db_rewrite.write_db(data_play)
    
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Попадание", callback_data=str(HIT_S)),
            InlineKeyboardButton("Промах", callback_data=str(MISS_S)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("И каков результат:", reply_markup=reply_markup)
    return RES_STRIKE

def hit(update, _):
    data_play = db_rewrite.read_db()
    data_play[3] += 1
    data_play[4] = 100*data_play[3]//data_play[0]
    if temp_type_strike == "mine": 
        data_play[5] += 1
        data_play[6] = 100*data_play[5]//data_play[3]
    if temp_type_strike == "alien": 
        data_play[7] += 1
        data_play[8] = 100*data_play[7]//data_play[3]
    db_rewrite.write_db(data_play)
    
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Удар", callback_data=str(STRIKE)),
            InlineKeyboardButton("Закончить", callback_data=str(EXITS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)   
    query.edit_message_text("Продолжим?", reply_markup=reply_markup) 
    return CHOISE

def miss(update, _):
    data_play = db_rewrite.read_db()
    data_play[4] = 100*data_play[3]//data_play[0]
    db_rewrite.write_db(data_play)
    
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Удар", callback_data=str(STRIKE)),
            InlineKeyboardButton("Закончить", callback_data=str(EXITS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)   
    query.edit_message_text("Продолжим?", reply_markup=reply_markup)  
    return CHOISE    

def statistic(update, _):
    data_play = db_rewrite.read_db()
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Игра", callback_data=str(STRIKE)),
            InlineKeyboardButton("Закончить", callback_data=str(EXITS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"""
        Произведено ударов: {data_play[0]}\n
        Свой - {data_play[1]} : Чужой {data_play[2]}\n
        Забито: {data_play[3]}, что в процентах: {data_play[4]} %\n
        Из низ своих - {data_play[5]} : Из них чужих {data_play[7]}\n
        В процентах - {data_play[6]} % : {data_play[8]} %""", reply_markup=reply_markup)
    return CHOISE

def canсel(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Приходите катать ещё!")
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token)
    app = updater.dispatcher

    conv_handler = ConversationHandler(  
            entry_points=[CommandHandler("start", start)],
            states={
                CHOISE: [
                    CallbackQueryHandler(strike, pattern = "^" + str(STRIKE) + "$"),
                    CallbackQueryHandler(statistic, pattern =  "^" + str(STAT)+ "$"), 
                    CallbackQueryHandler(canсel, pattern = "^" + str(EXITS) + "$"), 
                ],
                TYPE_STRIKE: [
                    CallbackQueryHandler(mine, pattern = "^" + str(MINE_S) + "$"),
                    CallbackQueryHandler(alien, pattern = "^" + str(ALIEN_S) + "$"),
                    CallbackQueryHandler(canсel, pattern = "^" + str(EXITS) + "$")
                ],
                RES_STRIKE: [
                    CallbackQueryHandler(hit, pattern = "^" + str(HIT_S) + "$"),
                    CallbackQueryHandler(miss, pattern = "^" + str(MISS_S) + "$"),
                ],
            },
            fallbacks=[CommandHandler("cancel", canсel)],
        )
    app.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
