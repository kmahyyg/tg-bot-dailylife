#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import time

import telebot
from telebot import types
from socket import gethostbyname
from apikey import tgbottoken, authedchat
from ymodules.m_aliexp import packagereq
from ymodules.m_ipip import ipsbgeo
from ymodules.m_kd100 import *
from ymodules.m_sendgrid import *
from ymodules.m_tuling123 import *
from ymodules.m_sentry import *
from ymodules.m_bdcall import *

# define bot instance
bot = telebot.TeleBot(tgbottoken)
YYGFile = open('/tmp/recvmails_yyg.dat', 'rb')
ECSFile = open('/tmp/recvmails_ecs.dat', 'rb')
SpamFile = open('/tmp/recvmails_idk.dat', 'rb')

import logging

telebot.logger.setLevel(logging.INFO)

# Test Environment with GFW Involved, fuck CCP
# telebot.apihelper.proxy = {'https': 'http://127.0.0.1:1085'}

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
                autodetect_cmpy_answer = 'The company auto-detected is: **' + str(
                    cmpy) + '** . If anything went wrong, append company code after you check it via /expcmpy.'
                bot.send_message(msgid, autodetect_cmpy_answer, parse_mode='Markdown')
                checked_pkg = ckkd100pkg(exparg[0], cmpy)
                bot.reply_to(msg, checked_pkg)
        elif (len(exparg) == 2):
            result1 = packagereq(exparg[0], exparg[1])
            checked_pkg = result1['result']['list'][0]
            bot.reply_to(msg, str(checked_pkg))
        else:
            bot.reply_to(msg, "Illegal Input[ERR-EXP-ELSE]")
    else:
        pass


