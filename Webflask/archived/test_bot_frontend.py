#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import logging
import telebot
from telebot import types

from apikey import tgbottoken

bot = telebot.TeleBot(tgbottoken)

# Test Environment with GFW Involved
telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to use @uuidgen bot")


@bot.message_handler(commands=['newtest'])
def newtest(msg):
    cid = msg.chat.id
    mk1 = types.ForceReply(selective=False)
    bot.send_message(cid, "SENDTO?", reply_markup=mk1)


bot.polling(none_stop=True)
