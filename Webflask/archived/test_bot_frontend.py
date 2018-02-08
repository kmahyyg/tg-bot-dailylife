#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import logging
import telebot, time
from telebot import types

from apikey import tgbottoken

bot = telebot.TeleBot(tgbottoken)

# Test Environment with GFW Involved
telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}


# telebot.logger.setLevel(logging.DEBUG)

# {"ok":true,"result":[{"update_id":93210382,\n"message":{"message_id":116,"from":{"id":492263923,"is_bot":false,"first_name":"rm -rf --Low-End-Person","last_name":"| RES L6","username":"uuidgen","language_code":"zh-CN"},"chat":{"id":492263923,"first_name":"rm -rf --Low-End-Person","last_name":"| RES L6","username":"uuidgen","type":"private"},"date":1518076761,"reply_to_message":{"message_id":115,"from":{"id":505582682,"is_bot":true,"first_name":"Hacking Lifestyle","username":"lifehap4_yygbot"},"chat":{"id":492263923,"first_name":"rm -rf --Low-End-Person","last_name":"| RES L6","username":"uuidgen","type":"private"},"date":1518076759,"text":"SENDTO?"},"text":"bullshit"}}]}''"
#
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to use @uuidgen bot")


@bot.message_handler(commands=['newtest'])
def newtest(msg):
    cid = msg.chat.id
    markup = types.ForceReply(selective=False)
    sendto = bot.send_message(cid, "", reply_markup=markup)
    ques1id = sendto.message_id


bot.polling(none_stop=True)
