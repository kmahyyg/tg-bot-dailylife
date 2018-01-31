#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import telebot
from apikey import tgbottoken

bot = telebot.TeleBot(tgbottoken)

# Test Environment with GFW Involved
telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to use @uuidgen bot")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Only4Test")


bot.polling()
