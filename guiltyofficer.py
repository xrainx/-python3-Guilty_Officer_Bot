#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Guilty officer Telegram game bot created by @rainzy
This code is protected under the GNU General Public License v3.0 (GNU GPLv3)


"""

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler #for btn
import logging
import time
import sqlite3

#Debug Mode
DEBUG = True #coming soon

#connect database
conn = sqlite3.connect('database.sqlite')
#create cursor
c = conn.cursor()

### CREATE TABLES ###
### uncomment below to create the tables on first run, then include the comment to prevent "table already exists" error
#c.execute('''CREATE TABLE players
#             (ID real, TelegramID text, displayName text, username text, admin text, role text)''')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


#no game running on start
game_running = False #Needs a join timer!

def start(bot, update):
    """Send a message when the command /start is issued."""
    cmembers = update.effective_chat.get_members_count()
    if cmembers == 2:
        first_name = update.effective_user.first_name
        update.message.reply_text("Hello {}! Thank you for starting me.".format(first_name))

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help list will appear here.')

def developer(bot, update):
    """Send a message when the command /developer is issued."""
    update.message.reply_text('@rainzy is my creator. Please respect her.')


def guiltyofficer(bot, update):
    """Send a message when the command /guiltyofficer is issued."""

    #is game running?
    cmembers = update.effective_chat.get_members_count()
    global game_running
    if game_running == False and cmembers > 3:
        game_running = True
        #reset players table in database
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute("DELETE FROM players")
        conn.commit()
        
        keyboard = [[InlineKeyboardButton("Join Game!", callback_data='start=joingame')]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("{} has started a game of guilty officer!\nUse the button to join the game.".format(update.effective_user.first_name), reply_markup=reply_markup)
        update.message.reply_text("Players that joined:\n► " + update.effective_user.first_name) ##TODO: add if statement for telegram.Emoji.PURPLE_HEART  ##TODO: get ALL names from database and bot.edit_message_text
    elif cmembers < 4:
        update.message.reply_text("Add me to a group of 4 or more players to play!")
    elif game_running == True:
        update.message.reply_text("Game is already running!")
    else:
        update.message.reply_text("an impossible error has somehow occured. @rainzy I need help.")
    

   

def button(bot, update):
    query = update.callback_query
    ID = 1 #latest +1
    btnTelegramID = update.effective_user.id
    btndisplayName = update.effective_user.first_name
    btnusername = update.effective_user.username
    btnadmin = "null"
    btnrole = "null"

    
    #insert user into database
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO players VALUES ('ID','btnTelegramID','btndisplayName','btnusername','btnadmin','btnrole')")
    #telegram.Bot.answerInlineQuery(switch_pm_gamejoined)
    bot.edit_message_text(text="You have joined the game".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
        
    #joined = telegram.CallbackQuery
    
    #"You have joined the game!"
    
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
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
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
