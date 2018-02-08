#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Guilty officer Telegram game bot created by @rainzy
This code is protected under the GNU General Public License v3.0 (GNU GPLv3)


"""

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import time
from random import randint
import sqlite3
from threading import Thread

#Dev Mode
DEVMODE = False
whitelist = -1001212923181
whitelist2 = -1001355546339
#connect database
conn = sqlite3.connect('database.sqlite')
#create cursor
c = conn.cursor()

### CREATE TABLES ###
c.execute('''CREATE TABLE IF NOT EXISTS players
             (ID real, TelegramID text, displayName text, username text, admin text, role text)''')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


#no game running on start
game_running = False 


def start(bot, update, args):
    cmembers = update.effective_chat.get_members_count()
    if "join" in args:
        btnTelegramID = update.effective_user.id
        btndisplayName = update.effective_user.first_name
        btnusername = update.effective_user.username
        btnadmin = "null"
        btnrole = "null"
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        if c.lastrowid == None:
            ID = 1
        else:
            ID = ID + 1
        print(c.lastrowid)
        print(btnTelegramID)
        c.execute("INSERT INTO players (ID, TelegramID, displayName, username, admin, role) VALUES (?, ?, ?, ?, ?, ?)", (ID,btnTelegramID,btndisplayName,btnusername,btnadmin,btnrole))
        conn.commit()
        bot.send_message(chat_id=update.effective_chat.id, text="I have added you to the game.")
    elif cmembers == 2 and "join" not in args:
        update.message.reply_text("Hello {}! Thank you for starting me. Type /help to get started.".format(update.effective_user.first_name))

def join(bot, update):
    """Send a message when the command /start=join is issued."""
    print("HELLO!")

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help list will appear here.')

def chatinfo(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text="chat ID: " + str(update.effective_chat.id) + "\nUser ID: " + str(update.effective_user.id) + "\nFirst name: " + str(update.effective_user.first_name) + "\nusername: " + str(update.effective_user.username))
def developer(bot, update):
    """Send a message when the command /developer is issued."""
    update.message.reply_text('@rainzy is my creator. Please respect her.')


def guiltyofficer(bot, update):
    """Send a message when the command /guiltyofficer is issued."""
    #bot.send_message(chat_id=update.effective_chat.id, text="test", parse_mode="Markdown")
    #is game running?
    print(update.effective_chat.id)
    cmembers = update.effective_chat.get_members_count()
    global game_running #Needs a join timer!
    global DEBUG
    if DEVMODE == True: #allows games in PM
        cmembers = 4
    if game_running == False and cmembers > 3 and (update.effective_chat.id == whitelist or update.effective_chat.id == whitelist2):
        game_running = True
        #reset players table in database
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute("DELETE FROM players")
        conn.commit()
        
        keyboard = [[InlineKeyboardButton("Join Game!", callback_data='start=join')]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        object_message_button = bot.send_message(chat_id=update.effective_chat.id, text="**{}** has started a game of guilty officer!\nUse the button to join the game.".format(update.effective_user.first_name), reply_markup=reply_markup, parse_mode="Markdown")
        bot.send_message(chat_id=update.effective_chat.id, text="Players that joined:\n-----")#►

        t1 = Thread(target=loadgame, args=(bot, update, object_message_button))
        t1.start()

    #if games can't start
    elif cmembers < 4:
        bot.send_message(chat_id=update.effective_chat.id, text="Add me to a group of 4 or more players to play!")
    elif game_running == True and (update.effective_chat.id == whitelist or update.effective_chat.id == whitelist2):
        bot.send_message(chat_id=update.effective_chat.id, text="Game is already running!")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text="I only work in selective groups. contact my /developer for more information.")

    
def loadgame(bot,update, object_message_button):
    if DEVMODE == True:
        n = 25
    else:
        n = 115
    object_message = bot.send_message(chat_id=update.effective_chat.id, text='creating game...')
    time.sleep(1)
    object_message.edit_text('Game is starting in 120 seconds!')
    time.sleep(0.5)
    bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=object_message.message_id)
    while n > 0:
        object_message.edit_text('Game is starting in ' + str(n) + " seconds!")
        n = n - 5
        time.sleep(5)
    if n == 0:
        print ("Game is starting, please wait..")
        object_message.edit_text('Game is starting, check your PMs!')
        bot.unpin_chat_message(chat_id=update.effective_chat.id, message_id=object_message.message_id)
        time.sleep(2)
        bot.delete_message(chat_id=update.effective_chat.id, message_id=object_message.message_id)
        bot.delete_message(chat_id=update.effective_chat.id, message_id=object_message_button.message_id)
        

def button(bot, update):
    query = update.callback_query
    bot.answerCallbackQuery(callback_query_id=query.id, url="t.me/camelliaxtestbot?start=join")
    
        
def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler, don't forget to insert your Bot's token!
    updater = Updater(token='TOKEN')
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Telegram commands
    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ci", chatinfo))
    dp.add_handler(CommandHandler("guiltyofficer", guiltyofficer))
    dp.add_handler(CommandHandler("developer", developer))
    dp.add_handler(CallbackQueryHandler(button)) #code for button

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
