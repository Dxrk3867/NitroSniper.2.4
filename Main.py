import json
import re
import requests
from time import sleep
import colorama
import datetime
import discord
import os
from colorama import Fore
from playsound import playsound
from discord.ext import commands

# CONFIG 
with open("config.json") as f:
    config = json.load(f)
onalt = config.get("on_alt")
token = config.get("token")
rtoken = config.get("reedem_token")
edelay = config.get("delay_enabled")
delay = config.get("delay")
giveaway_sniper = config.get("giveaway_sniper")
slotbot_sniper = config.get("slotbot_sniper")
nitro_sniper = config.get("nitro_sniper")
airdrop_sniper = config.get("airdrop_sniper")
webhooknotification = config.get("webhook_notification")
sound_notification = config.get("sound_notification")
webhook = config.get("webhook")
botlist = config.get("bot_list")
altlist = config.get("alt_list")
# CONFIG END
sname = ""
stag = ""
if os.path.isfile("tried-nitro-codes.txt"):
    with open("tried-nitro-codes.txt", "r") as fp:
        usedcodes = json.load(fp)
else:
    usedcodes = []


def codestart():
    global sname, stag
    if onalt:
        headers = {"Authorization": rtoken, "Content-Type": "application/json"}
        res = requests.get(
            "https://canary.discordapp.com/api/v6/users/@me", headers=headers
        )
        res = res.json()
        sname = res["username"]
        stag = res["discriminator"]
    if onalt:
        onaltt = " "
    else:
        if sname != "":
            onaltt = f"{Fore.LIGHTBLACK_EX}({sname}#{stag})"
        else:
            onaltt = " "
    if edelay:
        ddelay = f"{Fore.LIGHTBLACK_EX}({delay} seconds)"
    else:
        ddelay = " "
    print(
        f"""{Fore.RESET}
                                     {Fore.WHITE}  _____            _     _____ _   _ _                 
                                     {Fore.GREEN} |  __ \          | |   / ____| \ | (_)                
                                     {Fore.WHITE} | |  | |_  ___ __| | _| (___ |  \| |_ _ __   ___ _ __ 
                                     {Fore.GREEN} | |  | \ \/ / '__| |/ /\___ \| . ` | | '_ \ / _ \ '__|
                                     {Fore.WHITE} | |__| |>  <| |  |   < ____) | |\  | | |_) |  __/ |   
                                     {Fore.GREEN} |_____//_/\_\_|  |_|\_\_____/|_| \_|_| .__/ \___|_|   
                                     {Fore.WHITE}                                      | |              
                                     {Fore.GREEN}                                      |_|              

                                     {Fore.GREEN}Connected User     -  {Fore.GREEN}{Sniper.user.name}#{Sniper.user.discriminator}

                                     {Fore.BLUE}Nitro Sniper    -  {Fore.GREEN}{nitro_sniper} {onaltt}
                                     {Fore.WHITE}Giveaway Sniper -  {Fore.GREEN}{giveaway_sniper} {ddelay}

    """
        + Fore.RESET
    )


colorama.init()
Sniper = commands.Bot(description="Discord Sniper.2.4", command_prefix="", self_bot=True)


def Clear():
    print("\n" * 100)


Clear()


def Init():
    if onalt:
        if config.get("token") == config.get("reedem-token"):
            Clear()
            print(
                f"\n\n{Fore.RED}Error {Fore.WHITE}Alt token connot be same as Redeem Token!"
                + Fore.RESET
            )
            exit()
        if rtoken == "your-token":
            Clear()
            print(
                f"\n\n{Fore.RED}Error {Fore.WHITE}You didn't put your alt token in the config.json file"
                + Fore.RESET
            )
            exit()
        else:
            headers = {"Authorization": rtoken, "Content-Type": "application/json"}
            r = requests.get(
                "https://canary.discordapp.com/api/v6/users/@me", headers=headers
            )
            if r.status_code == 200:
                pass
            else:
                print(
                    f"\n\n{Fore.RED}Error {Fore.WHITE}Alt Token is invalid" + Fore.RESET
                )
                exit()
    if config.get("token") == "token-here":
        Clear()
        print(
            f"\n\n{Fore.RED}Error {Fore.WHITE}You didn't put your token in the config.json file"
            + Fore.RESET
        )
        exit()
    else:
        token = config.get("token")
        try:
            Sniper.run(token, reconnect=True)
        except discord.errors.LoginFailure:
            print(f"\n\n{Fore.RED}Error {Fore.WHITE}Token is invalid" + Fore.RESET)
            exit()


