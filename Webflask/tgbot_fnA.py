#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import telebot
import time
from telebot import types
from apikey import tgbottoken, authedchat
from ymodules.m_aliexp import packagereq
from ymodules.m_ipip import ipsbgeo
from ymodules.m_kd100 import *
from ymodules.m_sendgrid import *
from ymodules.m_tuling123 import *

# define bot instance
bot = telebot.TeleBot(tgbottoken)
# telebot.logger.setLevel(logging.INFO)

# Test Environment with GFW Involved, fuck CCP
# telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}

# separate arguments into list to handle with msg text
def extract_arg(arg):
    return arg.split()[1:]


# show chat id and welcome msg
@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    msgid = str(msg.chat.id)
    reply_msg = "Welcome to use the bot of @uuidgen. We love @chinanet . \n Your Private Chat ID: " + msgid
    bot.reply_to(msg, reply_msg)


# if auto detect failed, ask user to check company code here.
@bot.message_handler(commands=['expcmpy'])
def cmd_expcmpy(msg):
    msgrpy = "This command is used to check the proper company code of express. \n https://github.com/kmahyyg/life-tg-bot/blob/dev/Webflask/expno.md "
    bot.reply_to(msg, msgrpy)


# check express package status
@bot.message_handler(commands=['express'])
def cmd_express(msg):
    msgid = msg.chat.id
    if (msgid in authedchat):
        exparg = extract_arg(msg.text)
        bot.send_chat_action(msgid, 'typing')
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


# thanks to ip.sb, use this api to get ip's geoip info and AS num
@bot.message_handler(commands=['ipip'])
def geoipinfo(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        ipaddr = extract_arg(msg.text)
        if (ipaddr == []):
            bot.reply_to(msg, "Illegal Input.")
        else:
            bot.send_chat_action(cid, 'typing')
            repy = ipsbgeo(ipaddr)
            bot.send_message(cid, repy)
    else:
        pass


# receive mail attachments

file_name = " "
file_mime = " "
mail_details = {}

@bot.message_handler(content_types=['document'])
def handle_file(msg):
    cid = msg.chat.id
    if (cid == authedchat[0]):
        bot.send_chat_action(cid, 'typing')
        file_info = bot.get_file(msg.document.file_id)
        file_size = msg.document.file_size
        file_mime = msg.document.mime_type
        if (file_size > 7340032):
            file_name = "/tmp" + str(msg.document.file_name)
            DFILE = open(file_name, 'wb')
            downloaded_file = bot.download_file(file_info.file_path)
            DFILE.write(downloaded_file)
            DFILE.close()
            mail_details['atth'] = True
            bot.send_message(cid, "File Successfully Received.")
        else:
            mail_details['atth'] = False
            bot.reply_to(msg, "File size exceeds the max size (7MiB).")
    else:
        pass


msginitid = 0
# handle new mail request with my sendgrid api, xxx.edu.pl
# data stru: mail_details = {to,subject,plaintext,atth,atthname,atthmime}
@bot.message_handler(commands=['sendmail'])
@bot.message_handler(func=lambda msg: ("mail_" in msg.text), content_types=['text'])  # index start from 0 to split
def mailwithsg(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        bot.send_chat_action(cid, 'typing')
        mkup = types.ForceReply(selective=False)
        sendto = bot.send_message(cid, "Send to? reply must start with mail_to:", reply_markup=mkup)
        msginitid = sendto.message_id
        if (msg.message_id == msginitid + 1):
            mail_details['to'] = (msg.text)
            mailsub = bot.send_message(cid, "Subject? reply must start with mail_subject:", reply_markup=mkup)
        elif (msg.message_id == msginitid + 3):
            mail_details['subject'] = (msg.text)
            mailcontent = bot.send_message(cid, "Content? reply must start with mail_cont:", reply_markup=mkup)
        elif (msg.message_id == msginitid + 5):
            mail_details['plaintext'] = (msg.text)
            mailattach = bot.send_message(cid, "Do you have attachment? Y/N ", reply_markup=mkup)
        elif (msg.message_id == msginitid + 7):
            if msg.text == 'Y':
                bot.send_message(cid, "Please send your attachment (1 File Only, must <7MiB)")
                time.sleep(30)
                mail_details['atth'] = True
                mail_details['atthname'] = file_name
                mail_details['atthmime'] = file_mime
            if msg.text == 'N':
                mail_details['atth'] = False
                bot.send_chat_action(cid, 'typing')
                bot.send_message(cid, "Done!")
                bot.send_message(cid, "Send /finalsend to send your mail.")
        else:
            pass


@bot.message_handler(commands=['finalsend'])
def finalsend(msg):
    cid = msg.chat.id
    if cid in authedchat:
        from time import sleep
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, "To:" + mail_details['to'] + '\n')
        bot.send_message(cid, "Subject:" + mail_details['subject'] + '\n')
        bot.send_message(cid, "Content:" + mail_details['plaintext'] + '\n')
        bot.send_message(cid, "Has attachment:" + str(mail_details['atth']) + '\n')
        bot.send_message(cid, "File Name:" + str(mail_details['file_name']) + '\n')
        bot.send_message(cid, "You send the mail with above datas." + '\n')
        bot.send_chat_action(cid, 'typing')
        sleep(5)
        # TODO SENDGRID_WITHOUT_ATTACH
        # TODO SENDGRID_WITH_ATTACH
        if (mail_details['atth'] == True):
            att1 = build_atth(mail_details['file_name'], mail_details['file_mime'])
            sendmail_withatth(mail_details, att1)
            bot.send_message(cid, "Successfully sent!")
        if (mail_details['atth'] == False):
            sendmail_noatth(mail_details)
            bot.send_message(cid, "Successfully sent!")
    else:
        pass

# tuling123 chat API introduced, proceed all text message
@bot.message_handler(content_types=['text'])
def chattuling(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        text = msg.text
        bot.send_chat_action(cid, 'typing')
        rpy = send_turing(text, cid)
        bot.reply_to(msg, rpy)
    else:
        pass

# polling updates, ignore errors to be focused on running
bot.polling(none_stop=True)