# thanks to ip.sb, use this api to get ip's geoip info and AS num
@bot.message_handler(commands=['ipip'])
def geoipinfo(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        ipaddrlst = extract_arg(msg.text)
        try:
            ipaddr = ipaddrlst[0]
            ipaddr = gethostbyname(ipaddr)
            bot.send_chat_action(cid, 'typing')
            repy = ipsbgeo(ipaddr)
            bot.send_message(cid, repy)
        except IndexError as ierr:
            bot.reply_to(msg, 'Illgeal Input![IERR]')
            sendlog_sent()
        except UnboundLocalError as ubderr:
            bot.reply_to(msg, 'Illegal Input![UBDERR]')
            sendlog_sent()
    else:
        pass


# receive mail attachments

file_name = " "
file_confirm = " "
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
        if (file_size < 7340032):
            file_confirm = str(msg.document.file_name)
            file_name = "/tmp" + file_confirm
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
# data stru: mail_details = {from,to,subject,plaintext,atth,atthname,atthmime}
@bot.message_handler(commands=['sendmail'])
@bot.message_handler(func=lambda msg: ("mail_" in msg.text), content_types=['text'])  # index start from 0 to split
def mailwithsg(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        bot.send_chat_action(cid, 'typing')
        mkup = types.ForceReply(selective=False)
        bot.send_message(cid, "EACH MSG MUST START WITH **mail_**", parse_mode='Markdown')
        ask_frommsg = bot.send_message(cid, 'From which account? Fill in your username, start with mail_from:',
                                       reply_markup=mkup)
        msginitid = ask_frommsg.message_id
        if (msg.reply_to_message.message_id == msginitid):
            addr_fromm = str(msg.text)
            addr_fromm = addr_fromm.replace('mail_from:', '') + str("@ynu.edu.pl")
            mail_details['from'] = addr_fromm
            ask_tomsg = bot.send_message(cid, "Send to? reply must start with mail_to:", reply_markup=mkup)
            ask_tomsgid = ask_tomsg.message_id
        elif (msg.reply_to_message.message_id == ask_tomsgid):
            addr_to = str(msg.text)
            addr_to = addr_to.replace('mail_to:', '')
            mail_details['to'] = addr_to
            ask_submsg = bot.send_message(cid, "Subject? reply must start with mail_subject:", reply_markup=mkup)
            ask_submsgid = ask_submsg.message_id
        elif (msg.reply_to_message.message_id == ask_submsgid):
            mail_sub = str(msg.text)
            mail_sub = mail_sub.replace('mail_subject:', '')
            mail_details['subject'] = mail_sub
            ask_msgtext = bot.send_message(cid, "Content? reply must start with mail_cont:", reply_markup=mkup)
            ask_msgtextid = ask_msgtext.message_id
        elif (msg.reply_to_message.message_id == ask_msgtextid):
            mail_conc = str(msg.text)
            mail_conc = mail_conc.replace('mail_cont:', '')
            mail_details['plaintext'] = mail_conc
            ask_atthconfirm = bot.send_message(cid, "Do you have attachment? mail_Y/mail_N ", reply_markup=mkup)
            ask_atthconfirmid = ask_atthconfirm.message_id
        elif (msg.reply_to_message.message_id == ask_atthconfirmid):
            atth_conf = str(msg.text)
            atth_conf = atth_conf.replace('mail_', '')
            if atth_conf == 'Y':
                bot.send_message(cid, "Please send your attachment (1 File Only, must <7MiB, time out:30s)")
                time.sleep(32)
                mail_details['atth'] = True
                mail_details['atthname'] = file_name
                mail_details['atthmime'] = file_mime
            if atth_conf == 'N':
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
        bot.send_message(cid, "From:" + mail_details['from'] + '\n')
        bot.send_message(cid, "To:" + mail_details['to'] + '\n')
        bot.send_message(cid, "Subject:" + mail_details['subject'] + '\n')
        bot.send_message(cid, "Content:" + mail_details['plaintext'] + '\n')
        bot.send_message(cid, "Has attachment:" + str(mail_details['atth']) + '\n')
        bot.send_message(cid, "File Name:" + str(file_confirm) + '\n')
        bot.send_message(cid, "You send the mail with above datas." + '\n')
        bot.send_chat_action(cid, 'typing')
        sleep(5)
        if (mail_details['atth'] == True):
            att1 = build_atth(mail_details['file_name'], mail_details['file_mime'])
            sgmail = buildmail_withatth(mail_details, att1)
            sgsent = sendmail_atth(sgmail)
            bot.send_chat_action(cid, 'typing')
            bot.send_message(cid, sgsent)
            bot.send_message(cid, "Successfully sent!")
        if (mail_details['atth'] == False):
            sgresp = sendmail_noatth(mail_details)
            bot.send_chat_action(cid, 'typing')
            bot.send_message(cid, sgresp)
            bot.send_message(cid, "Successfully sent!")
    else:
        pass


@bot.message_handler(commands=['recvmail'])
def recvmail(msg):
    cid = msg.chat.id
    if (cid == authedchat[0]):
        bot.send_message(cid, 'Requested, Searching...')
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, 'File is now uploading...')
        bot.send_chat_action(cid, 'upload_document')
        bot.send_document(cid, YYGFile)
        bot.send_message(cid, 'Done!')
    else:
        pass


@bot.message_handler(commands=['disstel'])
def disssb(msg):
    cid = msg.chat.id
    tel4u = extract_arg(msg.text)
    tel4u = tel4u[0]
    telsta = check_phone(tel4u)

    if telsta == False:
        bot.reply_to(msg, 'Illegal Tel Number!')
    elif isinstance(telsta, str):
        resp = start_call(telsta)
    else:
        bot.reply_to(msg, 'Sent to queue.')

    if resp == False:
        bot.reply_to(msg, 'Unknown Error!')
    elif isinstance(resp,str):
        bot.reply_to(msg, str(resp))
    elif resp == True:
        bot.reply_to(msg, 'Sent to queue!')

        
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
try:
    from os import getpid
    pid = str(getpid())
    pidfile = open('/var/run/tgbot.pid', 'w')
    pidfile.write(pid)
    pidfile.close()
    bot.polling(none_stop=True, timeout=30, interval=5)
except:
    sendlog_sent()