@Sniper.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, "original", error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, discord.errors.Forbidden):
        print(f"{Fore.RED}Error: {Fore.WHITE}Discord error: {error}" + Fore.RESET)
    else:
        print(f"{Fore.RED}Error: {Fore.WHITE}{error_str}" + Fore.RESET)


@Sniper.event
async def on_message(message):
    global note_text

    def GiveawayInfo(elapsed):
        print(
            f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
            f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"
            f"\n{Fore.LIGHTBLACK_EX} Elapsed: {Fore.WHITE}{elapsed}s" + Fore.RESET
        )

    def GiveawayDelayInfo():
        print(
            f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
            f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"
            f"\n{Fore.LIGHTBLACK_EX} Delay: {Fore.WHITE}{delay} seconds" + Fore.RESET
        )

    def NitroInfo(elapsed, code):
        print(
            f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
            f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"
            f"\n{Fore.LIGHTBLACK_EX} Author: {Fore.WHITE}{message.author}"
            f"\n{Fore.LIGHTBLACK_EX} Author ID: {Fore.WHITE}{message.author.id}"
            f"\n{Fore.LIGHTBLACK_EX} Elapsed: {Fore.WHITE}{elapsed}s"
            f"\n{Fore.LIGHTBLACK_EX} Code: {Fore.WHITE}{code}" + Fore.RESET
        )

    time = datetime.datetime.now().strftime("%H:%M")
    if (
        "discord.gift/" in message.content
        or "discord.com/gifts/" in message.content
        or "discordapp.com/gifts/" in message.content
    ):
        if nitro_sniper:
            start = datetime.datetime.now()
            if "discord.gift/" in message.content:
                code = re.findall("discord[.]gift/(\w+)", message.content)
            if "discordapp.com/gifts/" in message.content:
                code = re.findall("discordapp[.]com/gifts/(\w+)", message.content)
            if "discord.com/gifts/" in message.content:
                code = re.findall("discord[.]com/gifts/(\w+)", message.content)
            for code in code:
                if len(code) == 16 or len(code) == 24:
                    if code not in usedcodes:
                        usedcodes.append(code)
                        with open("tried-nitro-codes.txt", "w") as fp:
                            json.dump(usedcodes, fp)
                        if onalt:
                            headers = {"Authorization": rtoken}
                        else:
                            headers = {"Authorization": token}
                        r = requests.post(
                            f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem",
                            headers=headers,
                        ).text
                        elapsed = datetime.datetime.now() - start
                        elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
                        if "This gift has been redeemed already." in r:
                            print(
                                ""
                                f"\n{Fore.RED}{time} - Nitro is Already Redeemed"
                                + Fore.RESET
                            )
                            NitroInfo(elapsed, code)
                        elif "subscription_plan" in r:
                            if sound_notification == True:
                                try:
                                    playsound("./sounds/success.wav")
                                except:
                                    pass

                            print(
                                ""
                                f"\n{Fore.GREEN}{time} - Nitro Successfuly Claimed!"
                                + Fore.RESET
                            )
                            NitroInfo(elapsed, code)
                            if webhooknotification:
                                data = {
                                    "embeds": [
                                        {
                                            "title": "Successfully Sniped Nitro Gift!",
                                            "description": f"Congratulations, good job! You can view your Nitro Gifts in your inventory.\n\nNitro Gift Server:\n{message.guild}\n\nNitro Gift Sender:\n{message.author}\n\nNitro Gift Code:\n{code}",
                                            "url": "https://github.com/lnxcz/discord-sniper",
                                            "color": 16732345,
                                            "footer": {"text": "lnxcz's sniper"},
                                            "image": {
                                                "url": "https://i.imgur.com/9QVtF0t.png"
                                            },
                                        }
                                    ],
                                    "username": f"Sniper | {Sniper.user.name}#{Sniper.user.discriminator}",
                                    "avatar_url": str(Sniper.user.avatar_url),
                                }
                                requests.post(webhook, json=data)
                        elif "Unknown Gift Code" in r:
                            print(
                                ""
                                f"\n{Fore.YELLOW}{time} - Unknown Nitro Gift Code"
                                + Fore.RESET
                            )
                            NitroInfo(elapsed, code)
        else:
            return
    # Don't react to all messages
    # Don't react to DMs
    if message.content or message.embeds and message.guild:
        if giveaway_sniper:
            if (
                message.author.id in botlist
                and not (
                    f"@{Sniper.user.id}" in message.content
                    or f"<@{Sniper.user.id}>" in message.content
                )
                and not (
                    "Giveaway ended" in message.content
                    or "Congratulations" in message.content
                )
            ):
                start = datetime.datetime.now()
                try:
                    if not edelay:
                        await message.add_reaction("🎉")
                        elapsed = datetime.datetime.now() - start
                        elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
                except discord.errors.Forbidden:
                    print(
                        ""
                        f"\n{Fore.RED}{time} - Couldn't React to Giveaway" + Fore.RESET
                    )
                    GiveawayInfo(elapsed)
                if edelay:
                    print("" f"\n{Fore.GREEN}{time} - Giveaway Found!" + Fore.RESET)
                    GiveawayDelayInfo()
                else:
                    print("" f"\n{Fore.GREEN}{time} - Giveaway Sniped" + Fore.RESET)
                    GiveawayInfo(elapsed)
                try:
                    if edelay:
                        sleep(delay)
                        await message.add_reaction("🎉")
                        print("")
                        print(
                            f"{Fore.GREEN}Giveaway Sniped with delay {delay} seconds!"
                        )
                except discord.errors.Forbidden:
                    print(
                        ""
                        f"\n{Fore.RED}{time} - Couldn't React to Giveaway" + Fore.RESET
                    )
                    GiveawayInfo(elapsed)
                if webhooknotification:
                    if message.content and message.embeds:
                        message_content = (
                            "`"
                            + message.content.replace("`", "").replace("\\", "")[:500]
                            + "`"
                            + "\n"
                            + "***Message Embed***: "
                            + "`"
                            + str(message.embeds[0].title)
                            + "\n"
                            + str(message.embeds[0].description)
                            .replace("`", "")
                            .replace("\\", "")[:500]
                            + "`"
                        )
                    elif message.embeds and not message.content:
                        message_content = (
                            "Empty Message\n"
                            + "***Message Embed***: "
                            + "`"
                            + str(message.embeds[0].title)
                            + "\n"
                            + str(message.embeds[0].description)
                            .replace("`", "")
                            .replace("\\", "")[:500]
                            + "`"
                        )
                    elif message.content and not message.embeds:
                        message_content = (
                            "`"
                            + message.content.replace("`", "").replace("\\", "")[:500]
                            + "`"
                        )
                    else:
                        message_content = "No content"
                    data = {
                        "embeds": [
                            {
                                "title": "Giveaway Joined!",
                                "description": f"**Message content**:\n {message_content}\n**Giveaway Server**: `{message.guild}`\n**Channel**: `#{message.channel}`\n**Bot**: `{message.author.name}`",
                                "url": message.jump_url,
                                "color": 3407667,
                            }
                        ],
                        "username": f"Sniper | {Sniper.user.name}#{Sniper.user.discriminator}",
                        "avatar_url": str(Sniper.user.avatar_url),
                    }
                    requests.post(webhook, json=data)
        else:
            return
    if (
        f"@{Sniper.user.id}" in message.content
        or f"<@{Sniper.user.id}>" in message.content
    ):
        if giveaway_sniper:
            if message.author.id in botlist:
                print("" f"\n{Fore.GREEN}{time} - Giveaway Won" + Fore.RESET)
                elapsed = "-"
                GiveawayInfo(elapsed)
                if webhooknotification:
                    if message.content and message.embeds:
                        message_content = (
                            "`"
                            + message.content.replace("`", "").replace("\\", "")[:500]
                            + "`"
                            + "\n"
                            + "***Message Embed***: "
                            + "`"
                            + str(message.embeds[0].title)
                            + "\n"
                            + str(message.embeds[0].description)
                            .replace("`", "")
                            .replace("\\", "")[:500]
                            + "`"
                        )
                    elif message.embeds and not message.content:
                        message_content = (
                            "Empty Message\n"
                            + "***Message Embed***: "
                            + "`"
                            + str(message.embeds[0].title)
                            + "\n"
                            + str(message.embeds[0].description)
                            .replace("`", "")
                            .replace("\\", "")[:500]
                            + "`"
                        )
                    elif message.content and not message.embeds:
                        message_content = (
                            "`"
                            + message.content.replace("`", "").replace("\\", "")[:500]
                            + "`"
                        )
                    else:
                        message_content = "No content"
                    data = {
                        "embeds": [
                            {
                                "title": "Giveaway Won!",
                                "description": f"**Message content**:\n {message_content}\n**Giveaway Server**: `{message.guild}`\n**Channel**: `#{message.channel}`",
                                "url": message.jump_url,
                                "color": 16732345,
                            }
                        ],
                        "username": f"Sniper | {Sniper.user.name}#{Sniper.user.discriminator}",
                        "avatar_url": str(Sniper.user.avatar_url),
                    }
                    requests.post(webhook, json=data)
        else:
            return

    await Sniper.process_commands(message)


@Sniper.event
async def on_connect():
    Clear()
    codestart()


Init()
