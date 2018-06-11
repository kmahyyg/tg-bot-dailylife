![version](https://img.shields.io/badge/version-1.3.0-blue.svg)
![license](https://img.shields.io/github/license/kmahyyg/life-tg-bot.svg)
![Python](https://img.shields.io/badge/Python-3.6-ff69b4.svg)
![star](https://img.shields.io/github/stars/kmahyyg/life-tg-bot.svg)

# Current Status

Need PR.

# Python - TG BOT - YYG

This bot is used to simplify the app you installed in your phone.
In China mainland, The Android APP eco system is really terrible.

As the most powerful Bot API I have ever seen, I hope that, one day in the future I could only use Telegram to do most of my life.

# Download and Deploy

```bash
touch /var/run/tgbot.pid && chmod 666 /var/run/tgbot.pid
git clone https://github.com/kmahyyg/life-tg-bot.git
cd ./life-tg-bot/
sudo pip3 install -r requirements.txt
chmod +x ./*.py
chmod +x ./*.sh
chmod +x ./*.service
cp ./tgbot-yyg.service /etc/systemd/system/
```

Renamed `apikey.py.eg` to `apikey.py` in this dircetory, input your API KEY there.

Then:

```bash
python3 ./tgbot_fnA.py
```

## Dependencies

See more details in requirements.txt

# Personally

Never use Wechat / QQ. Open a issue here.

# License

All my open-source project are licensed under AGPL V3, it never has been changed.

# About us

I'm now a freshman in a university. In the past few years, I use ```@chinanet``` TG BOT which brought me a lot of 
happiness. We love checking express packages and make jokes on each other.

However, It stopped working a few years ago.

I'm trying to practice my programming ability and write this bot to enjoy myself.

# Thanks

@bennythink

1. https://blog.nfz.moe/archives/how-to-write-beautiful-github-readme.html
2. https://github.com/BennyThink/ExpressBot
3. http://drakeet.me/create-telegram-bot-with-python/
4. https://www.stackoverflow.com
5. https://www.liaoxuefeng.com   Thanks for his tutorials. Very useful for green hands.
6. https://github.com/eternnoir/pyTelegramBotAPI
7. https://github.com/coderfox/Kuaidi100API
8. http://www.bennythink.com
9. https://fast.v2ex.com/member/showfom  and his https://ip.sb https://sm.ms https://u.nu

# TODO

- [x] | 1. AliBaba Cloud Package Tracker API Integration
- [x] | 2. Package BOT Frontend Authentication
- [x] | 3. Use Flask to do a second pack of third-party API
- [x] | 4. Kuaidi100 API Package Tracker API Integration
- [x] | 5. Turing-Chat API Integration [Artificial Fool]
- [X] | 6. SendGrid Inbound Mail Process WebHook. 
- [X] | 7. pyTelegramBotAPI Frontend Interaction.

<del> [WILL NEVER DO] | 8. Chat Messages FLAG Detection and Auto-Reply. (Reason: No Database!) </del>

- [X] | 9. Use ``` https://ip.sb ``` API to get GEOIP info.
- [ ] | 10. Use this bot to manage a channel.

# Bugs and Issues

- [x] | SFExpress cannot use Kuaidi100 API.

- [X] | Watchdog service and error handler need to be updated. Welcome PR.

Others still remain unknown.

