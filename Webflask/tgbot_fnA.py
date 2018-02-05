#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import telebot
from telebot import types
from apikey import tgbottoken, authedchat
from ymodules.m_kd100 import *
from ymodules.m_aliexp import packagereq
from ymodules.m_ipip import ipsbgeo
bot = telebot.TeleBot(tgbottoken)

# Test Environment with GFW Involved
telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}

def extract_arg(arg):
    return arg.split()[1:]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    msgid = str(msg.chat.id)
    reply_msg = "Welcome to use the bot of @uuidgen. We love @chinanet . \n Your Private Chat ID: " + msgid
    bot.reply_to(msg, reply_msg)


@bot.message_handler(commands=['expcmpy'])
def cmd_expcmpy(msg):
    msgrpy = "This command is used to check the proper company code of express. \n https://github.com/kmahyyg/life-tg-bot/blob/dev/Webflask/expno.md "
    bot.reply_to(msg, msgrpy)

@bot.message_handler(commands=['express'])
def cmd_express(msg):
    msgid = msg.chat.id
    if (msgid == authedchat):
        exparg = extract_arg(msg.text)
        # indexerror, import types from telebot
        # except Exception as e: bot.reply_to(message,e)
        if (len(exparg) == 1):
            cmpy = checkcmpy(exparg[0])
            if (isinstance(cmpy, int) == True):
                bot.reply_to(msg, "Cannot auto detect company. \n Use /expcmpy to check proper company code.")
            elif (cmpy == 'shunfeng'):
                checked_pkg = packagereq(exparg[0], 'SFEXPRESS')
                final = checked_pkg['result']['list'][0]
                bot.reply_to(msg, str(final))
            else:
                checked_pkg = ckkd100pkg(exparg[0], cmpy)
                bot.reply_to(msg, checked_pkg)
        elif (len(exparg) == 2):
            result1 = packagereq(exparg[0], exparg[1])
            checked_pkg = result1['result']['list'][0]
            bot.reply_to(msg, str(checked_pkg))
        else:
            bot.reply_to(msg, "Illegal Input")
    else:
        pass


@bot.message_handler(commands=['newmail'])
def mailwithsg(msg):
    cid = msg.chat.id
    mkup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(cid, "Send me some text", reply_markup=mkup)


@bot.message_handler(commands=['ipip'])
def geoipinfo(msg):
    cid = msg.chat.id
    if (cid == authedchat):
        ipaddr = extract_arg(msg.text)
        if (ipaddr == []):
            bot.reply_to(msg, "Illegal Input.")
        else:
            repy = ipsbgeo(ipaddr)
            bot.send_message(cid, repy)
    else:
        pass


bot.polling(none_stop=True)
